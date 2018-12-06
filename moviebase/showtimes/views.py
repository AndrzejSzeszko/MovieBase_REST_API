from showtimes.models import (
    Cinema,
    Screening,
)
from showtimes.serializers import (
    CinemaSerializer,
    CinemaWithMoviesPlayedInNearest30DaysSerializer,
    ScreeningSerializer
)
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend


class CinemaListView(generics.ListCreateAPIView):
    queryset = Cinema.objects.all()
    serializer_class = CinemaSerializer


class CinemaWithMoviesPlayedInNearest30DaysView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cinema.objects.all()
    serializer_class = CinemaWithMoviesPlayedInNearest30DaysSerializer


class CinemaView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cinema.objects.all()
    serializer_class = CinemaSerializer


class ScreeningListView(generics.ListCreateAPIView):
    queryset = Screening.objects.all()
    serializer_class = ScreeningSerializer
    filter_fields = ('cinema__name', 'movie__title')


class ScreeningView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Screening.objects.all()
    serializer_class = ScreeningSerializer
