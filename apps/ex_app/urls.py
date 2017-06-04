from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^reg$', views.register),
    url(r'^home$', views.home),
    url(r'^logout$', views.logout),
    url(r'^create$', views.create),
    url(r'^submit$', views.submit),
    url(r'^join/(?P<id>\d+)$', views.join),
    url(r'^details/(?P<id>\d+)$', views.details),
]
