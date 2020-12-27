"""
shared tasks for fetching votation results
"""
import hashlib
from typing import List, Iterable, Tuple

from celery import shared_task
import requests

from geo.models import Gemeinde, Kanton
from votes.models import Votation, VotationTitle, VotationDate
from predict.models import Result, input_json_result, Timestamp, LatestResult


def fetch_json_from(url) -> Tuple[dict, str]:
    """Retrieves the json from the given url and returns the json as dict"""
    response = requests.get(url)
    response_hash = hashlib.sha256(response.content).hexdigest()

    return (response.json()["schweiz"], response_hash)


def iterate_votations(data: Iterable[dict]) -> List[dict]:
    """Iterates over the votations that are present in the given json dict"""
    return data["vorlagen"]


def iterate_kantone(votation_data) -> List[dict]:
    """Iterate over the kantone"""
    return votation_data["kantone"]


def iterate_gemeinden(kanton_data) -> List[dict]:
    """Iterate over the gemeinden"""
    return kanton_data["gemeinden"]


def init_votation(votation_data: dict, votation_date: VotationDate) -> Votation:
    """Read metadata from votation json and create votation in database if not already present"""
    votation, _ = Votation.objects.update_or_create(
        id=votation_data["vorlagenId"],
        defaults={
            "date": votation_date,
            "is_finished": votation_data["vorlageBeendet"],
            "needs_staende": votation_data["doppeltesMehr"],
            "is_accepted": votation_data["vorlageAngenommen"],
        },
    )

    for title in votation_data["vorlagenTitel"]:
        VotationTitle.objects.get_or_create(
            votation=votation,
            language_code=title["langKey"],
            defaults={"title": title["text"]},
        )
    return votation


def init_kanton(kanton_data: dict) -> Kanton:
    """Read information from kanton json and create kanton in db if not already present"""
    kanton, _ = Kanton.objects.get_or_create(
        geo_id=kanton_data["geoLevelnummer"],
        defaults={"name": kanton_data["geoLevelname"]},
    )

    return kanton


def init_kantone(kanton_iterator: Iterable[dict], votation: Votation,
                 timestamp: Timestamp):
    """Iterates over the kantone that and creates them and their gemeinden"""
    results = []

    for kanton_data in kanton_iterator:
        kanton: Kanton = init_kanton(kanton_data)

        results += init_gemeinden(iterate_gemeinden(kanton_data), kanton, votation,
                                  timestamp)

    Result.objects.bulk_create(results)


def init_gemeinde(gemeinde_data: dict, kanton: Kanton, votation: Votation,
                  timestamp: Timestamp) -> Result:
    """Create a single gemeinde if not already present"""

    gemeinde, _ = Gemeinde.objects.get_or_create(
        geo_id=gemeinde_data["geoLevelnummer"],
        defaults={
            "name": gemeinde_data["geoLevelname"],
            "kanton": kanton,
            "voters": gemeinde_data["resultat"].get("anzahlStimmberechtigte", 0) or 0,
        },
    )

    if votation.date.is_demo:
        LatestResult.objects.create(votation=votation, gemeinde=gemeinde)
        return

    return input_json_result(gemeinde, votation, gemeinde_data["resultat"], timestamp)


def init_gemeinden(gemeinde_iterator: Iterable[dict], kanton: Kanton, votation: Votation,
                   timestamp: Timestamp) -> Iterable[Result]:
    """For every gemeinde in the iterator call the gemeinde init"""
    results = []

    for gemeinde_data in gemeinde_iterator:
        result = init_gemeinde(gemeinde_data, kanton, votation, timestamp)
        if result:
            results.append(result)

    return results


@shared_task
def init_votations(votation_date_pk: int):
    """
    Fetches the json under the url and creates:
        - Votations that are in the json
        - Kantone and Gemeinden
        - Sets the amount of eligible if present for any votation
    """
    votation_date = VotationDate.objects.get(pk=votation_date_pk)
    timestamp = Timestamp.objects.create()

    data, h = fetch_json_from(votation_date.json_url)
    votation_list = iterate_votations(data)

    if not votation_date.is_demo:
        votation_date.latest_hash = h
        votation_date.save()

    for votation_data in votation_list:
        votation = init_votation(votation_data, votation_date)
        init_kantone(iterate_kantone(votation_data), votation, timestamp)
