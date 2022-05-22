from urllib import response
from flask import Blueprint, request
from project.helpers.helper_auth import check_token
from project.helpers.helper_media import MediaRequester
from flask import jsonify
from flask_restx import Namespace, Resource, fields
from project.blueprints.media_genres_blueprint import music_genres_response_model

api = Namespace(
    name="Albums", path="/media/albums", description="Albums related endpoints"
)

album_model = api.model(
    "Album",
    {
        "title": fields.String(required=True, description="Album title"),
        "description": fields.String(required=False, description="Album description"),
        "artist": fields.Nested(
            api.model(
                "Album.artist",
                {
                    "artist": fields.String(
                        required=True,
                        description="Artist identifier",
                    ),
                    "name": fields.String(required=True, description="Artist name"),
                },
            )
        ),
        "photoURL": fields.String(required=True, description="Album photo URL"),
        "genres": music_genres_response_model,
    },
)

album_response_model = api.inherit(
    "Album Response",
    album_model,
    {
        "plays": fields.Integer(required=False, description="Album plays"),
        "isDeleted": fields.Boolean(required=False, description="Album is deleted"),
        "likes": fields.Integer(required=False, description="Album likes"),
    },
)

album_put_model = api.model(
    "Album Put",
    {
        "title": fields.String(required=True, description="Album title"),
        "description": fields.String(required=False, description="Album description"),
        "photoURL": fields.String(required=True, description="Album photo URL"),
    },
)

album_put_response = api.model(
    "Album Put Response",
    {
        "message": fields.String(
            required=True,
            description="Album updated",
            example="Album and Songs updated",
        ),
        "data": fields.Nested(album_model),
    },
)

album_delete_response = api.model(
    "Album Put Response",
    {
        "message": fields.String(
            required=True,
            description="Album deleted",
            example="Album and Songs deleted",
        ),
        "data": fields.Nested(album_model),
    },
)


@api.route("")
class Albums(Resource):
    # @check_token
    @api.expect(album_model)
    @api.response(200, "Success", album_response_model)
    def post(self):
        response, status_code = MediaRequester.post("albums", data=request.json)
        return response, status_code

    # @check_token
    @api.response(200, "Success", album_response_model)
    def get(self):
        response, status_code = MediaRequester.get("albums")
        return response, status_code


@api.route("/id/<id>", doc={"params": {"id": "Album id"}})
class AlbumsById(Resource):
    # @check_token
    @api.response(200, "Success", album_response_model)
    def get(self, id):
        response, status_code = MediaRequester.get(f"albums/{id}")
        return response, status_code

    # @check_token
    @api.expect(album_put_model)
    @api.response(200, "Success", album_put_response)
    def put(self, id):
        songs, status_code = MediaRequester.get(f"songs/albumId/{id}")

        for song in songs:
            song_id = song["_id"]
            song_request = {"album.name": request.json["title"]}
            _put_song(song_id, song_request)

        album_put_response, status_code = MediaRequester.put(
            f"albums/{id}", data=request.json
        )

        return (
            jsonify({"message": "Album and Songs updated", "data": album_put_response}),
            200,
        )

    # @check_token
    @api.response(200, "Success", album_delete_response)
    def delete(self, id):
        songs, status_code = MediaRequester.get(f"songs/albumId/{id}")

        for song in songs:
            song_id = song["_id"]
            _delete_song(song_id)

        album_delete_response, status_code = MediaRequester.delete(f"albums/{id}")

        return (
            jsonify(
                {"message": "Album and Songs deleted", "data": album_delete_response}
            ),
            200,
        )


@api.route("/artist/<artist_id>", doc={"params": {"artist_id": "Artist id"}})
class AlbumsByArtist(Resource):
    # @check_token
    @api.response(200, "Success", album_response_model)
    def get(self, artist_id):
        response, status_code = MediaRequester.get(f"albums/artistId/{artist_id}")
        return response, status_code


def _delete_song(song_id):
    return MediaRequester.delete(f"songs/{song_id}")


def _put_song(song_id, request):
    return MediaRequester.put(f"songs/{song_id}", data=request)
