from dateutil import parser
from django.http import HttpResponse, response
from .models import *
from .tokens import get_access_token
import requests
import calendar
import datetime

DATABASE_CONFIG = {
    "database": "api_test_db",
    "user": "postgres",
    "password": "anzac1914",
    "host": "localhost",
    "port":  5432,
}


def get_activity_name_by_id_from_db(obj_id):
    obj = ActivityData.objects.get(pk=obj_id).json_activity_blob
    # Make object a dictionary by taking first index
    obj_row = obj[0]
    name = obj_row['name']
    return name


def get_activity_date_by_id_from_db(obj_id):
    obj = ActivityData.objects.get(pk=obj_id).json_activity_blob
    # Make object a dictionary by taking first index
    obj_row = obj[0]
    date = obj_row['start_date']
    return date


# added a switch for either complete of last_db_import
# get activities list from api occurring after last database save and create 'activities_after_last_save_to_db.json'
def create_json_file(num):
    # check token is current and if not update
    # 1 = last_db_import
    # 2 = complete activity list_json

    access_token = get_access_token()
    activities_url = "https://www.strava.com/api/v3/athlete/activities/"
    header = {'Authorization': 'Bearer ' + str(access_token)}

    if num == 1:
        last_db_import = get_latest_import_time()
        print(last_db_import, 'checking if new activities exit')
    elif num == 2:
        last_db_import = 1262304000
        # epoch date time for 1 Jan 2010
    else:
        last_db_import = get_latest_import_time()

    data = []
    for n in range(10):  # Change this to be higher if you have more than 1000 activities
        param = {'per_page': 200, 'page': n + 1, 'after': last_db_import}
        res = requests.get(activities_url, headers=header, params=param).json()
        if not res:
            break
        data.append(res)

    if num == 1:
        with open('activities_after_last_save_to_db.json', 'w') as outfile:
            json.dump(data, outfile)
        with open('activities_after_last_save_to_db.json') as check:
            data = json.load(check)
    elif num == 2:
        with open('complete_activities_list.json', 'w') as outfile:
            json.dump(data, outfile)
        with open('complete_activities_list.json') as check:
            data = json.load(check)
    else:
        with open('activities_after_last_save_to_db.json', 'w') as outfile:
            json.dump(data, outfile)
        with open('activities_after_last_save_to_db.json') as check:
            data = json.load(check)

    return HttpResponse(num, 'JSON file updated')


# get json and save to Activity model (requires a check what is new since last dump)
def update_activity_database(request):
    # update JSON with new activities or create blank JSON
    create_json_file(1)
    with open('activities_after_last_save_to_db.json') as json_data:
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

        for row in d:
            activities = row

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

                i = ActivityObject(
                    name=name,
                    distance=distance,
                    moving_time=moving_time_pretty,
                    elapsed_time=elapsed_time_pretty,
                    total_elevation_gain=total_elevation_gain,
                    type=type,
                    start_date=start_date_offset,
                    start_date_local=start_date_local_offset,
                    average_speed=average_speed,
                    max_speed=max_speed,
                    average_cadence=average_cadence,
                    has_heartrate=has_heartrate,
                    average_heartrate=average_heartrate,
                    max_heartrate=max_heartrate,
                    )
                i.save()
        return HttpResponse('updated')


def create_json_file_view(request):
    create_json_file(2)
    return HttpResponse('updated')


def get_pretty_time(moving_time):
    result = str(datetime.timedelta(seconds=moving_time))
    return result


def convert_json_to_datetime(string):
    dt_object = parser.isoparse(string)
    return dt_object


def get_latest_import_time():
    qs = ActivityObject.objects.values_list('activity_logged_time', flat=True).order_by('-activity_logged_time')
    if qs.exists():
        date_time = next(iter(qs))
        latest_epoch = convert_date_to_epoch(date_time)
        print(latest_epoch, 'epoch of last activity')
        return latest_epoch

    else:
        latest_epoch = 1262304000
        # epoch date time for 1 Jan 2010
        return latest_epoch


def convert_date_to_epoch(date_time):
    epoch = calendar.timegm(date_time.timetuple())
    return epoch
