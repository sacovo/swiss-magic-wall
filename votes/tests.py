from unittest import skip

from django.test import TestCase
from django.utils.timezone import now

from geo.models import Gemeinde, Kanton
from predict.models import LatestResult, Result
from votes import tasks
from votes.models import Votation, VotationDate

# Create your tests here.


class VotationDateInitTest(TestCase):
    """
    Test the fetching of voting results
    """

    url = ("https://app-prod-static-voteinfo.s3.eu-central-1.amazonaws.com"
           "/v1/ogd/sd-t-17-02-20201129-eidgAbstimmung.json")

    def test_fetching(self):
        """
        Test the whole fetching process in steps
        """
        data, _ = tasks.fetch_json_from(self.url)

        votation_list = tasks.iterate_votations(data)
        self.assertEqual(len(votation_list), 2)

        kantone_list = tasks.iterate_kantone(votation_list[0])
        self.assertEqual(len(kantone_list), 26)

        gemeinde_list = tasks.iterate_gemeinden(kantone_list[0])

        self.assertTrue(len(gemeinde_list) >= 10)

    def test_initialize(self):
        """
        Test the process of fetching an url and initalizing the
        kantone and gemeinden.
        """
        start_date = now()
        votation_date = VotationDate.objects.create(json_url=self.url,
                                                    start_date=start_date)

        tasks.init_votations(votation_date.pk)

        self.assertEqual(len(Votation.objects.all()),
                         2,
                         msg="Two votations should be created")
        self.assertTrue(
            len(Gemeinde.objects.all()) > 30,
            msg="some gemeinden should have been create",
        )
        self.assertEqual(len(Kanton.objects.all()),
                         26,
                         msg="There should be exactly 26 kantons")
        self.assertTrue(Result.objects.all().exists())
        self.assertTrue(LatestResult.objects.all().exists())
        self.assertEqual(len(Result.objects.all()), len(LatestResult.objects.all()))


class TestGemeindenVotation(TestCase):

    def test_ensure_gemeinden(self):
        """Ensure the right amount of votes for all votations"""
        kanton = Kanton.objects.create(name="Test", geo_id=1)

        Gemeinde.objects.create(name="Test", geo_id=10, kanton=kanton, voters=12)
        Gemeinde.objects.create(name="Test", geo_id=11, kanton=kanton, voters=12)
        Gemeinde.objects.create(name="Test", geo_id=12, kanton=kanton, voters=12)
        Gemeinde.objects.create(name="Test", geo_id=13, kanton=kanton, voters=12)
        Gemeinde.objects.create(name="Test", geo_id=14, kanton=kanton, voters=12)

        date = VotationDate.objects.create(json_url="https://no-url.com",
                                           start_date=now())

        votation = Votation.objects.create(date=date, needs_staende=True, id=1)

        votation.ensure_results_for(Gemeinde.objects.all())

        self.assertEqual(len(votation.latestresult_set.all()), 5)
