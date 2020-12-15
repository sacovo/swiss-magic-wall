"""
Hallo
"""
from django.shortcuts import render
from django.http.request import HttpRequest
from django.http.response import HttpResponse, JsonResponse

from geo.models import Gemeinde, Kanton


def canton_detail(request: HttpRequest, canton_id: int) -> HttpResponse:
    pass


def commune_detail(request: HttpRequest, commune_id: int) -> HttpResponse:
    pass


def canton_json(request: HttpRequest, canton_id: int) -> JsonResponse:
    pass


def commune_json(request: HttpRequest, commune_id: int) -> JsonResponse:
    pass
