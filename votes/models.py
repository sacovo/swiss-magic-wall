from django.db.models.aggregates import Count
from django.db.models.expressions import ExpressionWrapper
from django.db.models.fields import CharField, FloatField
from django.db.models.query import QuerySet
import numpy as np
from django.db import models
from django.db.models import Sum, F
from django.db.models.functions import Coalesce, Cast
from django.utils.translation import get_language, gettext_lazy as _

from taggit.managers import TaggableManager

from predict.models import LatestResult

# Create your models here.


class VotationDate(models.Model):
    """
    A day where the votations a counted, usually a sunday.


    Attributes:
    -----------
    start_date: datetime
        date time when the counting starts and projections should be counted,
        usually at 12am
    json_url: URL
        url of the json that provides the current results
    """

    start_date = models.DateTimeField(verbose_name=_("start date"))

    json_url = models.URLField(max_length=500, verbose_name=_("json url"))
    is_finished = models.BooleanField(default=False, verbose_name=_("is finished"))
    is_demo = models.BooleanField(default=False, verbose_name=_("is demo"))
    latest_hash = models.CharField(max_length=500, verbose_name=_("latest hash"), blank=True)

    def __str__(self):
        return self.start_date.strftime("%Y-%m-%d")

    class Meta:
        verbose_name = _("votating day")
        verbose_name_plural = _("voting days")
        ordering = ['-start_date']


class Votation(models.Model):
    """
    One votation that is due at a VotationDate


    Attributes:
    -----------
    id: int
        id of the votation used by the bfs and as the primary_key in the databases
    date: VotationDate
        votation date when this vote will take place
    is_finished: bool
        set to true if the count is done
    needs_staende: bool
        whether or not this vote needs the majority of the votes and
        the majority of the cantons
    is_accepted: bool
        whether or not the vote is accepted, if is_finished is false this is a projection
    """

    id = models.IntegerField(primary_key=True)
    date = models.ForeignKey(VotationDate, models.CASCADE, verbose_name=_("date"))

    is_finished = models.BooleanField(default=False, verbose_name=_("is finished"))
    needs_staende = models.BooleanField(verbose_name=_("needs staende"))

    is_accepted = models.BooleanField(default=False, verbose_name=_("is accepted"))
    related = models.ManyToManyField("self", blank=True)

    tags = TaggableManager(blank=True)

    def result_dict(self) -> dict:
        """Returns a dict with results for the votation"""
        final_results = self.latestresult_set.filter(is_final=True).aggregate(
            yes=Coalesce(Sum("yes_absolute"), 0), no=Coalesce(Sum("no_absolute"), 0))

        predicted_results = self.latestresult_set.filter(is_final=False).aggregate(
            yes=Coalesce(Sum("yes_absolute"), 0), no=Coalesce(Sum("no_absolute"), 0))

        total_counted = final_results["yes"] + final_results["no"]
        total_predicted = predicted_results["yes"] + predicted_results["no"]

        return {
            "yes_counted":
                final_results["yes"],
            "no_counted":
                final_results["no"],
            "total_counted":
                total_counted,
            "yes_predicted":
                predicted_results["yes"],
            "no_predicted":
                predicted_results["no"],
            "total_predicted":
                total_predicted + total_counted,
            "yes_percent_predicted":
                ((final_results["yes"] + predicted_results["yes"]) /
                 (total_predicted+total_counted)) if
                (final_results["yes"] or predicted_results["yes"]) else 0,
            "yes_percent_counted":
                final_results["yes"] / total_counted,
            "percent_counted":
                total_counted / (total_counted+total_predicted) if total_counted else 0,
        }

    def related_stats(self):

        return list(
            self.related.annotate(
                y=Sum('latestresult__yes_absolute'),
                n=Sum('latestresult__no_absolute'),
                l=F('titles__language_code'),
                title=F('titles__title'),
            ).filter(l="de").values('title', 'y', 'n'))

    def related_stats_canton(self, canton_id: int):

        return list(
            self.related.annotate(
                y=Sum('latestresult__yes_absolute'),
                n=Sum('latestresult__no_absolute'),
                l=F('titles__language_code'),
                k=F('latestresult__gemeinde__kanton_id'),
                title=F('titles__title'),
            ).filter(l="de", k=canton_id).values('title', 'y', 'n'))

    def related_stats_commune(self, commune_id: int):
        return list(
            self.related.annotate(
                y=Sum('latestresult__yes_absolute'),
                n=Sum('latestresult__no_absolute'),
                l=F('titles__language_code'),
                c=F('latestresult__gemeinde_id'),
                title=F('titles__title'),
            ).filter(l="de", c=commune_id).values('title', 'y', 'n'))

    def result_cantons(self) -> dict:
        """

        """
        queryset = self.latestresult_set.values("gemeinde__kanton_id").order_by()

        total = annotate_cantons(queryset)
        total = {x["geo_id"]: x for x in total}

        counted = annotate_cantons(
            queryset.filter(is_final=True)).annotate(total=Count("gemeinde__geo_id"))

        counted = {x["geo_id"]: x for x in counted}

        predicted = annotate_cantons(
            queryset.filter(is_final=False)).annotate(total=Count("gemeinde__geo_id"))

        predicted = {x["geo_id"]: x for x in predicted}

        for geo_id in total:
            if geo_id in counted.keys():
                total[geo_id]["yes_counted"] = counted[geo_id]["yes"]
                total[geo_id]["no_counted"] = counted[geo_id]["no"]
            else:
                total[geo_id]["yes_counted"] = 0
                total[geo_id]["no_counted"] = 0

            if geo_id in predicted.keys():
                total[geo_id]["yes_predicted"] = predicted[geo_id]["yes"]
                total[geo_id]["no_predicted"] = predicted[geo_id]["no"]
                total[geo_id]["is_final"] = False
            else:
                total[geo_id]["yes_predicted"] = 0
                total[geo_id]["no_predicted"] = 0
                total[geo_id]["is_final"] = True

        return total

    def result_communes(self, canton_id=0) -> dict:
        if canton_id == 0:
            queryset = self.latestresult_set.order_by()
        else:
            queryset = self.latestresult_set.filter(
                gemeinde__kanton_id=canton_id).order_by()

        return annotate_communes(queryset)

    def get_count_stats(self, canton_id=None):
        query = self.result_set.order_by('timestamp__t').values('timestamp')

        if canton_id:
            query = query.filter(gemeinde__kanton_id=canton_id)

        annotate_dict = {
            'yes': Cast(Sum("yes_absolute"), models.FloatField()),
            'no': Cast(Sum("no_absolute"), models.FloatField()),
            'name': F('timestamp__t'),
            'value': F('yes') / (F('yes') + F('no')) * 100,
            'count': Count('id')
        }

        return [{
            'name': "Prognose",
            'series': list(query.annotate(**annotate_dict).values('name', 'value'))
        }, {
            'name':
                "Count",
            'series':
                list(
                    query.filter(is_final=True).annotate(**annotate_dict).values(
                        'name', 'value'))
        }]

    def get_count_stats_commune(self, commune_id):
        query = self.result_set.filter(
            gemeinde_id=commune_id).order_by('timestamp__t').values('timestamp')

        annotate_dict = {
            'yes': Cast(Sum("yes_absolute"), models.FloatField()),
            'no': Cast(Sum("no_absolute"), models.FloatField()),
            'name': F('timestamp__t'),
            'value': F('yes') / (F('yes') + F('no')) * 100,
            'count': Count('id')
        }

        return [{
            'name': "Prognose",
            'series': list(query.annotate(**annotate_dict).values('name', 'value'))
        }, {
            'name':
                "Count",
            'series':
                list(
                    query.filter(is_final=True).annotate(**annotate_dict).values(
                        'name', 'value'))
        }]

    def __str__(self):
        language_code: str = get_language()
        translation = self.titles.filter(language_code=language_code)

        if bool(translation):
            return translation[0].title
        translations = self.titles.all()

        if bool(translations):
            return translations[0].title

        return f"#{self.id}"

    def ensure_results_for(self, gemeinden: models.QuerySet):
        """
        Ensures that a result for every gemeinde in gemeinden exists in the
        resultset. If a result is missing, a result with NaN values is created.
        """
        missing_gemeinden = gemeinden.exclude(
            pk__in=self.latestresult_set.values("gemeinde"))

        for missing in list(missing_gemeinden):
            LatestResult.objects.create(gemeinde=missing, votation=self)

    def get_result_vector(self, gemeinden=None) -> np.ndarray:
        """
        Return a list of the latest results for this
        votation. This list contains final and projected results,
        to know which ones are final and which are projected use
        `get_index_vector`.
        """
        if gemeinden is None:
            return np.array(self.latestresult_set.all().values_list("yes_percent",
                                                                    flat=True))
        return np.array(
            self.latestresult_set.filter(gemeinde__in=gemeinden).values_list(
                "yes_percent", flat=True))

    def get_participation_vector(self, gemeinden=None) -> np.ndarray:
        """
        Return a list of the latest participation results
        """
        if gemeinden is None:
            return np.array(self.latestresult_set.all().values_list("participation",
                                                                    flat=True))
        return np.array(
            self.latestresult_set.filter(gemeinde__in=gemeinden).values_list(
                "participation", flat=True))

    def get_index_vector(self, gemeinden=None) -> np.ndarray:
        """
        Returns a boolean vector with True for the final results and
        false for the projected results.
        """
        if gemeinden is None:
            return np.array(self.latestresult_set.all().values_list("is_final",
                                                                    flat=True))
        return np.array(
            self.latestresult_set.filter(gemeinde__in=gemeinden).values_list("is_final",
                                                                             flat=True))

    class Meta:
        verbose_name = _("votation")
        verbose_name_plural = _("votations")
        ordering = ['-date__start_date']


class VotationTitle(models.Model):
    """
    Title of the votation in one of the languages of Switzerland.

    Attributes:
        ----------
        language_code: str
        two letter code to indicate the language
        title: str
        title of the votation
        votation: Votation
        votation that this title belongs to.
        """

    language_code = models.CharField(max_length=2, verbose_name=_("language code"))
    title = models.CharField(max_length=280, verbose_name=_("title"))
    votation = models.ForeignKey(Votation, models.CASCADE, verbose_name=_("votation"), related_name='titles')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["language_code", "votation"],
                name="unique_language_per_vocation",
            )
        ]
        verbose_name = _("votation title")
        verbose_name_plural = _("votation titles")

    def __str__(self):
        return self.title


def annotate_cantons(queryset: QuerySet) -> QuerySet:
    """
    Cacluates the total yes and no votes and the yes percentage
    """
    return queryset.annotate(
        geo_id=F("gemeinde__kanton_id"),
        name=F("gemeinde__kanton__name"),
        yes=Cast(Coalesce(Sum("yes_absolute"), 0), models.FloatField()),
        no=Cast(Coalesce(Sum("no_absolute"), 0), models.FloatField()),
    )


def annotate_communes(queryset: QuerySet) -> QuerySet:
    return queryset.annotate(geo_id=F("gemeinde_id"),
                             name=F("gemeinde__name")).values("yes_percent", "geo_id",
                                                              "name", "yes_absolute",
                                                              "no_absolute")
