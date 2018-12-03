from django.contrib import admin
from .models import (
    Cinema,
    Screening
)


@admin.register(Cinema)
class CinemaAdmin(admin.ModelAdmin):
    pass


@admin.register(Screening)
class ScreeningAdmin(admin.ModelAdmin):
    pass
