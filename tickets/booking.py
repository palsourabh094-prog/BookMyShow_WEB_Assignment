from datetime import date, datetime, timedelta
from uuid import UUID

from django.db import transaction
from django.db.models import F
from django.utils import timezone

from .models import Booking, GiftCard, ReservedSeat

SEAT_ROWS = [[f"{row}{number}" for number in range(1, 11)] for row in "ABCDEF"]
SEAT_LABELS = {label for row in SEAT_ROWS for label in row}
WINDOW_DAYS = 7
RENTAL_HOURS = 48
PROMO_CODE = "BMSDEMO10"


def booking_days():
    today = timezone.localdate()
    return [today + timedelta(days=index) for index in range(WINDOW_DAYS)]


def parse_day(value):
    try:
        day = date.fromisoformat(value)
    except (TypeError, ValueError):
        return None
    return day if day in booking_days() else None


def future(showtime, day):
    return datetime.combine(day, showtime.time) > timezone.localtime().replace(tzinfo=None)


def taken_seats(showtime, day):
    return set(ReservedSeat.objects.filter(showtime=showtime, date=day).values_list("label", flat=True))


class BookingError(Exception):
    def __init__(self, message, field=None):
        super().__init__(message)
        self.field = field


@transaction.atomic
def confirm_booking(*, user, listing, showtime, day, labels, draft_id, promo, gift_code):
    existing = Booking.objects.filter(id=draft_id, user=user).first()
    if existing:
        return existing
    if showtime:
        if not future(showtime, day):
            raise BookingError("This showtime has already started.")
        if taken_seats(showtime, day).intersection(labels):
            raise BookingError("One of those seats is now unavailable. Choose your seats again.")

    subtotal = listing.price * (len(labels) if showtime else 1)
    discount = 0
    if promo:
        if promo.upper() not in {PROMO_CODE, "CURTAIN10"}:
            raise BookingError("Enter a valid offer code.", "promo")
        discount = min(subtotal // 10, 100)
    due = subtotal - discount
    credit = 0
    if gift_code:
        card = GiftCard.objects.select_for_update().filter(code=gift_code, balance__gt=0).first()
        if card is None:
            raise BookingError("This gift card is invalid or has no balance.", "gift_code")
        credit = min(card.balance, due)
        GiftCard.objects.filter(pk=card.pk).update(balance=F("balance") - credit)

    booking = Booking.objects.create(
        id=UUID(draft_id), user=user, listing=listing, showtime=showtime,
        date=day, total=due - credit, discount=discount, gift_credit=credit,
    )
    if showtime:
        ReservedSeat.objects.bulk_create([
            ReservedSeat(booking=booking, showtime=showtime, date=day, label=label) for label in labels
        ])
    return booking
