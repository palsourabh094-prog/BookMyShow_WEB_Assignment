from django.contrib import admin
from .models import Movie, Event

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "genre", "language", "release_date", "rating")
    search_fields = ("title", "genre", "language")
    list_filter = ("genre", "language")

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "city", "event_date", "price")
    search_fields = ("title", "category", "city")
    list_filter = ("category", "city")
