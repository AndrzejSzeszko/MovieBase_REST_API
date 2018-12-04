from django.contrib import admin
from .models import (
    Movie,
    Person
)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Movie._meta.fields if field.name != 'id']


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Person._meta.fields if field.name != 'id']
