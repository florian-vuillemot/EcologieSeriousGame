from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^construction/', views.construction, name='construction'),
    url(r'^listeElements/', views.listeElements, name='listeElements'),
    url(r'^ressources', views.ressources, name='ressources'),
    url(r'^lose', views.lose, name='lose'),
    url(r'^win', views.win, name='win'),
]