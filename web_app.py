import requests
import os
import folium
from dotenv import load_dotenv
import json
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy.exc import GeocoderUnavailable, GeopyError

load_dotenv()
bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
main_map = folium.Map()
geolocator = Nominatim(user_agent='web_app.py')
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1, max_retries=0)


def location_from_user_id(user_id):
    """
    returns location from user_id
    :param user_id: str
    :return: (latitude, longitude)
    """
    base_url = "https://api.twitter.com/"
    search_headers = {
        'Authorization': 'Bearer {}'.format(bearer_token)
    }
    search_params = {
        'ids': user_id,
        'user.fields': 'location'
    }
    search_url = '{}2/users/'.format(base_url)
    search_resp = requests.get(search_url, headers=search_headers, params=search_params)
    try:
        location = search_resp.json()['data'][0]['location']
    except KeyError:
        location = ''
    return location


def username_to_id_and_loc(username):
    """
    Returns user_id by username and it`s location
    :param username: str
    :return: (user_id, location)
    """
    base_url = "https://api.twitter.com/"
    search_headers = {
        'Authorization': 'Bearer {}'.format(bearer_token)
    }
    search_params = {
        'usernames': username,
        'user.fields': 'id,username,location'
    }
    search_url = '{}2/users/by'.format(base_url)
    search_resp = requests.get(search_url, headers=search_headers, params=search_params)
    try:
        location = search_resp.json()['data'][0]['location']
        geolocator.geocode(location)
    except KeyError:
        location = ''
    return search_resp.json()['data'][0]['id'], location

def get_following_users(user_id):
    """
    Return list of users in format (username, name, location), followed by user_id
    :param user_id: str
    :return: [(username, name, (latitude, longitude)), ...]
    """
    base_url = "https://api.twitter.com/"
    search_headers = {
        'Authorization': 'Bearer {}'.format(bearer_token)
    }
    search_url = '{}2/users/{}/following'.format(base_url, user_id)
    search_resp = requests.get(search_url, headers=search_headers)
    following = search_resp.json()
    parsed_following = []
    cache = {}
    for user in following['data']:
        username = user['username']
        try:
            name = user['name']
        except KeyError:
            name = ''
        try:
            location = location_from_user_id(user['id'])
        except KeyError:
            location = ''
        text_location = location
        if text_location in cache.keys():
            lat, long = cache[text_location]
        else:
            if text_location == '':
                continue
            try:
                coords = geolocator.geocode(text_location)
            except GeocoderUnavailable:
                continue
            try:
                lat, long = coords.latitude, coords.longitude
            except AttributeError:
                continue
            cache[text_location] = (lat, long)
        parsed_following.append((username, name, (lat, long)))
    return parsed_following


def main(zero_username):
    zero_id, zero_location = username_to_id_and_loc(zero_username)
    print('Please wait!')
    following_users = get_following_users(zero_id)
    if type(zero_location) is not str:
        main_map.add_child(folium.Marker(location=zero_location, popup='This person is here',
                                         icon=folium.Icon(color='red', icon_color='blue', icon='home')))
    for user in following_users:
        main_map.add_child(folium.Marker(location=user[2], popup="Name: {}, Username: @{}".format(user[1], user[0]),
                                         icon=folium.Icon(color="green", icon_color="yellow", icon="fa-circle-user")))
    main_map.save('templates/map.html')
    print('Done! Check result in /map.html')


if __name__ == '__main__':
    main()