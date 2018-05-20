from django.conf.urls import url,include
from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    url(r'^$',views.home,name="home"),
    url(r'^stops/',views.get_stops, name="stops"),
    url(r'^osm/', views.load, name="load"),
]
