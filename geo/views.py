"""
Hallo
"""
from django.shortcuts import render

from geo.models import Gemeinde, Kantone


def index(request):
    """
    Hallo
    """
    gemeinde: Gemeinde = Gemeinde.objects.get(pk=1)

    return render(request, "templates/index.html", {"gemeinde": gemeinde})
