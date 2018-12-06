#!/usr/bin/python3.7
from rest_framework import serializers
from movielist.models import Movie
from showtimes.models import (
    Cinema,
    Screening
)


class CinemaSerializer(serializers.ModelSerializer):
    movies = serializers.HyperlinkedRelatedField(
        view_name='movie-detail',
        read_only=True,
        many=True,
        allow_null=True
    )

    class Meta:
        model = Cinema
        fields = '__all__'


class ScreeningSerializer(serializers.ModelSerializer):
    cinema = serializers.SlugRelatedField(slug_field='name', queryset=Cinema.objects.all())
    movie = serializers.SlugRelatedField(slug_field='title', queryset=Movie.objects.all())

    class Meta:
        model = Screening
        fields = '__all__'
