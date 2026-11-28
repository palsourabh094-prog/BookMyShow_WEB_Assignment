from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("movies/", views.movies, name="movies"),
    path("movies/<int:movie_id>/", views.movie_detail, name="movie_detail"),
    path("events/", views.events, name="events"),
    path("events/<int:event_id>/", views.event_detail, name="event_detail"),
    path("about/", views.about, name="about"),
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
    path("logout/", views.logout_view, name="logout"),
]
