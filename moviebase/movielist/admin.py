from django.contrib import admin
from .models import (
    Movie,
    Person
)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    pass


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    pass
