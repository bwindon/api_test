from django.contrib import admin
from django.urls import path, include
from .views import *
from .tokens import *
from .utils import *
from .other_views_and_utils import *
from . import models


urlpatterns = [
    path('menu/', menu, name='menu'),
    path('home/', home, name='home'),

    # a json file extracted from the database (token model)
    path('strava-token-view', strava_token_view, name='strava-token-view'),

    # query api and create JSON complete activities list (called from HTML button
    path('update-activity-json', create_json_file_view, name='update-activity-json'),


    # a shell for a dataframe view of the JSON complete activities list
    path('activities-dataframe-view/', activities_dataframe_view, name='activities-dataframe-view'),

    # a view from the parsed JSON complete activities list
    path('json-view', json_view, name='json-view'),

    # query api and update database if required
    path('update-activity-database/', update_activity_database, name='update-activity-database'),

    path('oauth/', include('social_django.urls', namespace='social')),

    # tables
    path('activity-table/', ActivityListView.as_view()),
    path('activity-single-table/', ActivitySingleTableView.as_view()),
    path('activity-filter-table/', FilteredActivityObjectListView.as_view()),

    # charts
    path('test-chart', test_chart, name='test-chart'),
    path('eddington', eddington, name='eddington'),

    # urls routes for testing purposes
    path('test/', json_output_to_web, name='jason-web-view'),
    path('token-currency', token_currency_check, name='token-currency'),
    ]
