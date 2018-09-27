from rest_framework import serializers
from bets.models import Match, RankList, MatchComments


class MatchesEndedListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        exclude = ('created_on', 'edited_on', 'match_ended')


class MatchesBetListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ('id', 'home_team', 'away_team', 'match_start_time')


class RankListSerializer(serializers.ModelSerializer):
    # user1 = serializers.Field(source='user.username')

    class Meta:
        model = RankList
        fields = ('user', 'points')


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchComments
        fields = ('match', 'user')
