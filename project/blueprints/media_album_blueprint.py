from urllib import response
from flask import Blueprint, request
from project.helpers.helper_auth import check_token
from project.helpers.helper_media import MediaRequester
from flask import jsonify
from flask_restx import Namespace, Resource, fields

namespace = Namespace(
    name="Albums", path="media/albums", description="Albums related endpoints"
)


@namespace.route("")
class Albums(Resource):
    # @check_token
    def post(self):
        response, status_code = MediaRequester.post("albums", data=request.json)
        return response, status_code


@namespace.route("/id/<id>")
class AlbumsById(Resource):
    # @check_token
    def get(self, id):
        response, status_code = MediaRequester.get(f"albums/{id}")
        return response, status_code

    # @check_token
    def put(self):
        id = request.json["id"]

        album, status_code = MediaRequester.get(f"albums/{id}")
        album_id = album["_id"]

        songs, status_code = MediaRequester.get(f"songs/albumId/{album_id}")

        for song in songs:
            song_id = song["_id"]
            song_request = {"album.name": request.json["title"]}
            _put_song(song_id, song_request)

        MediaRequester.put(f"albums/{album_id}", data=request.json)

        return jsonify({"message": "Album and Songs updated"}), 200

    # @check_token
    def delete(self):
        id = request.json["id"]

        album, status_code = MediaRequester.get(f"albums/{id}")
        album_id = album["_id"]

        songs, status_code = MediaRequester.get(f"songs/albumId/{album_id}")

        for song in songs:
            song_id = song["_id"]
            _delete_song(song_id)

        MediaRequester.delete(f"albums/{album_id}")

        return jsonify({"message": "Album and Songs deleted"}), 200


@namespace.route("/artist/<artist_id>")
class AlbumsByArtist(Resource):
    # @check_token
    def get(self, artist_id):
        response, status_code = MediaRequester.get(f"albums/artistId/{artist_id}")
        return response, status_code


def _delete_song(song_id):
    return MediaRequester.delete(f"songs/{song_id}")


def _put_song(song_id, request):
    return MediaRequester.put(f"songs/{song_id}", data=request)
