from django.shortcuts import render
from django.http import HttpResponse
import folium
import pandas as pd
import requests
import polyline
from json2html import *
# Create your views here.


def menu(request):
    return HttpResponse("This is the start of an menu page.")


def dataframe(request):
    # Make your map object
    user = request.user
    print(user)
    strava_login = user.social_auth.get(provider='strava')
    print(strava_login)
    access_token = strava_login.extra_data['access_token']
    print(access_token)
    activities_url = "https://www.strava.com/api/v3/athlete/activities/"

    # Get activity data
    header = {'Authorization': 'Bearer ' + str(access_token)}

    activities_json = requests.get(activities_url, headers=header).json()
    df = pd.DataFrame(activities_json)

    print(df)
    df_dict = {
        "df": df.to_html()
    }
    return render(request, 'dataframe.html', context=df_dict)


def base_map(request):
    # Make your map object
    main_map = folium.Map(location=[-33.8688, 151.2093], zoom_start = 12) # Create base map
    main_map_html = main_map._repr_html_() # Get HTML for website

    context = {
        "main_map":main_map_html
    }
    return render(request, 'index.html', context)


def connected_map(request):
    # Make your map object
    main_map = folium.Map(location=[-33.8688, 151.2093], zoom_start = 12) # Create base map
    user = request.user # Pulls in the Strava User data
    strava_login = user.social_auth.get(provider='strava') # Strava login
    access_token = strava_login.extra_data['access_token'] # Strava Access token
    activites_url = "https://www.strava.com/api/v3/athlete/activities"

    # Get activity data
    header = {'Authorization': 'Bearer ' + str(access_token)}
    activity_df_list = []
    for n in range(5):  # Change this to be higher if you have more than 1000 activities
        param = {'per_page': 200, 'page': n + 1}

        activities_json = requests.get(activites_url, headers=header, params=param).json()
        if not activities_json:
            break
        activity_df_list.append(pd.json_normalize(activities_json))
        # data check
        print(activity_df_list)

    # Get Polyline Data
    activities_df = pd.concat(activity_df_list)
    activities_df = activities_df.dropna(subset=['map.summary_polyline'])
    activities_df['polylines'] = activities_df['map.summary_polyline'].apply(polyline.decode)

    # Plot Polylines onto Folium Map
    for pl in activities_df['polylines']:
        folium.PolyLine(locations=pl, color='red').add_to(main_map)

    # Return HTML version of map
    main_map_html = main_map._repr_html_() # Get HTML for website
    context = {
        "main_map":main_map_html
    }
    return render(request, 'index.html', context)