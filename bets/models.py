from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save

# match status choices
choices = (('home', 'Home Team Wins'), ('away', 'Guest Team Wins'), ('tie', 'Tie'), ('ns', 'Not started'))
# current_user_model
user_model = get_user_model()


class UserExtraInfo(models.Model):
    """adds extra fields for user"""
    user = models.OneToOneField(user_model, on_delete=models.CASCADE)
    bio = models.TextField(default='BetMaster!')
    favourite_team = models.CharField(max_length=255, default="No favourite team")

    def __str__(self):
        return self.user


class Match(models.Model):
    """saves data for match"""
    home_team = models.CharField(max_length=255)
    away_team = models.CharField(max_length=255)
    match_start_time = models.DateTimeField()
    match_ended = models.BooleanField(default=False)
    match_status = models.CharField(choices=choices, max_length=10, default='ns')
    score_home = models.IntegerField(default=0)
    score_away = models.IntegerField(default=0)
    created_on = models.DateField(default=timezone.now)
    edited_on = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.home_team) + ' vs ' + str(self.away_team)


class UserPredictions(models.Model):
    """save user prediction for users"""
    user = models.ForeignKey(user_model, on_delete=models.CASCADE, related_name='prediction_user')
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='prediction_match')
    predicted_match_state = models.CharField(choices=choices, max_length=10)
    predicted_goals_home = models.IntegerField(default=0)
    predicted_goals_away = models.IntegerField(default=0)
    match_gained_points = models.IntegerField(default=0)
    created_on = models.DateTimeField(default=timezone.now)
    edited_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user) + ' : ' + str(self.match)


class RankList(models.Model):
    """Save and update current ranklist"""
    user = models.ForeignKey(user_model, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user) + ' : ' + str(self.points)


class MatchComments(models.Model):
    """saves comments about match"""
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='comment_match')
    user = models.ForeignKey(user_model, on_delete=models.CASCADE, related_name='comment_user')
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

    def __str__(self):
        return 'comments for ' + str(self.match)


def calculate_ranklist(sender, instance, created, *args, **kwargs):
    if not instance.match_ended:
        return
    user_points = {}
    for item in UserPredictions.objects.all():
        if item.user in user_points:
            print(item.match_gained_points)
            user_points[item.user] += item.match_gained_points
        else:
            user_points[item.user] = 0
    print(user_points)
    for item in user_points:
        user = user_points[item][0]
        points = user_points[item][1]
        user_obj = RankList.objects.get_or_create(user=user)[0]
        user_obj.points = points
        user_obj.save()


def add_user_extra_info(sender, instance, created, *args, **kwargs):
    """initializes extra info database with default data"""
    if created:
        new_user = UserExtraInfo(user=instance)
        new_user.save()


def score_calculator(sender, instance, created, *args, **kwargs):
    # 1. Calculate points for every user upon saving match result.
    # check for match_is_over to be true to continue
    if not instance.match_ended:
        return
    queryset = UserPredictions.objects.filter(match=instance)
    match_goals_home = instance.score_home
    match_goals_away = instance.score_away
    match_status = instance.match_status

    for item in queryset:
        user_prediction_goals_home = item.predicted_goals_home
        user_prediction_goals_away = item.predicted_goals_away
        user_prediction_match_state = item.predicted_match_state
        points = 0
        if user_prediction_match_state == match_status:
            points += 3
        if user_prediction_goals_home == match_goals_home and user_prediction_goals_away == match_goals_away:
            points += 6
        item.match_gained_points = points
        item.save()


post_save.connect(calculate_ranklist, sender=Match)
post_save.connect(add_user_extra_info, sender=user_model)
post_save.connect(score_calculator, sender=Match)
