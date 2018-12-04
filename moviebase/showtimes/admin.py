from django.contrib import admin
from .models import (
    Cinema,
    Screening
)


@admin.register(Cinema)
class CinemaAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Cinema._meta.fields if field.name != 'id']


@admin.register(Screening)
class ScreeningAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Screening._meta.fields if field.name != 'id']
