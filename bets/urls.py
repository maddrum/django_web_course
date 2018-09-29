from django.conf.urls import url, include
from bets import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register('register', views.RegisterUser, base_name='register')
router.register('login', views.LoginUser, base_name='login')
router.register('match', views.MatchesView, base_name='matches')
router.register('ranklist', views.RankListView, base_name='ranklist')
router.register('comments', views.CommentsView, base_name='comments')
router.register('user_predictions', views.UserPredictionsView, base_name='user_predictions')
router.register('user_notes', views.UserPrivateNotesView, base_name='user_private_notes')

app_name = 'bets'

urlpatterns = [
    url(r'', include(router.urls)),
    url(r'login_json', obtain_auth_token)
]
