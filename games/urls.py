from django.urls import path, re_path
from . import views

app_name = "games"
urlpatterns = [
    path('', views.index, name="home"),
    re_path(r'^games/([-\w]+)/$', views.games_list, name='games'),
    re_path(r'^search/$', views.game_search, name='search'),
    re_path(r'^api/games/([-\w]+)/$', views.games_list_api),
    re_path(r'^sendotp/$', views.send_otp, name="send-otp"),
    re_path(r'^recent/$', views.recentPlayed, name="recent")

]