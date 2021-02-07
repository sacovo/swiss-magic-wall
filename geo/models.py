from django.db import models
from django.utils.translation import gettext_lazy as _


class GeoObject(models.Model):
    """
    Abstract base class for all models that are a representation of of
    a geographic region (communities, kantons, ...)

    ...

    Attributes:
    -----------
    name : str
        name of the entity
    geo_id : int
        id of the entity from the bfs

    """

    name = models.CharField(max_length=100)
    geo_id = models.IntegerField(primary_key=True)

    class Meta:
        abstract = True
        ordering = ["geo_id"]

    def __str__(self):
        return self.name


class Kanton(GeoObject):
    """
    Represents a kanton of Switzerland

    ...

    Attributes:
    -----------
    standesstimme: float
       either 1.0 for a full standesstimme or 0.5 for the cantons that
       have a half standesstimme.
    """

    standesstimme = models.FloatField(default=1.0, verbose_name=_("standesstimme"))

    class Meta:
        verbose_name = _("canton")
        verbose_name_plural = _("cantons")


class Gemeinde(GeoObject):
    """
    Represents a gemeinde of Switzerland


    ...
    Attributes:
    ----------
    kanton: Kanton
        the kanton that this gemeinde belongs to.
    voters: int
        amount of voters that are eligible to vote in this
        commune.
    """

    kanton = models.ForeignKey(Kanton, models.CASCADE, verbose_name=_("canton"))
    voters = models.IntegerField(verbose_name=_("eligible voters"))

    class Meta:
        verbose_name = _("commune")
        verbose_name_plural = _("communes")
