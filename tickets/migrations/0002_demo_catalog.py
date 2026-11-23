from datetime import time

from django.db import migrations

VENUES = [
    ("lumen-picturehouse", "Lumen Picturehouse", "delhi", "Connaught Place, New Delhi", True),
    ("frame-cinema", "Frame Cinema", "gurugram", "Golf Course Road, Gurugram", True),
    ("the-screen-room", "The Screen Room", "noida", "Sector 18, Noida", True),
    ("courtyard-stage", "Courtyard Stage", "delhi", "Mehrauli, New Delhi", False),
    ("the-backroom", "The Backroom", "gurugram", "Sector 29, Gurugram", False),
    ("studio-nine", "Studio Nine", "delhi", "Mandi House, New Delhi", False),
    ("riverfront-grounds", "Riverfront Grounds", "delhi", "Mayur Vihar, New Delhi", False),
    ("arena-five", "Arena Five", "noida", "Sector 62, Noida", False),
    ("clay-house", "Clay House", "gurugram", "Sector 43, Gurugram", False),
    ("fairground-east", "Fairground East", "noida", "Sector 21, Noida", False),
]

LISTINGS = [
    ("whispers-of-the-monsoon", "Whispers of the Monsoon", "movies", "Drama", "Hindi", "2D", 124, "U/A 13+", 260, True,
     "When a downpour strands her in an old Delhi neighbourhood, a young radio producer follows a familiar voice through a city that remembers more than she does.",
     "Aditi Sen · Rohan Vaid · Directed by Mira Lal"),
    ("the-orbit-protocol", "The Orbit Protocol", "movies", "Sci-fi", "English", "IMAX", 138, "U/A 16+", 420, True,
     "A lone astronaut receives an impossible distress call from the dark side of a planet and has forty minutes to decide whether to answer it.",
     "Samira Rao · Daniel Cole · Directed by Leena Kapoor"),
    ("sunday-people", "Sunday People", "movies", "Comedy", "Hindi", "2D", 111, "U/A 13+", 240, True,
     "Four old friends reunite for a rooftop lunch. A broken lift, a missing cake and a confession turn their afternoon into the reunion they needed.",
     "Ishaan Mehra · Tara Joshi · Directed by Asha Dutt"),
    ("the-last-light", "The Last Light", "movies", "Adventure", "English", "2D", 105, "U", 300, True,
     "A photographer crosses an icy valley to capture the last sunset of the season and discovers why the village below keeps a light burning every night.",
     "Neel Arora · Hannah Bell · Directed by Dev Malik"),
    ("midnight-local", "Midnight Local", "movies", "Thriller", "Hindi", "2D", 119, "U/A 16+", 280, True,
     "A reporter boards the final train of the night and recognises every face on the carriage from an old missing-persons file.",
     "Rhea Das · Kabir Narang · Directed by Akhil Bedi"),
    ("the-last-light-short", "The Last Light: A Short", "stream", "Adventure", "English", "HD", 1, "U", 79, False,
     "A short visual study of the blue hour in a remote mountain valley. This original demo film is available for 48 hours after rental.",
     "A CurtainCall short"),
    ("neon-courtyard", "Neon Courtyard", "events", "Music", "Hindi / English", "Live", 150, "16+", 699, True,
     "An open-air evening of indie vocals, synths and live percussion at Mehrauli’s Courtyard Stage. Doors open thirty minutes before the set.", ""),
    ("just-one-more-joke", "Just One More Joke", "events", "Stand-up", "Hindi / English", "Live", 75, "18+", 399, True,
     "Three comics share new sets in a small club. Expect sharp observations, friendly crowd work and a rotating closing act.", ""),
    ("the-borrowed-room", "The Borrowed Room", "plays", "Drama", "Hindi", "Live", 95, "13+", 450, True,
     "Two tenants arrive with keys to the same room. Over one evening they begin to piece together the life of the person who lived there before them.", ""),
    ("city-after-dark", "City After Dark 5K", "sports", "Running", "English", "Entry", 90, "16+", 499, True,
     "A timed evening run on a flat riverside loop. Entry includes a race bib, hydration stops and a finisher’s medal.", ""),
    ("futsal-finals", "The Futsal Finals", "sports", "Football", "English", "Live", 90, "All ages", 299, False,
     "Watch the final two clubs in the local five-a-side league play for the season trophy in a covered arena.", ""),
    ("hands-in-clay", "Hands in Clay", "activities", "Workshop", "English / Hindi", "Workshop", 120, "12+", 899, False,
     "Learn to centre clay and throw a small bowl with a studio instructor. All materials are provided, and beginners are welcome.", ""),
    ("twilight-fair", "Twilight Fair", "activities", "Family", "Hindi / English", "Entry", 180, "All ages", 550, False,
     "Spend an evening under the fairground lights with a carousel, snack stalls and games for the whole family.", ""),
]

CINEMAS = ["lumen-picturehouse", "frame-cinema", "the-screen-room"]
OTHER_SHOWS = {
    "neon-courtyard": ("courtyard-stage", 19, 30),
    "just-one-more-joke": ("the-backroom", 20, 0),
    "the-borrowed-room": ("studio-nine", 18, 30),
    "city-after-dark": ("riverfront-grounds", 20, 30),
    "futsal-finals": ("arena-five", 18, 45),
    "hands-in-clay": ("clay-house", 15, 0),
    "twilight-fair": ("fairground-east", 17, 30),
}


def seed(apps, schema_editor):
    database = schema_editor.connection.alias
    venues = apps.get_model("tickets", "Venue").objects.using(database)
    listings = apps.get_model("tickets", "Listing").objects.using(database)
    shows = apps.get_model("tickets", "Showtime").objects.using(database)

    venue_ids = {}
    for slug, name, area, address, cinema in VENUES:
        venue = venues.create(slug=slug, name=name, area=area, address=address, cinema=cinema)
        venue_ids[slug] = venue.pk
    for index, data in enumerate(LISTINGS):
        slug, title, kind, genre, language, format_name, duration, age, price, featured, description, credits = data
        artwork = "the-last-light" if kind == "stream" else slug
        listing = listings.create(
            slug=slug, title=title, kind=kind, genre=genre, language=language, format=format_name,
            duration=duration, age=age, price=price, featured=featured,
            artwork=f"{artwork}.webp", description=description, credits=credits,
        )
        if kind == "movies":
            for offset, venue_slug in enumerate(CINEMAS):
                for hour, minutes in [(11 + 2 * offset + index % 2, 12 * index), (18 + offset + index % 2, 10 * index)]:
                    shows.create(listing_id=listing.pk, venue_id=venue_ids[venue_slug], time=time(hour, minutes))
        elif slug in OTHER_SHOWS:
            venue_slug, hour, minutes = OTHER_SHOWS[slug]
            shows.create(listing_id=listing.pk, venue_id=venue_ids[venue_slug], time=time(hour, minutes))


def unseed(apps, schema_editor):
    database = schema_editor.connection.alias
    slugs = [row[0] for row in LISTINGS]
    apps.get_model("tickets", "Showtime").objects.using(database).filter(listing__slug__in=slugs).delete()
    apps.get_model("tickets", "Listing").objects.using(database).filter(slug__in=slugs).delete()
    apps.get_model("tickets", "Venue").objects.using(database).filter(slug__in=[row[0] for row in VENUES]).delete()


class Migration(migrations.Migration):
    dependencies = [("tickets", "0001_initial")]
    operations = [migrations.RunPython(seed, unseed)]
