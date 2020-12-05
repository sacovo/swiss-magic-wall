"""
This module defines the models to store results to elections or referenda
"""
from django.db import models

# Create your models here.
from geo.models import Gemeinde
from votes.models import Votation


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

    votation = models.ForeignKey(Votation,
                                 models.CASCADE,
                                 related_name="projection")
    model_votations = models.ManyToManyField(Votation, blank=True)
    projection = models.FileField(upload_to="projections/",
                                  null=True,
                                  blank=True)

    def __str__(self):
        return f"Projection for {self.votation}"


class Result(models.Model):
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

    id = models.BigAutoField(primary_key=True)
    yes_percent = models.FloatField()
    participation = models.FloatField()

    yes_absolute = models.IntegerField()
    no_absolute = models.IntegerField()

    is_final = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)

    gemeinde = models.ForeignKey(Gemeinde, models.CASCADE)
    votation = models.ForeignKey(Votation, models.CASCADE)

    def __str__(self):
        return f"Result for {self.gemeinde.name} for #{self.votation.id} at {self.timestamp}"
