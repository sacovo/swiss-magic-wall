"""
Views for showing details of a votation
"""
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http.request import HttpRequest
from django.http.response import HttpResponse, JsonResponse

from votes.models import Votation, VotationDate
from geo.models import Kanton

# Create your views here.


def latest_votation_date(request: HttpRequest) -> HttpResponse:
    votation_date = VotationDate.objects.order_by('-start_date').first()

    return render(request, "votes/votation_date_detail.html", {
        'votation_date': votation_date,
    })


def votation_date_list(request: HttpRequest) -> HttpResponse:
    paginator = Paginator(VotationDate.objects.all().order_by('-start_date'), 5)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    return render(request, "votes/votation_date_list.html", {
        'page': page,
    })


def votation_date_detail(request: HttpRequest, votation_date_id: int) -> HttpResponse:
    votation_date = get_object_or_404(VotationDate, pk=votation_date_id)

    return render(request, "votes/votation_date_detail.html",
                  {'votation_date': votation_date})


def votation_detail(request: HttpRequest, votation_id: int) -> HttpResponse:
    votation = get_object_or_404(Votation, id=votation_id)

    return render(request, "votes/votation_detail.html", {
        'votation': votation,
        'votation_date': votation.date,
    })


def votation_stats(request: HttpRequest, votation_id: int) -> HttpResponse:
    votation = get_object_or_404(Votation, id=votation_id)

    return render(request, "votes/votation_stats.html", {
        'votation': votation,
        'votation_date': votation.date,
    })


def votation_communes(request: HttpRequest, votation_id: int) -> HttpResponse:
    votation = get_object_or_404(Votation, id=votation_id)

    return render(request, "votes/votation_communes.html", {
        'votation': votation,
        'votation_date': votation.date,
    })


def votation_canton_detail(request: HttpRequest, votation_id: int,
                           canton_id: int) -> HttpResponse:
    votation = get_object_or_404(Votation, id=votation_id)
    canton = get_object_or_404(Kanton, id=canton_id)

    return render(request, "votes/votation_communes.html", {
        'votation': votation,
        'votation_date': votation.date,
        'canton': canton,
    })
