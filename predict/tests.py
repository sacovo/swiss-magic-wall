from unittest.case import skip

from django.test import TestCase

import numpy as np
from geo.models import Gemeinde
from predict.models import VotingModel
from votes.models import Votation, VotationDate

# Create your tests here.


class BuildVotationMatrixTest(TestCase):
    """
    Download past votation results and build a matrix from it.
    """

    @skip
    def test_building_matrix(self):
        """
        Create the votations and fetch the results for them
        """
        votations = Votation.objects.all()

        first_votation = votations[0]

        other_votations = votations[1:]

        voting_model = VotingModel.objects.create(votation=first_votation)
        voting_model.model_votations.set(other_votations)

        voting_model.build_projection_matrix()

        yes_projection = voting_model.get_yes_projection()
        participation_projection = voting_model.get_participation_projection()

        self.assertIsInstance(yes_projection,
                              np.ndarray,
                              msg="Projection is a numpy array")

        self.assertIsInstance(participation_projection,
                              np.ndarray,
                              msg="Projection is a numpy array")
