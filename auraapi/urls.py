from django.urls import path
from . import views

urlpatterns = [
    path("health", views.health, name="health"),
    path("cities", views.list_cities, name="list_cities"),
    path("ground/<str:city>/<str:param>", views.ground_timeseries, name="ground_timeseries"),
    path("tempo/<str:city>", views.tempo_collocated, name="tempo_collocated"),
    path("forecast/<str:city>/<str:param>", views.forecast, name="forecast"),
    path("manifest", views.manifest, name="manifest"),
]
