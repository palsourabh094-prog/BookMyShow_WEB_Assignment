import re
import uuid
from collections import defaultdict
from datetime import timedelta
from pathlib import Path

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.db.models import Q
from django.http import FileResponse, Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.http import require_POST

from . import booking
from .forms import CheckoutForm, GiftCardForm, InquiryForm, NewsletterForm, SeatForm, SignupForm
from .models import Booking, GiftCard, Inquiry, Listing, NewsletterSubscription, Showtime, Venue

PAGE_COPY = {
    "movies": ("Movies", "Find your next big-screen story."),
    "stream": ("Stream", "Rent a short demo film and watch from home."),
    "events": ("Live events", "Live music, stand-up and nights worth going out for."),
    "plays": ("Plays", "Take your seat for stories told live on stage."),
    "sports": ("Sports", "Find a game to watch or a race to run."),
    "activities": ("Activities", "Make time for something hands-on, outdoors or a little unexpected."),
}
INQUIRY_COPY = {
    "list-your-show": ("List your show", "Tell us about your event and where you plan to host it."),
    "corporates": ("Corporate bookings", "Ask about group tickets, private screenings or gift cards for your team."),
    "help": ("Help centre", "Find answers about booking, then send us a message if you need a hand."),
}


def local_listings(request):
    listings = Listing.objects.all()
    region = request.session.get("region")
    if region:
        listings = listings.filter(Q(kind=Listing.Kind.STREAM) | Q(showtimes__venue__area=region)).distinct()
    return listings


def local_venues(request):
    venues = Venue.objects.filter(cinema=True)
    region = request.session.get("region")
    return venues.filter(area=region) if region else venues


def home(request):
    listings = local_listings(request)
    return render(request, "tickets/home.html", {
        "movies": listings.filter(kind=Listing.Kind.MOVIES).order_by("-featured", "id")[:5],
        "live_events": listings.filter(kind=Listing.Kind.EVENTS).order_by("-featured", "id")[:4],
        "stream_pick": listings.filter(kind=Listing.Kind.STREAM).first(),
    })


def catalog(request, kind=None):
    listings = local_listings(request)
    active_filters = {}
    filters = {}
    if kind:
        if kind not in PAGE_COPY:
            raise Http404
        heading, description = PAGE_COPY[kind]
        listings = listings.filter(kind=kind)
    else:
        heading, description = "Search", "Find a title, genre or language."
    query = request.GET.get("q", "").strip()[:100]
    if query:
        listings = listings.filter(
            Q(title__icontains=query) | Q(genre__icontains=query) | Q(language__icontains=query)
            | Q(showtimes__venue__name__icontains=query)
        ).distinct()

    for name in ("genre", "language", "format"):
        filters[name] = list(listings.order_by(name).values_list(name, flat=True).distinct())
        selected = request.GET.get(name)
        if selected in filters[name]:
            active_filters[name] = selected
    if active_filters:
        listings = listings.filter(**active_filters)

    return render(request, "tickets/catalog.html", {
        "heading": heading, "description": description, "listings": listings, "kind": kind,
        "filters": filters, "active_filters": active_filters, "query": query,
    })


def detail(request, slug):
    listing = get_object_or_404(Listing, slug=slug)
    related = local_listings(request).filter(kind=listing.kind).exclude(pk=listing.pk)[:4]
    return render(request, "tickets/detail.html", {"listing": listing, "related": related})


def cinemas(request):
    return render(request, "tickets/cinemas.html", {"venues": local_venues(request)})


def venue_detail(request, slug):
    venue = get_object_or_404(Venue, slug=slug, cinema=True)
    listings = Listing.objects.filter(showtimes__venue=venue).distinct()
    return render(request, "tickets/cinema_detail.html", {"venue": venue, "listings": listings})


def showtimes(request, slug):
    listing = get_object_or_404(Listing, slug=slug)
    if listing.kind == Listing.Kind.STREAM:
        return redirect("tickets:detail", slug=slug)
    days = booking.booking_days()
    day = booking.parse_day(request.GET.get("date")) or days[0]
    shows = listing.showtimes.select_related("venue")
    cinema = request.GET.get("cinema", "")
    if cinema:
        shows = shows.filter(venue__slug=cinema)
    elif region := request.session.get("region"):
        shows = shows.filter(venue__area=region)
    groups = defaultdict(list)
    for show in shows.order_by("venue__name", "time"):
        if booking.future(show, day):
            groups[show.venue].append(show)
    return render(request, "tickets/showtimes.html", {
        "listing": listing, "days": days, "day": day, "groups": dict(groups), "cinema": cinema,
    })


def seats(request, show_id, day):
    show = get_object_or_404(Showtime.objects.select_related("listing", "venue"), pk=show_id)
    date = booking.parse_day(day)
    if not date or not booking.future(show, date):
        messages.info(request, "This showtime is unavailable. Choose another time.")
        return redirect("tickets:showtimes", slug=show.listing.slug)
    occupied = booking.taken_seats(show, date)
    form = SeatForm(
        request.POST if request.method == "POST" else None, labels=sorted(booking.SEAT_LABELS - occupied),
    )
    if request.method == "POST" and form.is_valid():
        request.session["checkout"] = {
            "id": str(uuid.uuid4()), "listing": show.listing_id, "show": show.id,
            "date": date.isoformat(), "labels": form.cleaned_data["seats"],
        }
        return redirect("tickets:checkout")
    return render(request, "tickets/seats.html", {
        "show": show, "day": date, "seat_rows": booking.SEAT_ROWS, "occupied": occupied,
        "selected": set(request.POST.getlist("seats")) - occupied, "form": form,
    })


@require_POST
def rent(request, slug):
    listing = get_object_or_404(Listing, slug=slug, kind=Listing.Kind.STREAM)
    request.session["checkout"] = {"id": str(uuid.uuid4()), "listing": listing.pk}
    return redirect("tickets:checkout")


@login_required
def checkout(request):
    draft = request.session.get("checkout")
    if not draft:
        return redirect("tickets:bookings")
    existing = Booking.objects.filter(id=draft["id"], user=request.user).first()
    if existing:
        return redirect("tickets:confirmation", pk=existing.pk)
    listing = get_object_or_404(Listing, pk=draft["listing"])
    show, date = None, None
    labels = draft.get("labels", [])
    if draft.get("show"):
        show = get_object_or_404(Showtime.objects.select_related("venue"), pk=draft["show"], listing=listing)
        date = booking.parse_day(draft["date"])
        if not date or not booking.future(show, date):
            messages.info(request, "Choose a new showtime before checking out.")
            return redirect("tickets:showtimes", slug=listing.slug)
    form = CheckoutForm(request.POST if request.method == "POST" else None)
    if request.method == "POST" and form.is_valid():
        if request.POST.get("draft_id") != draft["id"]:
            form.add_error(None, "Your order changed in another tab. Review the updated order before confirming.")
        else:
            try:
                reservation = booking.confirm_booking(
                    user=request.user, listing=listing, showtime=show, day=date, labels=labels,
                    draft_id=draft["id"], **form.cleaned_data,
                )
            except booking.BookingError as error:
                form.add_error(error.field, str(error))
            else:
                return redirect("tickets:confirmation", pk=reservation.pk)
    return render(request, "tickets/checkout.html", {
        "listing": listing, "show": show, "day": date, "labels": labels,
        "subtotal": listing.price * (len(labels) if show else 1), "form": form, "draft_id": draft["id"],
    })


@login_required
def confirmation(request, pk):
    reservation = get_object_or_404(Booking, pk=pk, user=request.user)
    active = reservation.created_at + timedelta(hours=booking.RENTAL_HOURS) > timezone.now()
    return render(request, "tickets/confirmation.html", {"reservation": reservation, "rental_active": active})


@login_required
def download_receipt(request, pk):
    reservation = get_object_or_404(
        Booking.objects.select_related("listing", "showtime__venue").prefetch_related("seats"),
        pk=pk, user=request.user,
    )
    response = render(request, "tickets/receipt.txt", {"reservation": reservation}, content_type="text/plain; charset=utf-8")
    response["Content-Disposition"] = f'attachment; filename="booking-{reservation.pk}.txt"'
    response["Cache-Control"] = "private, no-store"
    return response


@login_required
def watch(request, pk):
    rental = get_object_or_404(Booking, pk=pk, user=request.user, listing__kind=Listing.Kind.STREAM)
    expires = rental.created_at + timedelta(hours=booking.RENTAL_HOURS)
    if expires <= timezone.now():
        messages.info(request, "This rental has expired.")
        return redirect("tickets:confirmation", pk=pk)
    return render(request, "tickets/watch.html", {"rental": rental, "expires": expires})


@login_required
def stream_media(request, pk):
    get_object_or_404(
        Booking, pk=pk, user=request.user, listing__kind=Listing.Kind.STREAM,
        created_at__gt=timezone.now() - timedelta(hours=booking.RENTAL_HOURS),
    )
    media = Path(__file__).resolve().parent / "media" / "last-light.mp4"
    if not media.is_file():
        raise Http404
    size = media.stat().st_size
    requested = request.headers.get("Range", "")
    if requested:
        match = re.fullmatch(r"bytes=(\d{0,19})-(\d{0,19})", requested)
        response = HttpResponse(status=416, headers={"Content-Range": f"bytes */{size}"})
        if match and any(match.groups()):
            start_text, end_text = match.groups()
            start = int(start_text) if start_text else max(0, size - int(end_text))
            end = min(size - 1, int(end_text)) if start_text and end_text else size - 1
            if 0 <= start <= end < size:
                with media.open("rb") as file:
                    file.seek(start)
                    content = file.read(end - start + 1)
                response = HttpResponse(content, status=206, content_type="video/mp4", headers={
                    "Content-Length": str(len(content)), "Content-Range": f"bytes {start}-{end}/{size}",
                })
    else:
        response = FileResponse(media.open("rb"), content_type="video/mp4")
    response["Accept-Ranges"] = "bytes"
    response["Cache-Control"] = "private, no-store"
    return response


@login_required
def bookings(request):
    reservations = Booking.objects.filter(user=request.user).select_related("listing", "showtime__venue")
    cards = GiftCard.objects.filter(purchaser=request.user)
    return render(request, "tickets/bookings.html", {"reservations": reservations, "gift_cards": cards})


@sensitive_post_parameters("password1", "password2")
def signup(request):
    next_url = request.POST.get("next", request.GET.get("next", ""))
    if not url_has_allowed_host_and_scheme(next_url, {request.get_host()}, require_https=request.is_secure()):
        next_url = ""
    if request.user.is_authenticated:
        return redirect(next_url or "tickets:home")
    form = SignupForm(request.POST if request.method == "POST" else None)
    if request.method == "POST" and form.is_valid():
        try:
            with transaction.atomic():
                user = form.save()
        except IntegrityError:
            form.add_error("email", "An account already uses this email.")
        else:
            login(request, user)
            messages.success(request, "Your account is ready.")
            return redirect(next_url or "tickets:home")
    return render(request, "tickets/signup.html", {"form": form, "next": next_url})


@require_POST
def set_region(request):
    region = request.POST.get("region", "")
    if region in {"", *Venue.Area.values}:
        request.session["region"] = region
    return redirect("tickets:home")


def offers(request):
    return render(request, "tickets/offers.html", {"promo": booking.PROMO_CODE})


def giftcards(request):
    form = GiftCardForm(request.POST if request.method == "POST" else None)
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect(f"{reverse('tickets:login')}?next={reverse('tickets:giftcards')}")
        if form.is_valid():
            GiftCard.objects.create(
                purchaser=request.user, recipient=form.cleaned_data["recipient"],
                amount=form.cleaned_data["amount"], balance=form.cleaned_data["amount"],
            )
            messages.success(request, "Demo gift card created. Copy its code from your account.")
            return redirect("tickets:bookings")
    return render(request, "tickets/giftcards.html", {"form": form})


def inquiry(request, topic):
    title, description = INQUIRY_COPY[topic]
    initial = {}
    if request.user.is_authenticated:
        initial = {"name": request.user.first_name, "email": request.user.email}
    form = InquiryForm(request.POST if request.method == "POST" else None, initial=initial)
    if request.method == "POST" and form.is_valid():
        entry = form.save(commit=False)
        entry.topic = topic
        entry.save()
        messages.success(request, "Your message was saved. Reference BMSC-%04d." % entry.pk)
        return redirect(request.resolver_match.view_name)
    return render(request, "tickets/inquiry.html", {
        "title": title, "description": description, "topic": topic, "form": form,
    })


def about(request):
    return render(request, "tickets/about.html")


def newsletter(request):
    initial = {"email": request.user.email} if request.user.is_authenticated else None
    form = NewsletterForm(request.POST if request.method == "POST" else None, initial=initial)
    if request.method == "POST" and form.is_valid():
        _, created = NewsletterSubscription.objects.get_or_create(email=form.cleaned_data["email"])
        notice = "You’re signed up for the demo newsletter." if created else "This email is already on the list."
        messages.success(request, notice)
        return redirect("tickets:newsletter")
    return render(request, "tickets/newsletter.html", {"form": form})
