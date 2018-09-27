from rest_framework import serializers
from bets.models import Match, RankList, MatchComments
from django.contrib.auth import get_user_model


class MatchesEndedListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        exclude = ('created_on', 'edited_on', 'match_ended')


class MatchesBetListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ('id', 'home_team', 'away_team', 'match_start_time')


class RankListSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = RankList
        fields = ('user', 'points')


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchComments
        fields = ('match', 'user')


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
            }
        }

    def create(self, validated_data):
        model = get_user_model()
        new_user = model(username=validated_data['username'])
        new_user.set_password(validated_data['password'])
        new_user.save()
        return new_user
    