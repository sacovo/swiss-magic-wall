from django.utils import timezone
from rest_framework import serializers
from django.db.models import Sum, F, Max

from geo.models import Gemeinde, Kanton
from predict.models import LatestResult, Timestamp
from votes.models import Votation, VotationDate, VotationTitle


class VotationTitleSerializer(serializers.ModelSerializer):

    class Meta:
        model = VotationTitle
        fields = ['language_code', 'title']


class ResultSerializer(serializers.ModelSerializer):
    geo_id = serializers.IntegerField(source="gemeinde_id")
    yes_total = serializers.IntegerField(source="yes_absolute")
    no_total = serializers.IntegerField(source="no_absolute")
    canton = serializers.IntegerField(source="gemeinde.kanton_id")
    name = serializers.CharField(source="gemeinde.name")

    class Meta:
        model = LatestResult

        fields = [
            'participation', 'yes_total', 'no_total', 'is_final', 'geo_id', 'canton',
            'name'
        ]


class CantonResultSerializer(serializers.Serializer):
    geo_id = serializers.IntegerField()

    yes_total = serializers.IntegerField(source="yes")
    no_total = serializers.IntegerField(source="no")

    yes_predicted = serializers.IntegerField()
    no_predicted = serializers.IntegerField()

    is_final = serializers.BooleanField()
    name = serializers.CharField()


class VotationSerializer(serializers.ModelSerializer):

    titles = VotationTitleSerializer(many=True, read_only=True)
    yes_counted = serializers.IntegerField()
    no_counted = serializers.IntegerField()

    yes_predicted = serializers.IntegerField()
    no_predicted = serializers.IntegerField()

    predicted_communes = serializers.IntegerField()
    counted_communes = serializers.IntegerField()

    def to_representation(self, instance):
        counted_results = instance.latestresult_set.filter(is_final=True).aggregate(
            yes_counted=Sum('yes_absolute'), no_counted=Sum('no_absolute'))

        instance.counted_communes = instance.latestresult_set.filter(
            is_final=True).count()

        instance.yes_counted = counted_results['yes_counted'] or 0
        instance.no_counted = counted_results['no_counted'] or 0

        predicted_results = instance.latestresult_set.filter(is_final=False).aggregate(
            yes_predicted=Sum('yes_absolute'), no_predicted=Sum('no_absolute'))

        instance.yes_predicted = predicted_results['yes_predicted'] or 0
        instance.no_predicted = predicted_results['no_predicted'] or 0

        instance.predicted_communes = instance.latestresult_set.filter(
            is_final=False).count()

        return super().to_representation(instance)

    class Meta:
        model = Votation
        fields = [
            'id',
            'titles',
            'is_finished',
            'needs_staende',
            'is_accepted',
            'yes_counted',
            'no_counted',
            'yes_predicted',
            'no_predicted',
            'counted_communes',
            'predicted_communes',
            'date_id',
        ]


class VotationDateSerializer(serializers.ModelSerializer):

    votations = VotationSerializer(many=True, read_only=True)

    def __init__(self, *args, **kwargs):
        self.sparse = kwargs.pop('sparse', False)

        super().__init__(*args, **kwargs)

    def to_representation(self, instance):
        if self.sparse:
            instance.votations = []
        else:
            instance.votations = instance.votation_set
        return super().to_representation(instance)

    class Meta:
        model = VotationDate

        fields = ['id', 'start_date', 'votations', 'is_finished']


class ExpandedVotationSerializer(VotationSerializer):
    cantons = CantonResultSerializer(source="kanton_results", many=True, read_only=True)
    communes = ResultSerializer(
        source="prefetched",
        many=True,
        read_only=True,
    )
    timestamp = serializers.DateTimeField()

    def to_representation(self, instance):
        instance.kanton_results = instance.result_cantons().values()
        instance.prefetched = instance.latestresult_set.prefetch_related('gemeinde')
        instance.timestamp = instance.latestresult_set.aggregate(t=Max('timestamp'))['t']

        return super().to_representation(instance)

    class Meta:
        model = Votation
        fields = [
            'id', 'titles', 'is_finished', 'needs_staende', 'is_accepted', 'yes_counted',
            'no_counted', 'yes_predicted', 'no_predicted', 'counted_communes',
            'predicted_communes', 'communes', 'cantons', 'date_id', 'timestamp'
        ]
