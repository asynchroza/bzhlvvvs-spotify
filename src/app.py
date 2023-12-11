from json import dumps, loads
from os import environ
import requests
from base64 import b64encode
from dotenv import load_dotenv
from random import random
from typing import Any, Union

# container won't copy .env file
load_dotenv(".env.spotify")

SPOTIFY_API = "https://api.spotify.com"


def _get(obj: dict, key: str, throw: bool = False, default_value = None) -> str:
    """Utility function for fetching an item from a dictionary.
    Throws a well formatted exception if key is not found and `throw` argument is `True`.
    Otherwise, it either returns the passed `default_value` or an `empty string`.

    Args:
        `default_value` (str, optional): Default value to be returned if key is not found.
        Redundant if `throw` is `True`.

        `throw` (bool, optional): Throw exception if key is not found

    Returns:
        Either `default_value` or an `empty_string`
    """

    try:
        return obj[key]
    except Exception as e:
        if throw:
            raise Exception(f"{str(e)} key was not found in dictionary")
        return default_value


def get_environment() -> dict[str, str]:
    return {
        "CLIENT_ID": _get(environ, "CLIENT_ID", throw=True),
        "CLIENT_SECRET": _get(environ, "CLIENT_SECRET", throw=True),
        "PLAYLIST_ID": _get(environ, "PLAYLIST_ID", throw=True),
        "TITLE": _get(environ, "TITLE", throw=True),
        "LINKEDIN": _get(environ, "LINKEDIN"),
        "GITHUB": _get(environ, "GITHUB"),
        "SOUNDCLOUD": _get(environ, "SOUNDCLOUD"),
        "FAVICON_URL": _get(environ, "FAVICON_URL"),
    }


def get_token(CLIENT_ID: str, CLIENT_SECRET: str) -> str:
    access_token = b64encode(bytes(f"{CLIENT_ID}:{CLIENT_SECRET}", "utf-8"))
    token_url = "https://accounts.spotify.com/api/token"

    headers = {"Authorization": f'Basic {access_token.decode("utf-8")}'}

    payload = {"grant_type": "client_credentials"}

    response = loads(requests.post(token_url, data=payload, headers=headers).content)

    return response["access_token"]


def get_playlist_info(
    bearer_token: str, PLAYLIST_ID: str
) -> dict[str, Union[str, Any]]:
    playlists_url = f"{SPOTIFY_API}/v1/playlists/{PLAYLIST_ID}?fields=tracks(total),external_urls(spotify), name"  # noqa: E501
    headers = {"Authorization": f"Bearer {bearer_token}"}

    # initial request is needed for fetching base info about the playlist
    response = loads(requests.get(playlists_url, headers=headers).content)
    playlists_public_url = response["external_urls"]["spotify"]
    playlist_name = response["name"]
    total_tracks = response["tracks"]["total"]

    return {
        "public_url": playlists_public_url,
        "name": playlist_name,
        "total_tracks": total_tracks,
    }


def get_artist_names(artists) -> str:
    artist_names = [artist["name"] for artist in artists]

    # Concatenate the names into a comma-separated string
    artist_names_string = ", ".join(artist_names)

    return artist_names_string


def get_artist_image(artist_url, bearer_token) -> str:
    headers = {"Authorization": f"Bearer {bearer_token}"}

    response = loads(requests.get(artist_url, headers=headers).content)
    return response["images"][0]["url"]


def get_display_name_of_added_by(user_api_url: str, bearer_token: str):
    headers = {"Authorization": f"Bearer {bearer_token}"}

    response = loads(requests.get(user_api_url, headers=headers).content)
    return response["display_name"]


def get_random_track_data(
    total_tracks: int, bearer_token: str, PLAYLIST_ID: str
) -> dict[str, str]:
    selected_track = int(random() * total_tracks)
    playlists_url = f"{SPOTIFY_API}/v1/playlists/{PLAYLIST_ID}/tracks?fields=items(added_by(external_urls, href), href, track(album(external_urls, images), name, images, external_urls, artists(name, href)))&limit={1}&offset={selected_track}"  # noqa: E501

    headers = {"Authorization": f"Bearer {bearer_token}"}
    selected_track = loads(requests.get(playlists_url, headers=headers).content)[
        "items"
    ][0]

    added_by_public_url = selected_track["added_by"]["external_urls"]["spotify"]
    added_by_api_url = selected_track["added_by"]["href"]
    added_by_name = get_display_name_of_added_by(added_by_api_url, bearer_token)
    track_url = selected_track["track"]["external_urls"]["spotify"]
    track_image_url = selected_track["track"]["album"]["images"][0][
        "url"
    ]  # expecting that the first object is always the largest
    track_name = selected_track["track"]["name"]

    artist_names_string = get_artist_names(selected_track["track"]["artists"])
    artist_image_url = get_artist_image(
        selected_track["track"]["artists"][0]["href"], bearer_token
    )

    return {
        "track_url": track_url,
        "track_image_url": track_image_url,
        "track_name": track_name,
        "artist_names": artist_names_string,
        "artist_image_url": artist_image_url,
        "added_by_name": added_by_name,
        "added_by_public_url": added_by_public_url,
    }


def insert_data_in_template(
    html: str, track_data: dict, environment: dict, playlist_info: dict
) -> str:
    html = (
        html.replace("{artist.image}", track_data["artist_image_url"])
        .replace("{track.name}", track_data["track_name"])
        .replace("{track.artist}", track_data["artist_names"])
        .replace("{track.image}", track_data["track_image_url"])
        .replace("{track.url}", track_data["track_url"])
        .replace("{playlist.public_url}", playlist_info["public_url"])
        .replace("{playlist.name}", playlist_info["name"])
        .replace("{index.title}", environment["TITLE"])
        .replace("{index.favicon}", environment["FAVICON_URL"])
        .replace("{icon.github}", environment["GITHUB"])
        .replace("{icon.soundcloud}", environ["SOUNDCLOUD"])
        .replace("{icon.linkedin}", environment["LINKEDIN"])
        .replace("{track.addedBy.url}", track_data["added_by_public_url"])
        .replace("{track.addedBy.name}", track_data["added_by_name"])
    )

    return html


def lambda_handler(event, context) -> dict[str, Any]:
    try:
        html = open("index.html", "r").read()
        environment = get_environment()
        bearer_token = get_token(environment["CLIENT_ID"], environment["CLIENT_SECRET"])

        playlist_info = get_playlist_info(bearer_token, environment["PLAYLIST_ID"])

        track_data = get_random_track_data(
            playlist_info["total_tracks"], bearer_token, environment["PLAYLIST_ID"]
        )
        html = insert_data_in_template(html, track_data, environment, playlist_info)

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
            "body": dumps(
                {
                    "message": "I'm probably in the Bahamas, right now! Excuse me for the inconvenience. I will get it fixed once I'm back. <3",
                    "error": str(e),
                }
            ),
        }
