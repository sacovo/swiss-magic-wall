from datetime import datetime
from geo.models import Gemeinde
from dal import autocomplete
from predict.tasks import run_calculation

from django.http.request import HttpRequest
from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.decorators.cache import cache_page

from api import serializers
from api.forms import ResultEntryForm
from predict.models import Timestamp, input_json_result
from votes.models import Votation, VotationDate

# Create your views here.


@cache_page(60 * 15)
def votation_date_list(request: HttpRequest) -> JsonResponse:
    """Return a list of all votation dates."""
    serializer = serializers.VotationDateSerializer(VotationDate.objects.all(),
                                                    many=True,
                                                    sparse=True)
    return JsonResponse(serializer.data, safe=False)


@cache_page(60)
def votation_date_detail(request: HttpRequest, votation_date_id: int):
    """
    Info about the selected date and list of votations.

    {'id': 1, 'date': 2020-01-01, 'votations': [
        {'id': 5000, 'titles': [{'language_code': 'de', 'title': '...'}],
        'finished': ..},
    ]}

    """
    votation_date = VotationDate.objects.get(pk=votation_date_id)

    serializer = serializers.VotationDateSerializer(votation_date)

    return JsonResponse(serializer.data)


@cache_page(30)
def votation_detail(request: HttpRequest, votation_id: int):
    """
    Return dict for CH with.

    dict includes:
        - Titles - [{language: 'de', 'title': ...}, ...]

        - Yes counted, yes_counted
        - Yes predicted, yes_predicted
        - No counted, no_counted
        - No predicted, no_predicted
        - Stände yes, staende_ja
        - needs_staende
        - accepted
        - finished
        - cantons: [{'id': ..., 'yes_counted', ...}]
        - communes: []
    """
    votation = Votation.objects.get(pk=votation_id)

    serializer = serializers.ExpandedVotationSerializer(votation)

    return JsonResponse(serializer.data)


@cache_page(30)
def votation_stats(request: HttpRequest,
                   votation_id: int,
                   canton_id=None) -> JsonResponse:
    """Return stats about one votation"""
    votation = Votation.objects.get(id=votation_id)

    return JsonResponse(votation.get_count_stats(canton_id), safe=False)


@cache_page(30)
def votation_stats_commune(request: HttpRequest,
                           votation_id: int,
                           commune_id=None) -> JsonResponse:
    """Return stats about one votation for a commune."""
    votation = Votation.objects.get(id=votation_id)

    return JsonResponse(votation.get_count_stats_commune(commune_id), safe=False)


def swiss_stats(request: HttpRequest, votation_id: int) -> JsonResponse:
    """Return stats about switzerland for a votation."""
    votation: Votation = Votation.objects.get(id=votation_id)

    return JsonResponse(votation.related_stats(), safe=False)


def canton_stats(request: HttpRequest, votation_id: int, canton_id: int) -> JsonResponse:
    """Return stats about one canton."""
    votation: Votation = Votation.objects.get(id=votation_id)
    return JsonResponse(votation.related_stats_canton(canton_id), safe=False)


def commune_stats(request: HttpRequest, votation_id: int,
                  commune_id: int) -> JsonResponse:
    """Return stats about one commune."""
    votation: Votation = Votation.objects.get(id=votation_id)
    return JsonResponse(votation.related_stats_commune(commune_id), safe=False)


class CommuneAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        if self.q and len(self.q) > 2:
            qs = Gemeinde.objects.filter(name__icontains=self.q)
            return qs
        return Gemeinde.objects.none()


class VoteAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        if self.q and len(self.q) > 2:
            qs = Votation.objects.filter(is_finished=False,
                                         titles__title__icontains=self.q).distinct()
            return qs
        return Votation.objects.none()


def enter_result(request):
    form = ResultEntryForm()

    if request.method == 'POST':
        form = ResultEntryForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            city = data['city']
            vote = data['vote']

            total = data['total']
            yes_total = data['yes_absolute']
            no_total = data['no_absolute']
            t = Timestamp.objects.create(t=datetime.now())

            input_json_result(
                city, vote, {
                    'gebietAusgezaehlt': True,
                    'jaStimmenInProzent': yes_total / total * 100,
                    'stimmbeteiligungInProzent': (yes_total+no_total) / total * 100,
                    'jaStimmenAbsolut': yes_total,
                    'neinStimmenAbsolut': no_total,
                    'anzahlStimmberechtigte': total,
                }, t)

            run_calculation.delay(vote.pk, t.pk)

    return render(request, 'api/input_form.html', {'form': form})
