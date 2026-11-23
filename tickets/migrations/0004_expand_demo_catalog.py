from datetime import time

from django.db import migrations


CINEMAS = ["lumen-picturehouse", "frame-cinema", "the-screen-room"]
ADDITIONS = [
    ("the-clockwork-garden", "The Clockwork Garden", "movies", "Fantasy", "Hindi", "2D", 108, "U", 240,
     "A child repairs a mechanical bird in a shuttered conservatory and finds a garden that wakes up after dark.",
     [(venue, 10, 10) for venue in CINEMAS]),
    ("paper-skies", "Paper Skies", "movies", "Adventure", "English", "2D", 117, "U/A 13+", 290,
     "Two glider pilots take on a long-distance flight to finish a route their instructor started decades ago.",
     [(venue, 16, 5) for venue in CINEMAS]),
    ("between-stations", "Between Stations", "movies", "Romance", "Hindi", "2D", 115, "U/A 13+", 260,
     "Strangers on the last train out of Delhi exchange handwritten notes as their journeys take an unexpected turn.",
     [(venue, 21, 20) for venue in CINEMAS]),
    ("brass-at-sundown", "Brass at Sundown", "events", "Jazz", "Instrumental", "Live", 90, "All ages", 649,
     "A rooftop jazz set with a brass trio and live percussion as the city lights come on.",
     [("courtyard-stage", 17, 45), ("the-backroom", 18, 0)]),
    ("letters-from-old-delhi", "Letters from Old Delhi", "plays", "Drama", "Hindi", "Live", 85, "13+", 499,
     "An actor brings a box of forgotten letters to life, tracing one neighbourhood through three generations.",
     [("studio-nine", 16, 30), ("the-backroom", 15, 0)]),
    ("the-quiet-kitchen", "The Quiet Kitchen", "plays", "Comedy", "Hindi / English", "Live", 80, "12+", 399,
     "Two siblings try to recreate a family recipe before dinner service in this intimate stage comedy.",
     [("studio-nine", 20, 15), ("fairground-east", 19, 15)]),
    ("baseline-open", "Baseline Open", "sports", "Tennis", "English", "Live", 120, "All ages", 349,
     "Watch local singles and doubles players compete on centre court in an evening tournament.",
     [("arena-five", 16, 15), ("riverfront-grounds", 17, 45)]),
    ("cyanotype-club", "Cyanotype Club", "activities", "Workshop", "English / Hindi", "Workshop", 105, "12+", 749,
     "Use sunlight, paper and botanical cuttings to make your own blue photographic prints.",
     [("clay-house", 11, 30), ("courtyard-stage", 12, 30)]),
]


def seed(apps, schema_editor):
    alias = schema_editor.connection.alias
    listings = apps.get_model("tickets", "Listing").objects.using(alias)
    venues = apps.get_model("tickets", "Venue").objects.using(alias)
    showtimes = apps.get_model("tickets", "Showtime").objects.using(alias)
    listings.filter(slug="the-last-light-short", credits="A CurtainCall short").update(credits="An original demo short")
    venue_ids = dict(venues.values_list("slug", "pk"))

    for slug, title, kind, genre, language, format_name, duration, age, price, description, slots in ADDITIONS:
        listing, created = listings.get_or_create(slug=slug, defaults={
            "title": title, "kind": kind, "genre": genre, "language": language, "format": format_name,
            "duration": duration, "age": age, "price": price, "description": description, "artwork": f"{slug}.webp",
        })
        if created:
            for venue_slug, hour, minute in slots:
                if venue_slug in venue_ids:
                    showtimes.get_or_create(
                        venue_id=venue_ids[venue_slug], time=time(hour, minute), defaults={"listing_id": listing.pk},
                    )


class Migration(migrations.Migration):
    dependencies = [("tickets", "0003_newslettersubscription")]
    # Keep catalog entries on rollback because existing orders can reference them.
    operations = [migrations.RunPython(seed, migrations.RunPython.noop)]
