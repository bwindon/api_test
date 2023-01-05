from .utils import *
from requests import Request
import requests


# get activities with no iteration for testing. Retrieves latest 30 activities.
def get_activities_from_api(request):
    access_token = get_access_token()
    activities_url = "https://www.strava.com/api/v3/athlete/activities"
    header = {'Authorization': 'Bearer ' + str(access_token)}
    response = requests.get(activities_url, headers=header).json()

    # Save tokens to file
    with open('small_activity_list.json', 'w') as outfile:
        json.dump(response, outfile)
    with open('small_activity_list.json') as check:
        data = json.load(check)

    return HttpResponse(response)