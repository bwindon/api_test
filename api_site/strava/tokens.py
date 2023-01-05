from django.http import HttpResponse, JsonResponse
from .models import *
import requests
from .credentials import CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN
import time


def get_access_token():
    # check whether token is current and update if expired
    token_currency_check()
    with open('strava_tokens.json') as json_data:
        d = json.load(json_data)
        access_token = d['access_token']
    return access_token


# Make Strava auth API call with your. Refresh token with read_all
def refresh_token():
    res = requests.post(
        url='https://www.strava.com/oauth/token',
        data={
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'grant_type': 'refresh_token',
            'refresh_token': REFRESH_TOKEN
             }
        )
    strava_tokens = res.json()

    # Save tokens to file
    with open('strava_tokens.json', 'w') as outfile:
        json.dump(strava_tokens, outfile)
    with open('strava_tokens.json') as check:
        data = json.load(check)

    # save token to database
    i = StravaToken(json_string=strava_tokens)
    i.save()
    return HttpResponse('token updated')


def token_currency_check():
    # Read JSON and check expires epoch
    with open('strava_tokens.json') as json_data:
        d = json.load(json_data)
        expires = d['expires_at']
        print(expires, 'token expires_at')
        now = time.time()
        if now > expires:
            check = 'expired'
            print('expired token')
            refresh_token()
        else:
            check = 'current'
            print('current token')

        return HttpResponse(check)


def strava_token_view(request):
    obj = StravaToken.objects.all()
    # iterate on the json_string field of the object. Print dictionary value.
    for i in obj:
        item = i.json_string
        print(item['expires_in'])

    # iterate on the dictionary within a dictionary
    values_list = list(obj.values('json_string'))

    for v in values_list:
        print(v['json_string']['expires_in'])

    return JsonResponse(values_list, safe=False)
