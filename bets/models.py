from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

# match status choices
choices = (('Home Team Wins', 'home'), ('Guest Team Wins', 'away'), ('Tie', 'tie'))
user_model = get_user_model()


class User(AbstractUser):
    """adds extra fields for user"""
    bio = models.TextField()


class Match(models.Model):
    """saves data for match"""
    home_team = models.CharField(max_length=255)
    away_team = models.CharField(max_length=255)
    match_start_time = models.DateField()
    match_ended = models.BooleanField(default=False)
    match_status = models.CharField(choices=choices)
    score_home = models.IntegerField(default=0)
    score_away = models.IntegerField(default=0)
    created_on = models.DateField(default=timezone.now)
    edited_on = models.DateField(auto_now=True)


class UserPredictions(models.Model):
    """save user prediction for users"""
    user = models.ForeignKey(user_model, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    predicted_match_state = models.CharField(choices=choices)
    predicted_goals_home = models.IntegerField(default=0)
    predicted_goals_away = models.IntegerField(default=0)
    gained_points = models.IntegerField(default=0)
    created_on = models.DateTimeField(default=timezone.now)
    edited_on = models.DateTimeField(auto_now=True)


class RankList(models.Model):
    """Save and update current ranklist"""
    user = models.ForeignKey(user_model, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    updated_on = models.DateTimeField(auto_now=True)

    def update_ranklist(self, instance):
        """Updates and save current playlist"""
        pass


class MatchComments(models.Model):
    """saves comments about match"""
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    user = models.ForeignKey(user_model)
    comment = models.TextField()


class RankListComments(models.Model):
    """saves comments about RankList"""
    user = models.ForeignKey(user_model)
    comment = models.TextField()
