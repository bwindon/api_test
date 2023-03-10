import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .credentials import REDIRECT_URI, CLIENT_ID, CLIENT_SECRET
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from requests import Request, post
from.utils import update_or_create_user_tokens, is_spotify_authenticated


# Create your views here.
class AuthURL(APIView):
    def get(self, request, format=None):
        scopes = 'user-read-playback-state user-modify-playback-state user-read-currently-playing'

        url = Request('Get', 'https://accounts.spotify.com/authorize', params={
            'scope': scopes,
            'response_type': 'code',
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID
        }).prepare().url

        return Response({'url': url}, status=status.HTTP_200_OK)


def spotify_callback(request, format=None):
    #code = request.GET.code('code', 'default')
    error = request.GET.get('error')

    #print('do i get code?  ', code)

    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'authorization_code',
        #'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }).json()

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    refresh_token = response.get('refresh_token')
    expires_in = response.get('expires_in')
    error = response.get('error')

    print('access', access_token)

    if not request.session.exists(request.session.session_key):
        request.session.create()

    update_or_create_user_tokens(request.session.session_key, access_token, token_type, expires_in, refresh_token)

    return redirect('frontend:')


class IsAuthenticated(APIView):
    def get_authenticators(self, request, format=None):
        is_authenticated = is_spotify_authenticated(self.request.session.session_key)
        return Response({'status': is_authenticated}, status=status.HTTP_200_OK)


def new_albums_view(request):
    with open('new_albums.json') as json_data:
        d = json.load(json_data)
        name_list = []
        artist_name_list = []
        release_date_list = []

        for item in d['albums']['items']:
            name = item['name']
            release_date = item['release_date']

            length = len(item['artists'])
            artist_name_list_sub = []
            for x in range(length):
                artist_name_sub = item['artists'][x]['name']
                artist_name_list_sub.append(artist_name_sub)

            name_list.append(name)
            release_date_list.append(release_date)
            artist_name_list.append(artist_name_list_sub)

        zip_list = zip(name_list, release_date_list, artist_name_list)
        context = {'zip_list': zip_list}

        return render(request, 'new_albums_list.html', context)


# shell top work with from games app
def test_list(request):
    return render(request, 'js_list_spotify.html')


def json_output_to_web_spotify(request):
    with open('new_albums.json') as json_data:
        d = json.load(json_data)
    json_d = json.dumps(d)
    return JsonResponse(d, safe=False)
