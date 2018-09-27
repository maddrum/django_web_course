from django.conf.urls import url
from bets import views


app_name = 'bets'

urlpatterns = [
    url(r'match/betlist/$', views.MatchesBetListView.as_view(), name='match_betlist'),
    url(r'match/ended/$', views.MatchEndedView.as_view(), name='match_ended'),
]
