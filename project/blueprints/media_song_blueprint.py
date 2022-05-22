from urllib import response
from flask import Blueprint, request
from project.helpers.helper_auth import check_token
from project.helpers.helper_media import MediaRequester
from flask import jsonify
from flask_restx import Namespace, Resource, fields
from project.blueprints.media_genres_blueprint import music_genres_response_model

api = Namespace(name="Songs", path="media/songs", description="Songs related endpoints")

song_model_upload = api.parser()
song_model_upload.add_argument(
    "files", type="FileStorage", help="Song file", location="files"
)
song_model_upload.add_argument(
    "'data' json containing payload specified below", type="json", location="form"
)

song_model = api.model(
    "Song",
    {
        "title": fields.String(required=True, description="Song title"),
        "artists": fields.Nested(
            api.model(
                "Song.artists",
                {
                    "artist": fields.String(
                        required=True,
                        description="Artist identifier",
                    ),
                    "name": fields.String(required=True, description="Artist name"),
                    "collaborators": fields.List(
                        fields.String(
                            required=False,
                            description="Collaborator artist identifier",
                        )
                    ),
                    "collaboratorsNames": fields.List(
                        fields.String(
                            required=False,
                            description="Collaborator artist name",
                        )
                    ),
                },
            )
        ),
        "album": fields.Nested(
            api.model(
                "Song.album",
                {
                    "album": fields.String(
                        required=True,
                        description="Album identifier",
                    ),
                    "name": fields.String(required=True, description="Album name"),
                },
            )
        ),
        "genres": music_genres_response_model,
    },
)

song_response_model = api.inherit(
    "Song Response",
    song_model,
    {
        "plays": fields.Integer(required=False, description="Song plays"),
        "isDeleted": fields.Boolean(required=False, description="Song is deleted"),
        "url": fields.String(required=True, description="Song url"),
    },
)


@api.route("")
class Songs(Resource):
    # @check_token
    @api.expect(song_model_upload, song_model)
    @api.response(200, "Success", song_response_model)
    @api.doc(
        responses={
            400: "{message: Error while creating Song. Missing file. || Error while creating Song. Missing data.}",
        }
    )
    def post(self):
        if "files" not in request.form:
            return (
                {"message": "Error while creating Song. Missing file."},
                422,
            )
        if "data" not in request.form:
            return {"message": "Error while creating Song. Missing data."}, 422

        response, status_code = MediaRequester.post_file("songs", files=request.form)
        return response, status_code

    # @check_token
    @api.response(200, "Success", song_response_model)
    def get(self):
        response, status_code = MediaRequester.get("songs")
        return response, status_code


@api.route("/id/<id>", doc={"params": {"id": "Song id"}})
class SongsById(Resource):
    # @check_token
    @api.response(200, "Success", song_response_model)
    def get(self, id):
        response, status_code = MediaRequester.get(f"songs/{id}")
        return response, status_code

    # @check_token
    @api.expect(song_model)
    @api.response(200, "Success", song_response_model)
    def put(self, id):
        response, status_code = MediaRequester.put(f"songs/{id}", data=request.json)
        return response, status_code

    # @check_token
    @api.response(200, "Success", song_response_model)
    def delete(self, id):
        response, status_code = MediaRequester.delete(f"songs/{id}")
        return response, status_code


@api.route("/name/<name>", doc={"params": {"name": "Song name"}})
class SongsByName(Resource):
    # @check_token
    @api.response(200, "Success", song_response_model)
    def get(self, name):
        response, status_code = MediaRequester.get(f"songs/name/{name}")
        return response, status_code


@api.route("/album/<albumId>", doc={"params": {"albumId": "Album id"}})
class SongsByAlbumId(Resource):
    # @check_token
    @api.response(200, "Success", song_response_model)
    def get(self, albumId):
        response, status_code = MediaRequester.get(f"songs/albumId/{albumId}")
        return response, status_code


@api.route("/artist/<artistId>", doc={"params": {"artistId": "Artist id"}})
class SongsByArtistId(Resource):
    # @check_token
    @api.response(200, "Success", song_response_model)
    def get(self, artistId):
        response, status_code = MediaRequester.get(f"songs/artistId/{artistId}")
        return response, status_code
