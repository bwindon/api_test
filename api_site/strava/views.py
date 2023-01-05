import django_filters
from django_tables2 import SingleTableView, LazyPaginator
from django_tables2.views import SingleTableMixin
from django_filters.views import FilterView
from django.shortcuts import render
from django.http import JsonResponse
from openpyxl.worksheet import page

from .utils import *
import pandas as pd
from django.views.generic import ListView, TemplateView
from.tables import *


# Create your views here.
def menu(request):
    return HttpResponse("This is the start of an STRAVA menu page.")


def home(request):
    return render(request, 'home.html')


# get activities with no iteration for testing. Returns dataframe. Retrieves latest 30 activities.
def activities_dataframe_view(request):
    with open('complete_activities_list.json') as json_data:
        d = json.load(json_data)

    df = pd.DataFrame(d)

    print(df)
    df_dict = {
        "df": df.to_html()
    }
    return render(request, 'dataframe.html', context=df_dict)


def json_view(request):
    with open('complete_activities_list.json') as json_data:
        d = json.load(json_data)

        name_list = []
        distance_list = []
        moving_time_list = []
        elapsed_time_list = []
        total_elevation_gain_list = []
        type_list = []
        start_date_list = []
        start_date_local_list = []
        average_speed_list = []
        max_speed_list = []
        average_cadence_list = []
        has_heartrate_list = []
        average_heartrate_list = []
        max_heartrate_list = []

# iterate through each activity array of 200
        for row in d:
            activities = row

# iterate through 200 activities
            for a_row in activities:
                name = a_row['name']
                distance = a_row['distance']
                moving_time = a_row['moving_time']
                moving_time_pretty = get_pretty_time(moving_time)

                elapsed_time = a_row['elapsed_time']
                elapsed_time_pretty = get_pretty_time(elapsed_time)

                total_elevation_gain = a_row['total_elevation_gain']
                type = a_row['type']

                start_date = a_row['start_date']
                start_date_pretty = convert_json_to_datetime(start_date)
                start_date_local = a_row['start_date_local']
                start_date_local_pretty = convert_json_to_datetime(start_date_local)
                offset = start_date_local_pretty - start_date_pretty
                start_date_offset = start_date_pretty - offset
                start_date_local_offset = start_date_local_pretty - offset

                average_speed = a_row['average_speed']
                max_speed = a_row['max_speed']
                average_cadence = a_row.get('average_cadence', 0)
                has_heartrate = a_row['has_heartrate']
                average_heartrate = a_row.get('average_heartrate', 0)
                max_heartrate = a_row.get('max_heartrate', 0)

                name_list.append(name)
                distance_list.append(distance)
                moving_time_list.append(moving_time_pretty)

                elapsed_time_list.append(elapsed_time)
                total_elevation_gain_list.append(total_elevation_gain)
                type_list.append(type)

                start_date_list.append(start_date_offset)
                start_date_local_list.append(start_date_local_offset)

                average_speed_list.append(average_speed)
                max_speed_list.append(max_speed)
                average_cadence_list.append(average_cadence)
                has_heartrate_list.append(has_heartrate)
                average_heartrate_list.append(average_heartrate)
                max_heartrate_list.append(max_heartrate)

            zip_list = zip(name_list,
                           distance_list,
                           moving_time_list,
                           elapsed_time_list,
                           total_elevation_gain_list,
                           type_list,
                           start_date_list,
                           start_date_local_list,
                           average_speed_list,
                           max_speed_list,
                           average_cadence_list,
                           has_heartrate_list,
                           average_heartrate_list,
                           max_heartrate_list)
            context = {'zip_list': zip_list}

        return render(request, 'json_list.html', context)


class ActivityListView(ListView):
    model = ActivityObject
    template_name = 'activity_objects.html'


class ActivitySingleTableView(SingleTableView):
    model = ActivityObject
    table_class = ActivityObjectTable
    template_name = 'activity_single_table.html'


class ActivityObjectFilter(django_filters.FilterSet):
    class Meta:
        model = ActivityObject
        fields = '__all__'


class FilteredActivityObjectListView(SingleTableMixin, FilterView):
    table_class = ActivityObjectTable
    model = ActivityObject
    template_name = 'activity_filter_table.html'

    filterset_class = ActivityObjectFilter


# shell top work with from games app
def test_chart(request):
    return render(request, 'js_chart_strava.html')


def eddington(request):
    return render(request, 'eddington.html')


def json_output_to_web(request):
    with open('complete_activities_list.json') as json_data:
        d = json.load(json_data)
    json_d = json.dumps(d)
    return JsonResponse(d, safe=False)
