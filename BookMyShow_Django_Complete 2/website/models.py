from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    language = models.CharField(max_length=50)
    duration = models.IntegerField()
    release_date = models.DateField()
    rating = models.IntegerField(default=0)
    poster_url = models.URLField(blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class Event(models.Model):
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=80)
    city = models.CharField(max_length=80)
    venue = models.CharField(max_length=150)
    event_date = models.DateField()
    price = models.IntegerField(default=0)
    image_url = models.URLField(blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title
