# BookMyShow — Django Web Application Mini Project

| Student details | Fill in before submission |
| --- | --- |
| Name | [Student name] |
| Roll number | [Roll number] |
| Section | [Section] |

## Objective and reference

BookMyShow is a movie and live-event discovery site built with Django. It uses
the BookMyShow ticketing site as a reference for the landing page structure, including a promotion,
movie cards, and event categories. BookMyShow is an independent academic project
with a text wordmark and student-built styling.

The project demonstrates Django views and URL routing, template inheritance,
static files, SQLite-backed catalog pages, and Django account forms.

## Features and page URLs

| Page | Local path | Features |
| --- | --- | --- |
| Home | `/` | Hero banner, recommended movies, live-event categories, premieres, and music listings |
| Movies | `/movies/` | Movie cards and search by title, genre, or language |
| Movie detail | `/movies/<id>/` | Title, poster, synopsis, genre, language, duration, release date, and rating |
| Events | `/events/` | Event cards and filters for title, category, or city |
| Event detail | `/events/<id>/` | Category, venue, city, date, price, and description |
| About | `/about/` | Project purpose and theme |
| Sign in | `/login/` | Username and password, validation feedback, and a Sign Up link |
| Sign up | `/signup/` | Name, email, username, password, confirmation, and a Sign In link |
| Sign out | `/logout/` | Authenticated POST action from the header or footer |
| Django admin | `/admin/` | Catalog management for staff accounts |

All public pages share the header and footer. The header search goes to Movies,
and the event category cards open filtered Events listings. Registration creates
a Django user and starts a session. Django hashes passwords, and all account
POST forms use CSRF protection.

## Navigation flow

- Home → Explore Movies → Movies → Movie detail → Back to Movies
- Home → Events or an event category → Events → Event detail → Back to Events
- Header → About
- Header → Sign in → Sign up → Sign in
- Any public page → BookMyShow wordmark or Home → Home

## Technologies and structure

Python, Django, SQLite, Django templates, HTML, CSS, and vanilla JavaScript.

```text
manage.py
requirements.txt
config/                   Django settings and root URL configuration
website/
  urls.py                 Named page routes
  views.py                Catalog and account views
  forms.py                Registration form
  models.py               Movie and Event models
  migrations/             SQLite schema migrations
  management/commands/    add_sample_data command
  templates/website/      Public page templates and shared base layout
  static/website/         CSS and catalog image fallback script
  tests.py                Account validation and session tests
submission/               Current screenshots and walkthrough
```

## Run locally

Run from the directory containing `manage.py`. Use Python 3.12 or newer.

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py add_sample_data
python manage.py runserver
```

On Windows PowerShell, activate with `.venv\Scripts\Activate.ps1`.
Open `http://127.0.0.1:8000/`. Migrations create a local SQLite database, and
`add_sample_data` creates or refreshes the demo catalog. To manage the catalog
through Django admin, run `python manage.py createsuperuser` and open `/admin/`.

The development server generates a temporary signing key unless
`DJANGO_SECRET_KEY` is set as an environment variable. Either sign in again
after a restart or set a private development key outside the repository.
When `DJANGO_DEBUG=0`, a key must be supplied. For submission, include the
migrations and leave local databases, virtual environments, and credentials out.

## Assignment checklist and evidence

| Guideline | Where to verify |
| --- | --- |
| 1. Objective and theme | Objective above and About page |
| 2. Mandatory pages | Home, Movies, Events, Sign In, and Sign Up |
| 3–4. Page linking and example flow | Navigation flow above, clickable cards, account cross-links, and Home links |
| 5. Shared header and footer | `website/templates/website/base.html` and all public page screenshots |
| 6–7. Django and project structure | Named URLs, views, inherited templates, static assets, and migration files |
| 8. UI and design | Desktop screenshots and mobile Home screenshot |
| 9. Account forms | Labeled Django forms, server-side validation, password hashing, and CSRF checks |
| 10. Testing | Django system and migration checks, account tests, and desktop/mobile browser click-through |
| 11–12. Submission and report | Project directory, this README, screenshots, walkthrough, and migrations |
| 13. Evaluation | The pages, navigation flow, checks, and submission evidence listed here |

```sh
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
```

The current submission screenshots are in `submission/screenshots/`:

- `01-home.png`, `02-movies.png`, and `04-events.png` cover the three required content pages.
- `07-sign-in.png` and `08-sign-up.png` cover the required account pages.
- `03-movie-detail.png`, `05-event-detail.png`, `06-about.png`, and
  `09-mobile-home.png` show additional routes and the mobile layout.

`submission/bookmyshow-walkthrough.webm` opens the site and shows the content
and account pages connected through visible links.

## Known limitations

The catalog is sample data. The site provides discovery and accounts. Ticket
sales, payments, and video playback are outside its scope. Movie and event
images with external URLs depend on the source host. An unavailable image
displays a title card. Confirm the instructor's submission format and destination,
then add your student details before submitting.
