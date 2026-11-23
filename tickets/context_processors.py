from .models import Listing, Venue


def navigation(request):
    region = request.session.get("region", "")
    return {
        "nav_categories": Listing.Kind.choices,
        "region_choices": [("", "Delhi-NCR"), *Venue.Area.choices],
        "region": region,
        "region_label": dict(Venue.Area.choices).get(region, "Delhi-NCR"),
    }
