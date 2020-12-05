from django.test import TestCase
from django.utils.timezone import now
from votes.models import VotationDate, Votation
from votes import tasks
from geo.models import Kanton, Gemeinde

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
        data = tasks.fetch_json_from(self.url)

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
