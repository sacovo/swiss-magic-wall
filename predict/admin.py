"""
administration for prediction
"""
from django.contrib import admin, messages
from django.utils.translation import gettext as _

from predict import models


@admin.register(models.VotingModel)
class VotingModelAdmin(admin.ModelAdmin):
    """
    Admin for a voting model
    """

    search_fields = ["votation__votation_title__name"]

    actions = ["build_projection_matrix"]

    filter_horizontal = ['model_votations']

    def build_projection_matrix(self, request, queryset):
        """
        Build the projection matrix
        """
        for model in queryset:
            model.build_projection_matrix()
        self.message_user(request, _(f"built matrices for {len(queryset)} models"), messages.SUCCESS)

    build_projection_matrix.short_description = _("build the projection matrices")


@admin.register(models.Result, models.LatestResult)
class ResultAdmin(admin.ModelAdmin):
    """
    Admin for a result
    """

    search_fields = ["gemeinde__name"]

    list_filter = ['gemeinde__kanton', 'votation']
    list_display = ["gemeinde", "timestamp", "votation", "yes_percent", "is_final"]
