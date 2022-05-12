from urllib import response
from flask import Blueprint, request
from project.helpers.helper_auth import check_token
from project.helpers.helper_media import MediaRequester
from flask import jsonify

media_blueprint = Blueprint("media_blueprint", __name__)
MEDIA_ENDPOINT = "/media"
ARTISTS_ENDPOINT = "artists"
ALBUMS_ENDPOINT = "albums"
SONGS_ENDPOINT = "songs"


@media_blueprint.route(f"{MEDIA_ENDPOINT}/{ARTISTS_ENDPOINT}", methods=["GET"])
# @check_token
def get_all_artists():
    response, status_code = MediaRequester.get(f"artists")
    return jsonify(response), status_code


@media_blueprint.route(f"{MEDIA_ENDPOINT}/{ALBUMS_ENDPOINT}", methods=["GET"])
# @check_token
def get_all_albums():
    response, status_code = MediaRequester.get("albums")
    return jsonify(response), status_code


@media_blueprint.route(f"{MEDIA_ENDPOINT}/{SONGS_ENDPOINT}", methods=["GET"])
# @check_token
def get_all_songs():
    response, status_code = MediaRequester.get("songs")
    return jsonify(response), status_code


# -----------------------------------------------------------------------------------


def _delete_artist(artist_id):
    return MediaRequester.delete(f"artists/{artist_id}")


def _delete_album(album_id):
    return MediaRequester.delete(f"albums/{album_id}")


def _delete_song(song_id):
    return MediaRequester.delete(f"songs/{song_id}")


# -----------------------------------------------------------------------------------


@media_blueprint.route(f"{MEDIA_ENDPOINT}/{ARTISTS_ENDPOINT}", methods=["DELETE"])
# @check_token
def delete_artist():
    uid = request.json["uid"]
    artist, rc = MediaRequester.get(f"artists/{uid}")
    artist_id = artist[0]["_id"]

    albums, rc = MediaRequester.get(f"albums/artistId/{artist_id}")

    songs, rc = MediaRequester.get(f"songs/artistId/{artist_id}")

    for album in albums:
        album_id = album["_id"]
        _delete_album(album_id)

    for song in songs:
        song_id = song["_id"]
        _delete_song(song_id)

    _delete_artist(artist_id)

    return jsonify({"message": "Artist, albums and songs deleted"}), 200


@media_blueprint.route(f"{MEDIA_ENDPOINT}/{ALBUMS_ENDPOINT}", methods=["DELETE"])
# @check_token
def delete_album():
    id = request.json["id"]

    album, rc = MediaRequester.get(f"albums/{id}")
    album_id = album["_id"]

    songs, rc = MediaRequester.get(f"songs/albumId/{album_id}")

    for song in songs:
        song_id = song["_id"]
        _delete_song(song_id)

    _delete_album(album_id)

    return jsonify({"message": "Album and Songs deleted"}), 200


@media_blueprint.route(f"{MEDIA_ENDPOINT}/{SONGS_ENDPOINT}", methods=["DELETE"])
# @check_token
def delete_song():
    id = request.json["id"]
    _delete_song(id)
    return jsonify({"message": "Song deleted"}), 200
