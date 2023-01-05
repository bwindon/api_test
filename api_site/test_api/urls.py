from django.contrib import admin
from django.urls import path, include
from .views import *
from . import models

urlpatterns = [
    path('menu/', menu, name='menu'),
    path('', base_map, name='Base Map View'),
    path('connected/', connected_map, name='Connect Map View'),
    path('dataframe/', dataframe, name='Dataframe'),
    #path(r"^oauth/", include("social_django.urls", namespace="social")),
    path('oauth/', include("social_django.urls", namespace="social")),
]
