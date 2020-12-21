from django.shortcuts import render
from django.http.request import HttpRequest
from django.core.serializers.json import DjangoJSONEncoder
from django.http.response import JsonResponse

from votes.models import Votation, VotationDate
from api import serializers

# Create your views here.


def votation_date_list(request: HttpRequest) -> JsonResponse:
    """
    A list of all votation dates,
    [{'id': 1, 'date': 2020-01-01}]
    """
    serializer = serializers.VotationDateSerializer(VotationDate.objects.all(),
                                                    many=True,
                                                    sparse=True)
    return JsonResponse(serializer.data, safe=False)


def votation_date_detail(request: HttpRequest, votation_date_id: int):
    """
    Info about the selected date and list of votations

    {'id': 1, 'date': 2020-01-01, 'votations': [
        {'id': 5000, 'titles': [{'language_code': 'de', 'title': '...'}], 'finished': ..},
    ]}

    """
    votation_date = VotationDate.objects.get(pk=votation_date_id)

    serializer = serializers.VotationDateSerializer(votation_date)

    return JsonResponse(serializer.data)


def votation_detail(request: HttpRequest, votation_id: int):
    """
    Dict for CH with:
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
