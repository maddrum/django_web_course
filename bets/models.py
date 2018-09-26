from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

# match status choices
choices = (('Home Team Wins', 'home'), ('Guest Team Wins', 'away'), ('Tie', 'tie'))
# current_user_model
user_model = get_user_model()


class UserExtraInfo(models.Model):
    """adds extra fields for user"""
    user = models.OneToOneField(user_model, on_delete=models.CASCADE)
    bio = models.TextField(default='BetMaster!')
    favourite_team = models.CharField(max_length=255)


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
    match_gained_points = models.IntegerField(default=0)
    created_on = models.DateTimeField(default=timezone.now)
    edited_on = models.DateTimeField(auto_now=True)


class RankList(models.Model):
    """Save and update current ranklist"""
    user = models.ForeignKey(user_model, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    updated_on = models.DateTimeField(auto_now=True)


class MatchComments(models.Model):
    """saves comments about match"""
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    user = models.ForeignKey(user_model)
    comment = models.TextField()
    rating = models.IntegerField(default=0)

    def add_plus(self, instance):
        """plus 1 rating to a comment"""
        instance.rating += 1
        instance.save()

    def add_minus(self, instance):
        """minus 1 rating to a comment"""
        instance.rating -= 1
        instance.save()


def calculate_ranklist():
    user_points = {}
    for item in UserPredictions.objects.all():
        if item.user in user_points:
            user_points[item.user][1] += item.points
        else:
            user_points[item.user] = [item.user, 0]
    for item in user_points:
        user = user_points[item][0]
        points = user_points[item][1]
        user_obj = RankList.objects.get_or_create(user=user)
        user_obj.update(points=points)
