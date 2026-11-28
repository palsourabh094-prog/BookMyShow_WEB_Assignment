from datetime import date
from django.core.management.base import BaseCommand
from website.models import Movie, Event


class Command(BaseCommand):
    help = "Add sample movies and live events to the CineBook database"

    def handle(self, *args, **options):
        movies = [
            {
                "title": "Dune: Part Two", "genre": "Sci-Fi / Adventure",
                "language": "English", "duration": 166,
                "release_date": date(2024, 3, 1), "rating": 8,
                "poster_url": "https://image.tmdb.org/t/p/w500/1pdfLvkbY9ohJlCjQH2CZjjYVvJ.jpg",
                "description": "Paul Atreides unites with the Fremen on a journey of destiny."
            },
            {
                "title": "Oppenheimer", "genre": "Drama / History",
                "language": "English", "duration": 180,
                "release_date": date(2023, 7, 21), "rating": 8,
                "poster_url": "https://image.tmdb.org/t/p/w500/ptpr0kGAckfQkJeJIt8st5dglvd.jpg",
                "description": "The story of J. Robert Oppenheimer and the development of the atomic bomb."
            },
            {
                "title": "Interstellar", "genre": "Sci-Fi / Drama",
                "language": "English", "duration": 169,
                "release_date": date(2014, 11, 7), "rating": 9,
                "poster_url": "https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg",
                "description": "A team travels beyond this galaxy to discover whether mankind has a future among the stars."
            },
            {
                "title": "Spider-Man: Across the Spider-Verse", "genre": "Animation / Action",
                "language": "English", "duration": 140,
                "release_date": date(2023, 6, 2), "rating": 9,
                "poster_url": "https://image.tmdb.org/t/p/w500/8Vt6mWEReuy4Of61Lnj5Xj704m8.jpg",
                "description": "Miles Morales travels across the multiverse and meets a team of Spider-People."
            },
            {
                "title": "Inside Out 2", "genre": "Animation / Family",
                "language": "English", "duration": 96,
                "release_date": date(2024, 6, 14), "rating": 8,
                "poster_url": "https://image.tmdb.org/t/p/w500/vpnVM9B6NMmQpWeZvzLvDESb2QY.jpg",
                "description": "Riley enters her teenage years as new emotions arrive at headquarters."
            },
            {
                "title": "Jawan", "genre": "Action / Thriller",
                "language": "Hindi", "duration": 169,
                "release_date": date(2023, 9, 7), "rating": 7,
                "poster_url": "",
                "description": "A man driven by a personal mission takes on corruption and injustice."
            },
            {
                "title": "The Batman", "genre": "Action / Crime",
                "language": "English", "duration": 176,
                "release_date": date(2022, 3, 4), "rating": 8,
                "poster_url": "https://image.tmdb.org/t/p/w500/74xTEgt7R36Fpooo50r9T25onhq.jpg",
                "description": "Batman investigates a series of crimes that reveal corruption in Gotham."
            },
            {
                "title": "La La Land", "genre": "Romance / Musical",
                "language": "English", "duration": 128,
                "release_date": date(2016, 12, 9), "rating": 8,
                "poster_url": "",
                "description": "A jazz musician and an aspiring actor fall in love while pursuing their dreams."
            },
        ]

        events = [
            {
                "title": "Live Music Night", "category": "Music",
                "city": "Delhi", "venue": "Venue Arena, Delhi",
                "event_date": date(2026, 12, 12), "price": 799,
                "image_url": "https://images.unsplash.com/photo-1501386761578-eac5c94b800a?w=900",
                "description": "An evening of live music, great energy and unforgettable performances."
            },
            {
                "title": "The Comedy Club", "category": "Comedy",
                "city": "Gurugram", "venue": "Studio X, Gurugram",
                "event_date": date(2026, 12, 19), "price": 499,
                "image_url": "",
                "description": "A live stand-up comedy show featuring fresh jokes and big laughs."
            },
            {
                "title": "City Food Festival", "category": "Food & Drinks",
                "city": "Noida", "venue": "Central Park, Noida",
                "event_date": date(2027, 1, 10), "price": 299,
                "image_url": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=900",
                "description": "Explore food stalls, new flavours and fun activities."
            },
            {
                "title": "Sunset Music Festival", "category": "Festival",
                "city": "Delhi", "venue": "Garden Grounds, Delhi",
                "event_date": date(2027, 1, 24), "price": 999,
                "image_url": "https://images.unsplash.com/photo-1459749411175-04bf5292ceea?w=900",
                "description": "Enjoy an outdoor music festival with live performances."
            },
            {
                "title": "Stage Lights", "category": "Theatre",
                "city": "Delhi", "venue": "Studio Theatre, Delhi",
                "event_date": date(2027, 2, 6), "price": 599,
                "description": "An ensemble performs three short plays about life in the city.",
            },
            {
                "title": "Winter Fun Fair", "category": "Amusement",
                "city": "Noida", "venue": "Riverside Fairgrounds, Noida",
                "event_date": date(2027, 2, 13), "price": 450,
                "description": "Spend an afternoon exploring rides, games and family activities.",
            },
            {
                "title": "Printmaking Basics", "category": "Workshop",
                "city": "Gurugram", "venue": "Open Studio, Gurugram",
                "event_date": date(2027, 2, 20), "price": 850,
                "description": "Learn to carve a design, ink a block and print your own artwork.",
            },
        ]

        for item in movies:
            Movie.objects.update_or_create(title=item["title"], defaults=item)
        for item in events:
            Event.objects.update_or_create(title=item["title"], defaults=item)

        self.stdout.write(self.style.SUCCESS(
            f"Sample data ready: {len(movies)} movies and {len(events)} events."
        ))
