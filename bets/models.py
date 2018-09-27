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
    user = models.ForeignKey(user_model, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
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

    def __str__(self):
        return 'comments for ' + str(self.match)


def calculate_ranklist(sender, instance, created, *args, **kwargs):
    if not instance.match_ended:
        return
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


def add_user_extra_info(sender, instance, created, *args, **kwargs):
    """initializes extra info database with default data"""
    if created:
        new_user = UserExtraInfo(user=instance)
        new_user.save()


post_save.connect(calculate_ranklist, sender=Match)
post_save.connect(add_user_extra_info, sender=user_model)
