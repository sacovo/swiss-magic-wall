from predict.models import LatestResult, Result
from django.contrib import admin, messages
from django.utils.translation import gettext as _
from django.shortcuts import redirect, reverse

# Register your models here.
from votes import models, tasks


@admin.register(models.VotationDate)
class VotationDateAdmin(admin.ModelAdmin):
    """
    admin for votation date
    """

    list_display = ["start_date", "json_url", "is_finished"]
    date_hierarchy = "start_date"

    actions = ["init_votations", "reset_votations"]

    def init_votations(self, request, queryset):
        """
        Starts a celery task to fetch the votations
        """
        for votation_date in queryset:
            tasks.init_votations.delay(votation_date.pk)
        self.message_user(
            request,
            _(f"started fetching for {len(queryset)} votation dates"),
            messages.SUCCESS,
        )

    def reset_votations(self, request, queryset):

        for date in queryset:
            LatestResult.objects.filter(votation__date__id=date.id).delete()
            Result.objects.filter(votation__date__id=date.id).delete()
            tasks.init_votations.delay(date.id)



    init_votations.short_description = _("init votations")


class VotationTitleInline(admin.TabularInline):
    """
    Inline for votation title translation
    """

    model = models.VotationTitle
    fields = ["language_code", "title"]
    extra = 0


@admin.register(models.Votation)
class VotationAdmin(admin.ModelAdmin):
    """
    admin for a single votation
    """

    list_display = ["__str__", "date", "is_finished", "needs_staende", "is_accepted"]
    search_fields = ["translation_title_set__name"]
    list_filter = ["tags"]

    inlines = [VotationTitleInline]

    actions = ["model_based_on_selection"]

    def model_based_on_selection(self, request, queryset):
        pk_query = "?model_votations=" + ",".join(
            str(x) for x in queryset.values_list("id", flat=True))

        return redirect(reverse("admin:predict_votingmodel_add") + pk_query)
