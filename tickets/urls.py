from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from . import views
from .forms import LoginForm

app_name = "tickets"

urlpatterns = [
    path("", views.home, name="home"),
    path("explore/<slug:kind>/", views.catalog, name="catalog"),
    path("search/", views.catalog, name="search"),
    path("title/<slug:slug>/", views.detail, name="detail"),
    path("title/<slug:slug>/showtimes/", views.showtimes, name="showtimes"),
    path("title/<slug:slug>/rent/", views.rent, name="rent"),
    path("cinemas/", views.cinemas, name="cinemas"),
    path("cinemas/<slug:slug>/", views.venue_detail, name="cinema"),
    path("seats/<int:show_id>/<str:day>/", views.seats, name="seats"),
    path("checkout/", views.checkout, name="checkout"),
    path("bookings/", views.bookings, name="bookings"),
    path("bookings/<uuid:pk>/", views.confirmation, name="confirmation"),
    path("bookings/<uuid:pk>/receipt/", views.download_receipt, name="download_receipt"),
    path("bookings/<uuid:pk>/watch/", views.watch, name="watch"),
    path("bookings/<uuid:pk>/media/", views.stream_media, name="stream_media"),
    path("login/", auth_views.LoginView.as_view(
        template_name="tickets/login.html", authentication_form=LoginForm,
        next_page=reverse_lazy("tickets:home"), redirect_authenticated_user=True,
    ), name="login"),
    path("signup/", views.signup, name="signup"),
    path("logout/", auth_views.LogoutView.as_view(next_page=reverse_lazy("tickets:home")), name="logout"),
    path("region/", views.set_region, name="region"),
    path("offers/", views.offers, name="offers"),
    path("gift-cards/", views.giftcards, name="giftcards"),
    path("list-your-show/", views.inquiry, {"topic": "list-your-show"}, name="list_show"),
    path("corporates/", views.inquiry, {"topic": "corporates"}, name="corporates"),
    path("help/", views.inquiry, {"topic": "help"}, name="help"),
    path("about/", views.about, name="about"),
    path("newsletter/", views.newsletter, name="newsletter"),
]
