

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from django.views.decorators.http import require_POST

from .forms import SignUpForm
from .models import Movie, Event


MUSIC_EVENTS = (
    Q(category__icontains="music")
    | Q(category__icontains="concert")
    | Q(title__icontains="music")
    | Q(title__icontains="concert")
)


# ---------------- HOME PAGE ----------------

def home(request):
    movies = Movie.objects.all().order_by('-release_date')[:8]

    premieres = Movie.objects.all().order_by('-release_date')[:5]

    music_events = Event.objects.filter(MUSIC_EVENTS).order_by('event_date')[:5]

    context = {
        'movies': movies,
        'premieres': premieres,
        'music_events': music_events,
    }

    return render(request, 'website/home.html', context)


# ---------------- MOVIES PAGE ----------------

def movies(request):
    search = request.GET.get('search', '').strip()

    all_movies = Movie.objects.all()

    if search:
        all_movies = all_movies.filter(
            Q(title__icontains=search) |
            Q(genre__icontains=search) |
            Q(language__icontains=search)
        )

    context = {
        'movies': all_movies.order_by('-release_date'),
        'search': search,
    }

    return render(request, 'website/movies.html', context)


# ---------------- MOVIE DETAIL PAGE ----------------

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    return render(
        request,
        'website/movie_detail.html',
        {'movie': movie}
    )


# ---------------- EVENTS PAGE ----------------

def events(request):
    search = request.GET.get('search', '').strip()

    all_events = Event.objects.all()

    if search:
        category = search.lower()

        if category in ['comedy']:
            all_events = all_events.filter(
                Q(category__icontains='comedy') |
                Q(title__icontains='comedy')
            )

        elif category in ['amusement park', 'fun & amusement', 'amusement']:
            all_events = all_events.filter(
                Q(category__icontains='amusement') |
                Q(category__icontains='fun') |
                Q(title__icontains='amusement') |
                Q(title__icontains='fun')
            )

        elif category in ['theatre', 'theater']:
            all_events = all_events.filter(
                Q(category__icontains='theatre') |
                Q(category__icontains='theater') |
                Q(title__icontains='theatre') |
                Q(title__icontains='theater')
            )

        elif category in ['music', 'concert']:
            all_events = all_events.filter(MUSIC_EVENTS)

        elif category in ['workshops', 'workshop']:
            all_events = all_events.filter(
                Q(category__icontains='workshop') |
                Q(title__icontains='workshop')
            )

        elif category in ['gurgaon', 'gurugram']:
            all_events = all_events.filter(city__in=['Gurgaon', 'Gurugram'])

        else:
            all_events = all_events.filter(
                Q(title__icontains=search) |
                Q(category__icontains=search) |
                Q(city__icontains=search)
            )

    all_events = all_events.order_by('event_date', 'pk')

    context = {
        'events': all_events,
        'search': search,
    }

    return render(request, 'website/events.html', context)


# ---------------- EVENT DETAIL PAGE ----------------

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    return render(
        request,
        'website/event_detail.html',
        {'event': event}
    )


# ---------------- ABOUT PAGE ----------------

def about(request):
    return render(request, 'website/about.html')


def signup_view(request):
    form = SignUpForm(request.POST if request.method == "POST" else None)
    if form.is_valid():
        login(request, form.save())
        messages.success(request, "Account created successfully.")
        return redirect("home")
    return render(request, "website/signup.html", {"form": form})


def login_view(request):
    form = AuthenticationForm(
        request, data=request.POST if request.method == "POST" else None
    )
    if form.is_valid():
        login(request, form.get_user())
        messages.success(request, "Signed in successfully.")
        return redirect("home")
    return render(request, "website/login.html", {"form": form})


@require_POST
def logout_view(request):
    logout(request)
    messages.success(request, "You have been signed out.")
    return redirect("home")
