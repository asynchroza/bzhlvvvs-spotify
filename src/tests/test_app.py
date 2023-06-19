from src.app import insert_data_in_template, _get
import pytest

def test_insert_data_in_template():
    html = """
    <html>
        <body>
            <img src="{artist.image}" alt="Artist Image">
            <h1>{track.name}</h1>
            <p>Artist: {track.artist}</p>
            <img src="{track.image}" alt="Track Image">
            <a href="{track.url}">Listen to Track</a>
            <a href="{playlist.public_url}">View Playlist</a>
            <h2>{playlist.name}</h2>
            <h3>{index.title}</h3>
            <link rel="icon" href="{index.favicon}">
            <a href="{icon.github}">GitHub</a>
            <a href="{icon.linkedin}">LinkedIn</a>
        </body>
    </html>
    """

    track_data = {
        "artist_image_url": "https://example.com/artist_image.jpg",
        "track_name": "Track Name",
        "artist_names": "Artist Name",
        "track_image_url": "https://example.com/track_image.jpg",
        "track_url": "https://example.com/track_url",
    }

    playlist_info = {
        "public_url": "https://example.com/playlist",
        "name": "Playlist Name",
    }

    environment = {
        "TITLE": "Page Title",
        "FAVICON_URL": "https://example.com/favicon.ico",
        "GITHUB": "https://github.com/example",
        "LINKEDIN": "https://linkedin.com/example",
    }

    expected_result = """
    <html>
        <body>
            <img src="https://example.com/artist_image.jpg" alt="Artist Image">
            <h1>Track Name</h1>
            <p>Artist: Artist Name</p>
            <img src="https://example.com/track_image.jpg" alt="Track Image">
            <a href="https://example.com/track_url">Listen to Track</a>
            <a href="https://example.com/playlist">View Playlist</a>
            <h2>Playlist Name</h2>
            <h3>Page Title</h3>
            <link rel="icon" href="https://example.com/favicon.ico">
            <a href="https://github.com/example">GitHub</a>
            <a href="https://linkedin.com/example">LinkedIn</a>
        </body>
    </html>
    """

    result = insert_data_in_template(html, track_data, environment, playlist_info)
    assert result == expected_result

def test_get():
    obj = {
        "key1": "value1",
        "key2": "value2",
    }

    # should return value
    result = _get(obj, "key1")
    assert result == "value1"

    # should return empty string because throw is implicitly False
    result = _get(obj, "key3")
    assert result == ""

    # should throw when key is missing
    with pytest.raises(Exception) as exc_info:
        _get(obj, "key3", throw=True)
    assert str(exc_info.value) == "'key3' key was not found in dictionary"

    # should return default value because throw is implicitly False
    result = _get(obj, "key3", default_value="default")
    assert result == "default"