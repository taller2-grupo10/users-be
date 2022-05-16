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


def _put_artist(artist_id, request):
    return MediaRequester.put(f"artists/{artist_id}", data=request)


def _put_album(album_id, request):
    return MediaRequester.put(f"albums/{album_id}", data=request)


def _put_song(song_id, request):
    return MediaRequester.put(f"songs/{song_id}", data=request)


def _post_artist(request):
    return MediaRequester.post("artists", data=request)


def _post_album(request):
    return MediaRequester.post("albums", data=request)


def _post_song(request):
    return MediaRequester.post_file("songs", files=request)


# -----------------------------------------------------------------------------------
# Creators


@media_blueprint.route(f"{MEDIA_ENDPOINT}/{ARTISTS_ENDPOINT}", methods=["POST"])
# @check_token
def create_artist():
    response, status_code = _post_artist(request.json)
    return jsonify(response), status_code


@media_blueprint.route(f"{MEDIA_ENDPOINT}/{ALBUMS_ENDPOINT}", methods=["POST"])
# @check_token
def create_album():
    response, status_code = _post_album(request.json)
    return jsonify(response), status_code


@media_blueprint.route(f"{MEDIA_ENDPOINT}/{SONGS_ENDPOINT}", methods=["POST"])
# @check_token
def create_song():
    if "files" not in request.files:
        return (
            jsonify({"message": "Error while creating Song. Missing file."}),
            422,
        )
    if "data" not in request.files:
        return jsonify({"message": "Error while creating Song. Missing data."}), 422
    file = request.files["files"]
    if file.filename == "":
        return (
            jsonify({"message": "Error while creating Song. File without name."}),
            422,
        )
    response, status_code = _post_song(request.files)
    return jsonify(response), status_code


# -----------------------------------------------------------------------------------
# Updaters


@media_blueprint.route(f"{MEDIA_ENDPOINT}/{ARTISTS_ENDPOINT}", methods=["PUT"])
# @check_token
def update_artist():
    uid = request.json["uid"]
    artist, rc = MediaRequester.get(f"artists/{uid}")
    artist_id = artist[0]["_id"]

    albums, rc = MediaRequester.get(f"albums/artistId/{artist_id}")

    songs, rc = MediaRequester.get(f"songs/artistId/{artist_id}")

    for album in albums:
        album_id = album["_id"]
        album_request = {"artist.name": request.json["name"]}
        _put_album(album_id, album_request)

    for song in songs:
        song_id = song["_id"]
        song_artist_names = song["artists"]["names"]
        artist_name = artist[0]["name"]
        song_artist_names = list(filter(lambda x: x != artist_name, song_artist_names))
        song_artist_names.append(request.json["name"])

        song_request = {"artists.names": song_artist_names}
        _put_song(song_id, song_request)

    _put_artist(artist_id, request.json)

    return jsonify({"message": "Artist, albums and songs updated"}), 200


@media_blueprint.route(f"{MEDIA_ENDPOINT}/{ALBUMS_ENDPOINT}", methods=["PUT"])
# @check_token
def update_album():
    id = request.json["id"]

    album, rc = MediaRequester.get(f"albums/{id}")
    album_id = album["_id"]

    songs, rc = MediaRequester.get(f"songs/albumId/{album_id}")

    for song in songs:
        song_id = song["_id"]
        song_request = {"album.name": request.json["title"]}
        _put_song(song_id, song_request)

    _put_album(album_id, request.json)

    return jsonify({"message": "Album and Songs updated"}), 200


@media_blueprint.route(f"{MEDIA_ENDPOINT}/{SONGS_ENDPOINT}", methods=["PUT"])
# @check_token
def update_song():
    id = request.json["id"]
    print(f"request.json: {request.json}")
    _put_song(id, request.json)
    return jsonify({"message": "Song updated"}), 200


# -----------------------------------------------------------------------------------
# Deleters


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
