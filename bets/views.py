from rest_framework import viewsets
from bets.models import Match, RankList, MatchComments
from django.utils import timezone
from bets.serializers import MatchesSerializer, RankListSerializer, UserProfileSerializer, CommentsSerializer
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


class MatchesView(viewsets.ModelViewSet):
    """By default: Returns list of all matches
        status parameter:
            active - returns only matches you could bet on
            finished = returns matches that are currently finished"""
    serializer_class = MatchesSerializer

    def get_queryset(self):
        status = self.request.query_params.get('status')
        start_time = timezone.now() + timezone.timedelta(minutes=30)
        queryset = False
        if status:
            if status == 'active':
                queryset = Match.objects.filter(match_start_time__gt=start_time, match_ended=False)
            elif status == 'finished':
                queryset = Match.objects.filter(match_ended=True)
        if not queryset:
            queryset = Match.objects.all()
        return queryset


class RankListView(viewsets.ModelViewSet):
    """Get all matches for which the bets are possible"""
    queryset = RankList.objects.all()
    serializer_class = RankListSerializer


class Comments(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    queryset = MatchComments.objects.all()

    def get_queryset(self):
        match_id = self.request.query_params.get('match_id')
        if match_id:
            queryset = MatchComments.objects.filter(match__id=match_id)
        else:
            queryset = MatchComments.objects.all()
        return queryset
