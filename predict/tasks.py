"""
Shared tasks for calculating projections
"""
from celery import shared_task
from django.utils import timezone

from geo.models import Gemeinde
from votes.models import Votation, VotationDate

from predict.models import input_json_result, VotingModel, Result, LatestResult, Timestamp
from predict.utils import prediction
from votes.tasks import (
    fetch_json_from,
    iterate_kantone,
    iterate_gemeinden,
    iterate_votations,
)


def update_results(data: dict, timestamp: Timestamp) -> bool:
    """
    Iterates over the votations in the data list,
    returns true if the votations are all finished and the
    counting can stop.
    """
    all_finished = True
    results = []

    for votation_data in iterate_votations(data):
        votation = update_votation(votation_data)

        all_finished = all_finished and votation.is_finished

        for kanton_data in iterate_kantone(votation_data):
            for gemeinde_data in iterate_gemeinden(kanton_data):
                result = update_gemeinde(gemeinde_data, votation, timestamp)

                if result:
                    results.append(result)

        Result.objects.bulk_create(results)

        if not votation.is_finished:
            calculate_projection.delay(votation.pk)

    return all_finished


@shared_task
def calculate_projection(votation_pk: int, timestamp: Timestamp):
    """
    Uses the results we already have and calculates the new results
    """
    votation = Votation.objects.get(pk=votation_pk)
    model: VotingModel = votation.projection

    yes_projection = model.get_yes_projection()
    participation_projection = model.get_participation_projection()

    yes_vector = votation.get_yes_vector()
    particpation_vector = votation.get_participation_vector()
    indexes = votation.get_index_vector()

    yes_results = prediction(yes_projection, yes_vector, indexes)
    part_results = prediction(participation_projection, particpation_vector, indexes)

    latest_results = [] # We only want to make one query to the database, so
    results = []        # we store the results in memory and bulk save them.

    # No we have to write these results into the database
    for i, latest_result in votation.latestresult_set.filter(is_final=False):
        gemeinde = latest_result.gemeinde

        latest_result.yes_percent = yes_results[i]
        latest_result.participation = part_results[i]
        latest_result.yes_absolute = gemeinde.voters * yes_results[i] * part_results[i]
        latest_result.no_absolute = gemeinde.voters - latest_result.yes_absolute

        latest_results.append(latest_result)

        results.append(
            Result(
                yes_percent=latest_result.yes_percent,
                participation=latest_result.participation,
                yes_absolute=latest_result.yes_absolute,
                no_absolute=latest_result.no_absolute,
                votation=votation,
                gemeinde=latest_result.gemeinde,
                timestamp=timestamp,
                is_final=False,
            ))

    LatestResult.objects.bulk_update(latest_results)
    Result.objects.bulk_create(results)


def update_votation(data: dict) -> Votation:
    """
    Update is finished and is_accepted from the dict and
    return the votation that is described through this votation.
    """
    votation: Votation = Votation.objects.get(id=data["vorlagenId"])

    votation.is_finished = data["vorlageBeendet"]
    votation.is_accepted = data["vorlageAngenommen"]

    return votation


def update_gemeinde(data: dict, votation: Votation, timestamp: Timestamp) -> Result:
    """
    Create a new result for the given gemeinde and votation if
    the count in this votation is finished.
    """
    gemeinde = Gemeinde.objects.get(geo_id=data["geoLevelnummer"])

    if gemeinde.latestresult_set.filter(is_final=True, votation=votation).exists():
        return

    return input_json_result(gemeinde, votation, data["resltat"], timestamp)


@shared_task
def check_running_counts():
    """
    Selects the votations that are currently running and fetches them.
    """
    active_votation_dates = VotationDate.objects.filter(start_date__lte=timezone.now(),
                                                        is_finished=False)
    if active_votation_dates.exists():
        timestamp = Timestamp.objects.create()

        for active_votation_date in active_votation_dates:
            active_votation_date.is_finished = update_results(
                fetch_json_from(active_votation_date.json_url), timestamp)
            active_votation_date.save()
