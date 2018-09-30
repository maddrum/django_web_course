from rest_framework import viewsets
from bets.models import Match, RankList, MatchComments, UserPredictions, UserPrivateNotes
from django.utils import timezone
from bets.serializers import MatchesSerializer, RankListSerializer, UserProfileSerializer, CommentsSerializer, \
    UserPredictionSerializer, UserPrivateNotesSerializer
from django.contrib.auth import get_user_model
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from bets.permissions import UpdateOwnObjects, UserPrivateData
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied


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
        current_time = timezone.now() + timezone.timedelta(minutes=30)
        queryset = False
        if status:
            if status == 'active':
                queryset = Match.objects.filter(match_start_time__gt=current_time, match_ended=False)
            elif status == 'finished':
                queryset = Match.objects.filter(match_ended=True)
        if not queryset:
            queryset = Match.objects.all()
        return queryset


class RankListView(viewsets.ModelViewSet):
    """Get all matches for which the bets are possible"""
    queryset = RankList.objects.all()
    serializer_class = RankListSerializer


class CommentsView(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    queryset = MatchComments.objects.all()
    permission_classes = (UpdateOwnObjects,)
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        match_id = self.request.query_params.get('match_id')
        if match_id:
            queryset = MatchComments.objects.filter(match__id=match_id)
        else:
            queryset = MatchComments.objects.all()
        return queryset


class UserPredictionsView(viewsets.ModelViewSet):
    serializer_class = UserPredictionSerializer
    permission_classes = (UpdateOwnObjects,)
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        # returns all predictions and unfinished matches predictions for user
        finished_matches = UserPredictions.objects.filter(match__match_ended=True)
        if self.request.user.is_authenticated:
            user_matches_queryset = UserPredictions.objects.filter(user=self.request.user, match__match_ended=False)
            final_queryset = finished_matches | user_matches_queryset
            return final_queryset
        return finished_matches

    def perform_create(self, serializer):
        if self.request.user.id is None:
            raise PermissionDenied('No logged-in user!')
        serializer.save(user=self.request.user)


class UserPrivateNotesView(viewsets.ModelViewSet):
    """handles user private notes"""
    serializer_class = UserPrivateNotesSerializer
    permission_classes = (IsAuthenticated, UserPrivateData)
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        queryset = UserPrivateNotes.objects.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
