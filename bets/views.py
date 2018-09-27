from rest_framework.views import APIView
from rest_framework.views import Response
from bets.models import Match
from django.utils import timezone
from bets.serializers import MatchesBetListSerializer, MatchesEndedListSerializer


class MatchesBetListView(APIView):
    """Get all matches for which the bets are possible"""

    def get(self, request, format=None):
        start_time = timezone.now() + timezone.timedelta(minutes=30)
        queryset = Match.objects.filter(match_ended=False, match_start_time__gt=start_time)
        serialized_data = MatchesBetListSerializer(instance=queryset, many=True)
        return Response(data=serialized_data.data)


class MatchEndedView(APIView):
    """Get all matches which has ended"""

    def get(self, request, format=None):
        queryset = Match.objects.filter(match_ended=True)
        serialized_data = MatchesEndedListSerializer(instance=queryset, many=True)
        return Response(data=serialized_data.data)
