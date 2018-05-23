from django.conf.urls import url,include
from django.contrib import admin
from osm import views
from django.views.generic import TemplateView
from djgeojson.views import GeoJSONLayerView
from osm.models import Node

urlpatterns = [
    url('admin/', admin.site.urls),
    url(r'^$',include('osm.urls')),
    url(r'^data/', GeoJSONLayerView.as_view(model=Node, properties=('id','version','visible','incomplete')), name="data"),
    url(r'^stops/',views.get_stops, name="stops"),
    url(r'^osm/', views.load, name="load"),
    url(r'^route_masters', views.get_route_master_relations, name="route_master"),
]
