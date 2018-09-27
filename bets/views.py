from rest_framework import viewsets
from bets.models import Match, RankList
from django.utils import timezone
from bets.serializers import MatchesBetListSerializer, MatchesEndedListSerializer, RankListSerializer, \
    UserProfileSerializer
from django.contrib.auth import get_user_model
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken


class RegisterUser(viewsets.ModelViewSet):
    """register a new user"""
    serializer_class = UserProfileSerializer
    queryset = get_user_model().objects.all()


class LoginUser(viewsets.ViewSet):
    """log user in"""
    serializer_class = AuthTokenSerializer

    def create(self, request, *args, **kwargs):
        return ObtainAuthToken().post(request)


class MatchesBetListView(viewsets.ModelViewSet):
    """Get all matches for which the bets are possible"""
    serializer_class = MatchesBetListSerializer
    start_time = timezone.now() + timezone.timedelta(minutes=30)
    queryset = Match.objects.filter(match_ended=False, match_start_time__gt=start_time)


class MatchEndedView(viewsets.ModelViewSet):
    """Get all matches which has ended"""
    queryset = Match.objects.filter(match_ended=True)
    serializer_class = MatchesEndedListSerializer


class RankListView(viewsets.ModelViewSet):
    """Get all matches for which the bets are possible"""
    queryset = RankList.objects.all()
    serializer_class = RankListSerializer
