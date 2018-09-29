from rest_framework import serializers
from bets.models import Match, RankList, MatchComments, UserPredictions
from django.contrib.auth import get_user_model
from django.utils import timezone
from bets.helpers import check_correct_user_prediction


class MatchesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = (
            'id', 'home_team', 'away_team', 'match_start_time', 'match_ended', 'match_status', 'score_home',
            'score_away')
        extra_kwargs = {
            'id': {'read_only': True},
            'home_team': {'read_only': True},
            'away_team': {'read_only': True},
            'match_ended': {'read_only': True},
            'match_start_time': {'read_only': True},
            'match_status': {'read_only': True},
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
        user_model = get_user_model()
        new_user = user_model(username=validated_data['username'])
        new_user.set_password(validated_data['password'])
        new_user.save()
        return new_user


class CommentsSerializer(serializers.ModelSerializer):
    user_username = serializers.ReadOnlyField(source='user.username')
    match_name = serializers.ReadOnlyField(source='match.__str__')

    class Meta:
        model = MatchComments
        fields = ('id', 'user', 'user_username', 'match', 'match_name', 'comment', 'rating')


class UserPredictionSerializer(serializers.ModelSerializer):
    user_username = serializers.ReadOnlyField(source='user.username')
    match_name = serializers.ReadOnlyField(source='match.__str__')
    match_ended = serializers.ReadOnlyField(source='match.match_ended')
    match_status = serializers.ReadOnlyField(source='match.match_status')
    match_result_goals_home = serializers.ReadOnlyField(source='match.score_home')
    match_result_goals_away = serializers.ReadOnlyField(source='match.score_away')

    class Meta:
        model = UserPredictions
        fields = ('id', 'user', 'user_username', 'match', 'match_name', 'match_ended',
                  'match_status', 'match_result_goals_home', 'match_result_goals_away',
                  'predicted_match_state', 'predicted_goals_home', 'predicted_goals_away')

    def create(self, validated_data):
        current_time = timezone.now() + timezone.timedelta(minutes=30)
        current_user = validated_data['user']
        current_match = validated_data['match']
        if UserPredictions.objects.filter(user=current_user, match=current_match).count() != 0:
            raise serializers.ValidationError('User prediction already in database!')
        if current_match.match_start_time < current_time:
            raise serializers.ValidationError('Too LATE! Match is starting in 30 minutes or less!')
        state = check_correct_user_prediction(match_state=validated_data['predicted_match_state'],
                                              goals_home=validated_data['predicted_goals_home'],
                                              goals_away=validated_data['predicted_goals_away'])
        if state['state']:
            raise serializers.ValidationError(state['error'])
        return super(UserPredictionSerializer, self).create(validated_data)
