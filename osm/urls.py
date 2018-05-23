from django.conf.urls import url,include
from django.contrib import admin
from . import views
from .models import Node
from djgeojson .views import GeoJSONLayerView

urlpatterns = [
    url(r'^$',views.home,name="home"),
    url(r'^stops/',views.get_stops, name="stops"),
    url(r'^osm/', views.load, name="load"),
    url(r'^data/', GeoJSONLayerView.as_view(model=Node, properties=('id','version','visible','incomplete')), name="data")
]
