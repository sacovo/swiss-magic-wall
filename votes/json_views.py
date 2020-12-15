from django.http.request import HttpRequest
from django.http.response import JsonResponse

from votes.models import Votation, VotationDate


def votation_date_json(request: HttpRequest, votation_date_id: int) -> JsonResponse:
    votation_date = VotationDate.objects.get(pk=votation_date_id)

    return JsonResponse(votation_date.votation_dict())


def votation_json(request: HttpRequest, votation_id: int) -> JsonResponse:
    """
    Returns information about the requested votation.
    The returned json contains:
        - yes_percent: the projected percentage of the votation
        - yes_absolute: the projected absolute amount of yes voters
        - no_absolute: the projected absolute amount of no voters
        - yes_counted: the currently counted votes for yes
        - no_counted: the currently counted votes for no
        - staende_projection: projected amount of staende that agree
        - staende_counted: counted staende
    """

    votation: Votation = Votation.objects.get(id=votation_id)

    return JsonResponse(votation.result_dict())


def votation_canton_json(request: HttpRequest, votation_id: int) -> JsonResponse:
    """
    Returns a list of dicts that contain information about the cantons
    for the requested votation. Each entry contains:
        - canton_name
        - canton_id
        - ...
    """
    votation: Votation = Votation.objects.get(votation_id)

    return JsonResponse(votation.result_cantons())


def votation_commune_json(request: HttpRequest, votation_id: int) -> JsonResponse:
    """
    Returns a list of dicts for each commune to the requested votation.
    """
    votation: Votation = Votation.objects.get(votation_id)

    return JsonResponse(votation.result_communes())


def votation_canton_commune_json(request: HttpRequest, votation_id: int,
                                 canton_id: int) -> JsonResponse:
    """
    Returns a list of dicts for each commune to the requested votation and
    canton.
    """
    votation: Votation = Votation.objects.get(votation_id)

    return JsonResponse(votation.result_communes(canton_id))
