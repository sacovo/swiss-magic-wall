from django import forms
from dal import autocomplete
from geo.models import Gemeinde
from votes.models import Votation


class ResultEntryForm(forms.Form):
    city = forms.ModelChoiceField(
        Gemeinde.objects.all(),
        widget=autocomplete.ModelSelect2(url='api:commune-autocomplete'),
        label="Gemeinde")
    vote = forms.ModelChoiceField(
        Votation.objects.all(),
        widget=autocomplete.ModelSelect2(url="api:vote-autocomplete"),
        label="Abstimmung")
    total = forms.IntegerField(label="Anzahl Stimmberechtigte")

    yes_absolute = forms.IntegerField(label="Ja-Stimmen")
    no_absolute = forms.IntegerField(label="Nein-Stimmen")
