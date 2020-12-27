"""
This module defines the models to store results to elections or referenda
"""

from django.utils import timezone
import numpy as np
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
from geo.models import Gemeinde
from predict import utils


def nan():
    return float("nan")


class VotingModel(models.Model):
    """
    A selection of votations are used to calculate a model to make projections.

    Attributes:
    -----------
    votation: Votation
        the votation that this model is for
    model_votations: List[Votation]
        list of past votations that should be used to calculate the model
    projection: file
        saved projection that should be used to calculate the model
    """

    votation = models.OneToOneField(
        "votes.Votation",
        models.CASCADE,
        related_name="projection",
        verbose_name=_("votation"),
    )
    model_votations = models.ManyToManyField(
        "votes.Votation",
        blank=True,
        related_name="+",
        verbose_name=_("model votations"),
    )
    yes_projection = models.FileField(
        upload_to="projections/",
        null=True,
        blank=True,
        verbose_name=_("yes projection"),
    )

    participation_projection = models.FileField(
        upload_to="projections/",
        null=True,
        blank=True,
        verbose_name=_("participation projection"),
    )

    def __str__(self):
        return f"Projection for {self.votation}"

    def build_projection_matrix(self):
        """Builds and saves the projection matrix"""
        votations = list(self.model_votations.all())
        gemeinden = Gemeinde.objects.filter(latestresult__votation_id=self.votation_id)

        result_matrix = np.empty(shape=(len(gemeinden), len(votations)))
        particpation_matrix = np.empty(shape=(len(gemeinden), len(votations)))

        # Build the Matrix with the past results
        for i, votation in enumerate(votations):
            votation.ensure_results_for(gemeinden)
            result_matrix[:, i] = votation.get_result_vector(gemeinden)
            particpation_matrix[:, i] = votation.get_participation_vector(gemeinden)

        # Calculate the projection
        yes_projection: np.ndarray = utils.calculate_projection(result_matrix)
        participation_projection = utils.calculate_projection(particpation_matrix)

        # Save them to the filesystem
        utils.save_projection_to_file(yes_projection, self.yes_projection, self.pk, "yes")
        utils.save_projection_to_file(participation_projection,
                                      self.participation_projection, self.pk, "part")

        self.save()

    def get_yes_projection(self) -> np.ndarray:
        """Loads the projection from the filesystem"""
        return np.load(self.yes_projection)

    def get_participation_projection(self) -> np.ndarray:
        """Loads the projection for the participation from the filesystem"""
        return np.load(self.participation_projection)

    class Meta:
        verbose_name = _("voting model")
        verbose_name_plural = _("voting models")


class Timestamp(models.Model):
    t = models.DateTimeField(auto_now_add=True, primary_key=True)

    class Meta:
        ordering = ['-t']


class AbstractResult(models.Model):
    """
    Represents a result of an election, could be final or a temporary projection

    ...

    Attributes:
    ----------
    yes_percent: float
        percentage of people that voted yes
    participation: float
        percentage of the eligible voters that participated
    yes_absolute: int
        absolute number of people that voted yes
    no_absolute: int
        absolute number of people that voted no
    is_final: bool
        whether the result is final or a projection
    timestamp: datetime
        timestamp when the result was first created
    gemeinde: Gemeinde
        the gemeinde that the result belongs to
    votation: Votation
        the votation that this result is from
    """

    id = models.BigAutoField(primary_key=True, verbose_name=_("id"))
    yes_percent = models.FloatField(default=0, verbose_name=_("yes percent"))
    participation = models.FloatField(default=0, verbose_name=_("participation"))

    yes_absolute = models.IntegerField(default=0, verbose_name=_("yes absolute"))
    no_absolute = models.IntegerField(default=0, verbose_name=_("no absolute"))

    is_final = models.BooleanField(default=False, verbose_name=_("is final"))

    gemeinde = models.ForeignKey(Gemeinde, models.CASCADE, verbose_name=_("commune"))
    votation = models.ForeignKey(
        "votes.Votation", models.CASCADE, verbose_name=_("votation")
    )

    def __str__(self):
        return f"Result for {self.gemeinde.name} for #{self.votation.id} at {self.timestamp}"

    class Meta:
        abstract = True
        ordering = ["votation", "gemeinde"]


class LatestResult(AbstractResult):
    """
    Unique for every combination of votation and gemeinde, stores
    the latest result for every votation
    """

    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["gemeinde", "votation"],
                                    name="unique_gemeinde_votation")
        ]
        verbose_name = _("latest result")
        verbose_name_plural = _("latest results")
        ordering = ["votation", "gemeinde"]


class Result(AbstractResult):
    """
    Not unique for every combination, used to store the timeseries
    """

    timestamp = models.ForeignKey(Timestamp, models.CASCADE)

    class Meta:
        verbose_name = _("result")
        verbose_name_plural = _("results")
        ordering = ["votation", "gemeinde"]


def input_json_result(gemeinde: Gemeinde, votation: "Votation", result_data: dict,
                      timestamp: Timestamp):
    """
    Creates a new Result and updates or creates the latest result for this votation.
    """
    is_final = result_data["gebietAusgezaehlt"]

    if not is_final:
        LatestResult.objects.get_or_create(votation=votation, gemeinde=gemeinde)
        return

    info_dict = dict(
        is_final=is_final,
        yes_percent=result_data["jaStimmenInProzent"],
        participation=result_data["stimmbeteiligungInProzent"] or 0,
        yes_absolute=result_data["jaStimmenAbsolut"],
        no_absolute=result_data["neinStimmenAbsolut"],
    )

    LatestResult.objects.update_or_create(gemeinde=gemeinde,
                                          votation=votation,
                                          defaults=info_dict)

    if result_data["anzahlStimmberechtigte"]:
        gemeinde.voters = result_data["anzahlStimmberechtigte"]
        gemeinde.save()
    info_dict['id'] = None

    Result.objects.create(gemeinde=gemeinde,
                          votation=votation,
                          timestamp=timestamp,
                          **info_dict)
    return
