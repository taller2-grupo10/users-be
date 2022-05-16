from urllib import response
from flask import Blueprint, request
from project.helpers.helper_auth import check_token
from project.helpers.helper_media import MediaRequester
from flask import jsonify
from flask_restx import Namespace, Resource, fields


namespace = Namespace(
    name="Artists", path="media/artists", description="Artists related endpoints"
)


@namespace.route("")
class Artists(Resource):
    # @check_token
    def get(self):
        response, status_code = MediaRequester.get(f"artists")
        return response, status_code

    # @check_token
    def post(self):
        response, status_code = MediaRequester.post("artists", data=request.json)
        return response, status_code


@namespace.route("/id/<id>")
class ArtistById(Resource):
    # @check_token
    def get(self, id):
        response, status_code = MediaRequester.get(f"artists/{id}")
        return response, status_code

    # @check_token
    def put(self):
        uid = request.json["uid"]  # TODO: front knows mongo id, no need to use uid
        artist, status_code = MediaRequester.get(f"artists/{uid}")
        artist_id = artist[0]["_id"]

        albums, status_code = MediaRequester.get(f"albums/artistId/{artist_id}")

        songs, status_code = MediaRequester.get(f"songs/artistId/{artist_id}")

        for album in albums:
            album_id = album["_id"]
            album_request = {"artist.name": request.json["name"]}
            _put_album(album_id, album_request)

        for song in songs:
            song_id = song["_id"]
            song_artist_names = song["artists"]["names"]
            artist_name = artist[0]["name"]
            song_artist_names = list(
                filter(lambda x: x != artist_name, song_artist_names)
            )
            song_artist_names.append(request.json["name"])

            song_request = {"artists.names": song_artist_names}
            _put_song(song_id, song_request)

        MediaRequester.put(f"artists/{artist_id}", data=request.json)

        return jsonify({"message": "Artist, albums and songs updated"}), 200

    # @check_token
    def delete(self):
        uid = request.json["uid"]
        artist, status_code = MediaRequester.get(f"artists/{uid}")
        artist_id = artist[0]["_id"]

        albums, status_code = MediaRequester.get(f"albums/artistId/{artist_id}")

        songs, status_code = MediaRequester.get(f"songs/artistId/{artist_id}")

        for album in albums:
            album_id = album["_id"]
            _delete_album(album_id)

        for song in songs:
            song_id = song["_id"]
            _delete_song(song_id)

        MediaRequester.delete(f"artists/{artist_id}")

        return jsonify({"message": "Artist, albums and songs deleted"}), 200


@namespace.route("/name/<name>")
class ArtistByName(Resource):
    # @check_token
    def get(self, name):
        response, status_code = MediaRequester.get(f"artists/name/{name}")
        return response, status_code


def _delete_album(album_id):
    return MediaRequester.delete(f"albums/{album_id}")


def _delete_song(song_id):
    return MediaRequester.delete(f"songs/{song_id}")


def _put_album(album_id, request):
    return MediaRequester.put(f"albums/{album_id}", data=request)


def _put_song(song_id, request):
    return MediaRequester.put(f"songs/{song_id}", data=request)
