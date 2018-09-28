from rest_framework import serializers
from bets.models import Match, RankList, MatchComments
from django.contrib.auth import get_user_model


class MatchesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ('id', 'home_team', 'away_team', 'match_start_time', 'score_home', 'score_away')
        extra_kwargs = {
            'id': {'read_only': True},
            'home_team': {'read_only': True},
            'away_team': {'read_only': True},
            'match_start_time': {'read_only': True},
            'score_home': {'read_only': True},
            'score_away': {'read_only': True},
        }


class RankListSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = RankList
        fields = ('user', 'points')


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


class CommentsSerializer(serializers.ModelSerializer):
    user_username = serializers.ReadOnlyField(source='user.username')
    match_name = serializers.ReadOnlyField(source='match.__str__')

    class Meta:
        model = MatchComments
        fields = ('id', 'user', 'user_username', 'match', 'match_name', 'comment', 'rating')
