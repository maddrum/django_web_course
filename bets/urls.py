from django.conf.urls import url, include
from bets import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register('register', views.RegisterUser, base_name='register')
router.register('login', views.LoginUser, base_name='login')
router.register('match', views.MatchesView, base_name='matches')
router.register('ranklist', views.RankListView, base_name='ranklist')
router.register('comments', views.Comments, base_name='comments')

app_name = 'bets'

urlpatterns = [
    url(r'', include(router.urls)),
    url(r'login_json', obtain_auth_token)
]
