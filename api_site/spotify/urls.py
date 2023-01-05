from django.contrib import admin
from django.urls import path, include
from .views import *
from . import models


urlpatterns = [
    path('get-auth-url', AuthURL.as_view()),
    path('redirect', spotify_callback),
    path('is-authenticated', IsAuthenticated.as_view()),
    path('new-albums', new_albums_view, name='new-albums'),
    path('test/', json_output_to_web_spotify, name='test-spotify'),
    path('test-list/', test_list, name='test-list-spotify'),
]
