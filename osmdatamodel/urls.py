from django.conf.urls import url,include
from django.contrib import admin
from django.urls import path
from osm import views
urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$',include('osm.urls')),
    url(r'^stops/',views.get_stops, name="stops"),
    url(r'^osm/', views.load, name="load"),
    url(r'^route_masters', views.get_route_master_relations, name="route_master"),
]
