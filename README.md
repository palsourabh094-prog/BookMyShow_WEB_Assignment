# BookMyShow Clone

BookMyShow Clone is a Django mini project for discovering and booking fictional entertainment in Delhi-NCR. It follows the discovery, title, showtime and booking flow of the [BookMyShow Delhi-NCR reference](https://in.bookmyshow.com/explore/home/national-capital-region-ncr) with its own visual design, copy and artwork. The clone is an independent student project.

## Run locally

With Python 3.10 or newer installed, run these commands from the project directory.

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

On Windows PowerShell, activate with `.venv\Scripts\Activate.ps1`. Open [the Django homepage](http://127.0.0.1:8000/). The migrations create the SQLite schema and insert sample titles, venues and daily demo showtimes. Sign up through the site to try bookings. Use sample contact details.

The admin panel is available at `/admin/`. Run `python manage.py createsuperuser` if you want to edit the catalog or review inquiries.

## Pages and features

| Page | URL | What it does |
| --- | --- | --- |
| Home | `/` | Featured carousel, recommended movies, live categories, search, and the NCR area selector |
| Movies | `/explore/movies/` | Movie catalog with genre, language and format filters |
| Stream | `/explore/stream/` | Demo short film with a 48-hour rental |
| Events, Plays, Sports and Activities | `/explore/events/`, `/explore/plays/`, `/explore/sports/`, `/explore/activities/` | Separate browsable catalogs with detail pages |
| Search and cinema directory | `/search/`, `/cinemas/` | Search by title, venue, genre or language, or browse cinema-specific listings |
| Movie detail and showtimes | `/title/whispers-of-the-monsoon/`, `/title/whispers-of-the-monsoon/showtimes/` | Synopsis, credits, show dates and venue times |
| Seats and checkout | `/seats/<show-id>/<date>/`, `/checkout/` | Choose available seats and confirm a simulated order |
| Account and booking details | `/bookings/`, `/bookings/<reference>/` | View and download private receipts, or manage rentals and gift-card balances |
| Log in and Sign up | `/login/`, `/signup/` | Django session authentication, form validation and password hashing |
| Offers and Gift cards | `/offers/`, `/gift-cards/` | Enter `BMSDEMO10` at checkout or create and redeem a demo gift card |
| List your show, Corporates and Help | `/list-your-show/`, `/corporates/`, `/help/` | Submit inquiries saved in the local database |
| Newsletter | `/newsletter/` | Register a sample address and store it in the local database |
| About | `/about/` | Project description, demo terms and privacy details |

A typical journey is **Home → Movies → Movie detail → Showtimes → Seats → Log in or Sign up → Checkout → Confirmation**. The brand link returns to Home, and the two account forms link to each other while preserving the checkout destination.

All catalog and service pages share one template for navigation and the footer. POST forms use CSRF protection and server-side validation. The database prevents a seat from being reserved twice for the same show and date. Repeating a checkout confirmation returns the existing order.

## Project structure

- `curtaincall/` contains project settings, the root URL configuration and the WSGI entry point.
- `tickets/` contains models, views, forms, URLs, and booking logic.
- `tickets/migrations/` contains the schema and demo catalog.
- `tickets/templates/tickets/` contains the shared layout and page templates.
- `tickets/static/tickets/` contains CSS, JavaScript and WebP artwork.
- `tickets/media/` contains the silent demo short served to authenticated renters.
- `submission/` contains screenshots and the walkthrough.

The stack is Django 5.2, SQLite, HTML, CSS and a small amount of vanilla JavaScript. ImageGen produced the concert banner and the original poster art. The demo short pans across the fictional mountain scene from *The Last Light*.

The built-in ImageGen prompts requested an ultrawide night concert in New Delhi with open space for the headline, an eight-panel contact sheet for the rainy alley, red eclipse, rooftop reunion, blue glacier, indie gig, comedy club, theatre stage and night race, and a four-panel contact sheet for futsal, pottery, a carnival carousel and a night subway corridor. The expanded catalog used two more prompts. One requested a wide auditorium with rust-red velvet seats and warm projector light. The other requested an eight-panel contact sheet with a clockwork bird, glider pilots, a night train, rooftop jazz, two theatre scenes, tennis and a cyanotype workshop. The processed WebP files are in [the artwork directory](tickets/static/tickets/images/).

## Screenshots and walkthrough

[Home](submission/screenshots/01-home.png) · [Movies](submission/screenshots/02-movies.png) · [Movie detail](submission/screenshots/03-movie-detail.png) · [Log in](submission/screenshots/04-login.png) · [Sign up](submission/screenshots/05-sign-up.png) · [Seats](submission/screenshots/06-seat-selection.png) · [Booking confirmation](submission/screenshots/07-booking-confirmation.png) · [Mobile Home](submission/screenshots/08-mobile-home.png) · [Footer](submission/screenshots/09-footer.png)

[Watch the walkthrough](submission/bookmyshow-clone-walkthrough.mp4)

## Checks and demo scope

```sh
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
```

The listings, venues, showtimes, payment totals and credits are demonstration data. No payment gateway or external booking inventory is connected. Inquiry and newsletter forms save submissions locally for review in Django admin. The project records newsletter sign-ups without sending emails. Gift-card codes can be copied from the account page. A development-mode restart generates a new session signing key unless you supply `DJANGO_SECRET_KEY`, so the browser may need to log in again after a restart.
