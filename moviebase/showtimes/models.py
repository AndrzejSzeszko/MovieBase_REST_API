from django.db import models
from movielist.models import Movie


class Cinema(models.Model):
    name = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    movies = models.ManyToManyField(Movie, through='Screening')


class Screening(models.Model):
    cinema = models.ForeignKey(Cinema, on_delete=models.SET_NULL, null=True)
    movie = models.ForeignKey(Movie, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField()
