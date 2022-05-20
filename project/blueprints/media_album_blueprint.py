from urllib import response
from flask import Blueprint, request
from project.helpers.helper_auth import check_token
from project.helpers.helper_media import MediaRequester
from flask import jsonify
from flask_restx import Namespace, Resource, fields

api = Namespace(
    name="Albums", path="/media/albums", description="Albums related endpoints"
)

album_model = api.model(
    "Album",
    {
        "title": fields.String(required=True, description="Album title"),
        "artist": fields.Nested(
            api.model(
                "Album.artist",
                {
                    "artist": fields.String(
                        required=True,
                        description="Artist identifier provided by Firebase",
                    ),
                    "name": fields.String(required=True, description="Artist name"),
                },
            )
        ),
        "plays": fields.Integer(required=False, description="Album plays"),
        "likes": fields.Integer(required=False, description="Album likes"),
        "photoURL": fields.String(required=True, description="Album photo URL"),
        "isDeleted": fields.Boolean(required=False, description="Album is deleted"),
    },
)


@api.route("")
class Albums(Resource):
    # @check_token
    @api.expect(album_model)
    @api.response(200, "Success", album_model)
    def post(self):
        response, status_code = MediaRequester.post("albums", data=request.json)
        return response, status_code


@api.route("/id/<id>", doc={"params": {"id": "Album id"}})
class AlbumsById(Resource):
    # @check_token
    @api.response(200, "Success", album_model)
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


@api.route("/artist/<artist_id>", doc={"params": {"artist_id": "Artist id"}})
class AlbumsByArtist(Resource):
    # @check_token
    @api.response(200, "Success", album_model)
    def get(self, artist_id):
        response, status_code = MediaRequester.get(f"albums/artistId/{artist_id}")
        return response, status_code


def _delete_song(song_id):
    return MediaRequester.delete(f"songs/{song_id}")


def _put_song(song_id, request):
    return MediaRequester.put(f"songs/{song_id}", data=request)
