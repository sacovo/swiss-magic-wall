from django.db import models
from django.utils.translation import get_language

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

    start_date = models.DateTimeField()

    json_url = models.URLField(max_length=500)

    def __str__(self):
        return self.start_date.strftime("%Y-%m-%d")


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
    date = models.ForeignKey(VotationDate, models.CASCADE)

    is_finished = models.BooleanField(default=False)
    needs_staende = models.BooleanField()

    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        language_code: str = get_language()
        translation = self.translation_title_set.filter(
            language_code=language_code)

        if bool(translation):
            return translation[0].title
        translations = self.translation_title_set.all()

        if bool(translations):
            return translations[0].title

        return f"#{self.id}"


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

    language_code = models.CharField(max_length=2)
    title = models.CharField(max_length=280)
    votation = models.ForeignKey(Votation, models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["language_code", "votation"],
                name="unique_language_per_vocation",
            )
        ]

    def __str__(self):
        return self.title
