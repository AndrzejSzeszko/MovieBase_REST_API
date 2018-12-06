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


class ScreeningView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Screening.objects.all()
    serializer_class = ScreeningSerializer
