from django.db import models
from movielist.models import Movie


class Cinema(models.Model):
    name = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    movies = models.ManyToManyField(Movie, through='Screening')

    def __str__(self):
        return self.name


class Screening(models.Model):
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE)
    screening_room = models.CharField(max_length=64, null=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    date = models.DateTimeField()

    def __str__(self):
        return f'{self.cinema}-{self.movie.title}-{self.date}'

    class Meta:
        unique_together = ['cinema', 'screening_room', 'date']
