from django.conf.urls import url, include
from bets import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('register', views.RegisterUser, base_name='register')
router.register('match/betlist', views.MatchesBetListView, base_name='match_betlist')
router.register('match/ended', views.MatchEndedView, base_name='match_ended')
router.register('ranklist', views.RankListView, base_name='ranklist')
router.register('login', views.LoginUser, base_name='login')

app_name = 'bets'

urlpatterns = [
    url(r'', include(router.urls)),

]
