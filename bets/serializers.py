from rest_framework import serializers
from bets.models import Match


class MatchesEndedListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        exclude = ('created_on', 'edited_on', 'match_ended')


class MatchesBetListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ('id', 'home_team', 'away_team', 'match_start_time')
