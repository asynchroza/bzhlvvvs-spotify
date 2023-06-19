import json
from os import environ
import requests
from base64 import b64encode
from dotenv import load_dotenv
from random import random
from typing import Union

# container won't copy .env file
load_dotenv(".env.spotify")

SPOTIFY_API = "https://api.spotify.com"

def _get(obj: dict, key: str, throw: bool = False) -> Union[str, None]:
    """Utility function for fetching an item from a dictionary.
    Throws a well formatted exception if key is not found and throw argument is True.
    Otherwise, it returns None.

    Args:
        throw (bool, optional): Throw exception if key is not found

    Returns:
        Union[str, None]
    """
    try: 
        return obj[key]
    except Exception as e:
        if throw:
            raise Exception(f"{str(e)} key was not found in dictionary")
        return None



def get_environment() -> dict[str, None]:
    """Loads all environment variables needed for making calls
    and updating the html template.

    Implementation:
        Some of the variables are loaded using get() because they're
        not mission critical, the template will simply not render the corresponding elements.

    Returns:
        dict[str, None]
    """
    
    return {
        "CLIENT_ID": _get(environ, "CLIENT_ID", True),
        "CLIENT_SECRET": _get(environ, "CLIENT_SECRET", True),
        "PLAYLIST_ID": _get(environ, "PLAYLIST_ID", True),
        "TITLE": _get(environ, "TITLE", True),
        "LINKEDIN": _get(environ, "LINKEDIN"),
        "GITHUB": _get(environ, "GITHUB"),
        "FAVICON_URL": _get(environ, "FAVICON_URL"),
    }


def get_token(CLIENT_ID: str, CLIENT_SECRET: str) -> str:
    access_token = b64encode(bytes(f"{CLIENT_ID}:{CLIENT_SECRET}", "utf-8"))
    token_url = "https://accounts.spotify.com/api/token"

    headers = {"Authorization": f'Basic {access_token.decode("utf-8")}'}

    payload = {"grant_type": "client_credentials"}

    response = json.loads(
        requests.post(token_url, data=payload, headers=headers).content
    )

    return response["access_token"]


def get_tracks(bearer_token: str) -> list:
    playlists_url = f"{SPOTIFY_API}/v1/playlists/4qw4F3Mi3eGjXwLeKM5pYx"

    headers = {"Authorization": f"Bearer {bearer_token}"}

    response = json.loads(requests.get(playlists_url, headers=headers).content)
    return response["tracks"]["items"]


def get_artist_names(artists):
    artist_names = [artist["name"] for artist in artists]

    # Concatenate the names into a comma-separated string
    artist_names_string = ", ".join(artist_names)

    return artist_names_string


def get_artist_image(artist_url, bearer_token):
    headers = {"Authorization": f"Bearer {bearer_token}"}

    response = json.loads(requests.get(artist_url, headers=headers).content)
    return response["images"][0]["url"]


def get_random_track_data(tracks: list, bearer_token: str) -> dict:
    selected_track = tracks[int(random() * len(tracks))]

    track_url = selected_track["track"]["external_urls"]["spotify"]
    track_image_url = selected_track["track"]["album"]["images"][0][
        "url"
    ]  # expecting that the first object is always the largest
    track_name = selected_track["track"]["name"]

    artist_names_string = get_artist_names(selected_track["track"]["artists"])
    artist_image_url = get_artist_image(
        selected_track["track"]["artists"][0]["href"], bearer_token
    )

    track_data = {
        "track_url": track_url,
        "track_image_url": track_image_url,
        "track_name": track_name,
        "artist_names": artist_names_string,
        "artist_image_url": artist_image_url,
    }

    return track_data


def insert_data_in_template(html: str, track_data: dict) -> str:
    html = (
        html.replace("{artist.image}", track_data["artist_image_url"])
        .replace("{track.name}", track_data["track_name"])
        .replace("{track.artist}", track_data["artist_names"])
        .replace("{track.image}", track_data["track_image_url"])
        .replace("{track.url}", track_data["track_url"])
    )

    return html


def lambda_handler(event, context):
    try:
        html = open("index.html", "r").read()
        environment = get_environment()
        bearer_token = get_token(environment["CLIENT_ID"], environment["SECRET_ID"])
        tracks = get_tracks(bearer_token)
        track_data = get_random_track_data(tracks, bearer_token)
        html = insert_data_in_template(html, track_data)

        return {
            "headers": {"Content-Type": "text/html"},
            "statusCode": 200,
            "body": html,
        }

    except Exception as e:
        print(e)

        return {
            "headers": {"Content-Type": "application/json"},
            "statusCode": 500,
            "body": {
                "message": "I'm probably in the Bahamas 🌴 right now! Excuse me for the inconvenience. I will get it fixed once I'm back 🫶.",
                "playlist": "https://open.spotify.com/playlist/4qw4F3Mi3eGjXwLeKM5pYx?si=e26637db63a94ca0",
                "error": str(e),
            },
        }
