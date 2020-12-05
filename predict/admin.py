"""
administration for prediction
"""
from django.contrib import admin

from predict import models


@admin.register(models.VotingModel)
class VotingModelAdmin(admin.ModelAdmin):
    """
    Admin for a voting model
    """

    search_fields = ["votation__votation_title__name"]


@admin.register(models.Result)
class ResultAdmin(admin.ModelAdmin):
    """
    Admin for a result
    """

    list_display = [
        "gemeinde", "timestamp", "votation", "yes_percent", "is_final"
    ]
