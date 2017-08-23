from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.welcome),
    url(r'^show$', views.show),
    url(r'^play$', views.play),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^home$', views.home),
    url(r'^leaderboard$', views.leaderboard),
    url(r'^logout$', views.logout),
    url(r'^delete/user/(?P<id>\d+)/$', views.delete),
    url(r'^process$', views.process),
]