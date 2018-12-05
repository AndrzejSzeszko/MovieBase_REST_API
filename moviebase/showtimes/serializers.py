#!/usr/bin/python3.7
from rest_framework import serializers
from showtimes.models import (
    Cinema,
    Screening
)


class CinemaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cinema
        exclude = ['movies']


class ScreeningSerializer(serializers.ModelSerializer):

    class Meta:
        model = Screening
        fields = '__all__'
