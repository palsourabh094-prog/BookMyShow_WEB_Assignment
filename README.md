# BookMyShow Django Mini Project

The runnable Django project is in [BookMyShow_Django_Complete 2](BookMyShow_Django_Complete%202/).
It includes Home, Movies, Events, catalog details, About, Sign In, and Sign Up.

From this directory, run:

```sh
cd "BookMyShow_Django_Complete 2"
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py add_sample_data
python manage.py runserver
```

Open [BookMyShow on localhost](http://127.0.0.1:8000/). The [project README](BookMyShow_Django_Complete%202/README.txt)
contains the assignment checklist, navigation flow, page URLs, and testing commands.
The updated screenshots and walkthrough are in the [submission folder](BookMyShow_Django_Complete%202/submission/).
