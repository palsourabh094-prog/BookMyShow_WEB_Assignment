import uuid

from django.conf import settings
from django.db import models


class Venue(models.Model):
    class Area(models.TextChoices):
        DELHI = "delhi", "New Delhi"
        GURUGRAM = "gurugram", "Gurugram"
        NOIDA = "noida", "Noida"

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    area = models.CharField(max_length=20, choices=Area)
    address = models.CharField(max_length=160)
    cinema = models.BooleanField(default=False)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Listing(models.Model):
    class Kind(models.TextChoices):
        MOVIES = "movies", "Movies"
        STREAM = "stream", "Stream"
        EVENTS = "events", "Events"
        PLAYS = "plays", "Plays"
        SPORTS = "sports", "Sports"
        ACTIVITIES = "activities", "Activities"

    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    kind = models.CharField(max_length=15, choices=Kind)
    genre = models.CharField(max_length=50)
    language = models.CharField(max_length=35)
    format = models.CharField(max_length=20)
    description = models.TextField()
    duration = models.PositiveSmallIntegerField(help_text="Minutes")
    age = models.CharField(max_length=15)
    price = models.PositiveIntegerField(help_text="Rupees")
    artwork = models.CharField(max_length=120, help_text="Static path under tickets/images")
    featured = models.BooleanField(default=False)
    credits = models.CharField(max_length=180, blank=True)

    class Meta:
        ordering = ["id"]

    @property
    def image(self):
        return f"tickets/images/{self.artwork}"

    def __str__(self):
        return self.title


class Showtime(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.PROTECT, related_name="showtimes")
    venue = models.ForeignKey(Venue, on_delete=models.PROTECT, related_name="showtimes")
    time = models.TimeField()

    class Meta:
        ordering = ["time", "id"]
        constraints = [
            models.UniqueConstraint(fields=["listing", "venue", "time"], name="unique_showtime"),
            models.UniqueConstraint(fields=["venue", "time"], name="unique_venue_time"),
        ]

    def __str__(self):
        return f"{self.listing} at {self.venue}, {self.time:%H:%M}"


class Booking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.PROTECT)
    showtime = models.ForeignKey(Showtime, on_delete=models.PROTECT, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    total = models.PositiveIntegerField()
    discount = models.PositiveIntegerField(default=0)
    gift_credit = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.listing} ({str(self.id)[:8]})"


class ReservedSeat(models.Model):
    booking = models.ForeignKey(Booking, related_name="seats", on_delete=models.CASCADE)
    showtime = models.ForeignKey(Showtime, on_delete=models.PROTECT)
    date = models.DateField()
    label = models.CharField(max_length=4)

    class Meta:
        ordering = ["label"]
        constraints = [
            models.UniqueConstraint(fields=["showtime", "date", "label"], name="unique_reserved_seat"),
        ]


class GiftCard(models.Model):
    code = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    purchaser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    recipient = models.CharField(max_length=100)
    amount = models.PositiveIntegerField()
    balance = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Gift for {self.recipient}"


class Inquiry(models.Model):
    class Topic(models.TextChoices):
        ORGANIZER = "list-your-show", "List Your Show"
        CORPORATE = "corporates", "Corporates"
        SUPPORT = "help", "Help"

    topic = models.CharField(max_length=30, choices=Topic)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=120)
    message = models.TextField(max_length=1500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject


class NewsletterSubscription(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
