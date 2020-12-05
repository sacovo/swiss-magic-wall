"""
Admin for Geographic objects
"""
from django.contrib import admin

from geo import models

# Register your models here.


@admin.register(models.Kanton)
class KantonAdmin(admin.ModelAdmin):
    """
    Admin for the kantons
    """

    list_display = ["name", "geo_id"]
    search_fields = ["name"]
    readonly_fields = ["geo_id"]


@admin.register(models.Gemeinde)
class GemeindeAdmin(admin.ModelAdmin):
    """
    Admin for gemeinden
    """

    list_display = ["name", "geo_id", "kanton"]
    search_fields = ["name", "kanton"]

    list_filter = ["kanton"]
    readonly_fields = ["geo_id"]
