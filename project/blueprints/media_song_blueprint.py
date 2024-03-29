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
                    "name": fields.String(required=False, description="Album name"),
                    "photoURL": fields.String(
                        required=False, description="Album photo URL"
                    ),
                },
            )
        ),
        "filename": fields.String(required=True, description="Song filename"),
        "genres": music_genres_response_model,
        "subscriptionLevel": fields.String(
            required=False, description="Subscription level"
        ),
        "isActive": fields.Boolean(required=False, description="Song is active"),
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
    @check_token
    @api.expect(song_model_upload, song_model)
    @api.response(200, "Success", song_response_model)
    @api.doc(
        responses={
            422: "{code: UPLOAD_MISSING_FILE || UPLOAD_MISSING_FILE}",
        }
    )
    def post(self):
        if "files" not in request.form:
            return (
                {"code": "UPLOAD_MISSING_FILE"},
                422,
            )
        if "data" not in request.form:
            return {"code": "UPLOAD_MISSING_DATA"}, 422

        response, status_code = MediaRequester.post_file("songs", files=request.form)
        return response, status_code

    @check_token
    @api.response(200, "Success", song_response_model)
    def get(self):
        response, status_code = MediaRequester.get(f"songs")
        return response, status_code


@api.route("/id/<id>", doc={"params": {"id": "Song id"}})
class SongsById(Resource):
    @check_token
    @api.response(200, "Success", song_response_model)
    def get(self, id):
        response, status_code = MediaRequester.get(f"songs/{id}")
        return response, status_code

    @check_token
    @api.expect(song_model)
    @api.response(200, "Success", song_response_model)
    def put(self, id):
        response, status_code = MediaRequester.put(f"songs/{id}", data=request.json)
        return response, status_code

    @check_token
    @api.response(200, "Success", song_response_model)
    def delete(self, id):
        response, status_code = MediaRequester.delete(f"songs/{id}")
        return response, status_code


@api.route("/name/<name>", doc={"params": {"name": "Song name"}})
class SongsByName(Resource):
    @check_token
    @api.response(200, "Success", song_response_model)
    def get(self, name):
        response, status_code = MediaRequester.get(
            f"songs/name/{name}", user_id=request.user.id
        )
        return response, status_code


@api.route("/album/<albumId>", doc={"params": {"albumId": "Album id"}})
class SongsByAlbumId(Resource):
    @check_token
    @api.response(200, "Success", song_response_model)
    def get(self, albumId):
        response, status_code = MediaRequester.get(
            f"songs/albumId/{albumId}", user_id=request.user.id
        )
        return response, status_code


@api.route("/artist/<artistId>", doc={"params": {"artistId": "Artist id"}})
class SongsByArtistId(Resource):
    @check_token
    @api.response(200, "Success", song_response_model)
    def get(self, artistId):
        response, status_code = MediaRequester.get(
            f"songs/artistId/{artistId}", user_id=request.user.id
        )
        return response, status_code


@api.route("/genre/<genreName>", doc={"params": {"genreName": "Genre name"}})
class SongsByGenreName(Resource):
    @check_token
    @api.response(200, "Success", song_response_model)
    def get(self, genreName):
        response, status_code = MediaRequester.get(
            f"songs/genre/{genreName}", user_id=request.user.id
        )
        return response, status_code


@api.route(
    "/subscription/<subscriptionLevel>",
    doc={"params": {"subscriptionLevel": "Subscription level"}},
)
class SongsBySubscriptionLevel(Resource):
    @check_token
    @api.response(200, "Success", song_response_model)
    def get(self, subscriptionLevel):
        response, status_code = MediaRequester.get(
            f"songs/subscription/{subscriptionLevel}"
        )
        return response, status_code
