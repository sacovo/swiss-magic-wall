from django.contrib import admin

# Register your models here.
from votes import models, tasks


@admin.register(models.VotationDate)
class VotationDateAdmin(admin.ModelAdmin):
    """
    admin for votation date
    """

    list_display = ["start_date", "json_url"]
    date_hierarchy = "start_date"

    def init_votations(self, queryset):
        """
        Starts a celery task to fetch the votations
        """
        for votation_date in queryset:
            tasks.init_votations.delay(votation_date.pk)


class VotationTitleInline(admin.TabularInline):
    """
    Inline for votation title translation
    """

    model = models.VotationTitle
    fields = ["language_code", "title"]


@admin.register(models.Votation)
class VotationAdmin(admin.ModelAdmin):
    """
    admin for a single votation
    """

    list_display = [
        "__str__", "date", "is_finished", "needs_staende", "is_accepted"
    ]
    search_fields = ["translation_title_set__name"]

    inlines = [VotationTitleInline]
