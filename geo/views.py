"""
Hallo
"""
from django.shortcuts import render, get_object_or_404
from django.http.request import HttpRequest
from django.http.response import HttpResponse, JsonResponse

from geo.models import Gemeinde, Kanton


def canton_list(request: HttpRequest) -> HttpResponse:

    return render(request, "geo/canton_list.html", {"cantons": Kanton.objects.all()})


def canton_detail(request: HttpRequest, canton_id: int) -> HttpResponse:
    canton = get_object_or_404(Kanton, id=canton_id)

    return render(request, "geo/canton_detail.html", {"canton": canton})


def commune_detail(request: HttpRequest, commune_id: int) -> HttpResponse:
    commune = get_object_or_404(Gemeinde, id=commune_id)

    return render(request, "geo/commune_detail.html", {"commune": commune})


def canton_json(request: HttpRequest, canton_id: int) -> JsonResponse:
    pass


def commune_json(request: HttpRequest, commune_id: int) -> JsonResponse:
    pass
