from flask import request
from project.helpers.helper_auth import check_token
from project.helpers.helper_media import MediaRequester
from flask_restx import Namespace, Resource, fields

api = Namespace(
    name="Playlists", path="media/playlists", description="Playlists related endpoints"
)

playlist_model = api.model(
    "Playlist",
    {
        "title": fields.String(required=True),
        "description": fields.String(required=True),
        "owner": fields.String(required=True),
        "collaborators": fields.List(fields.String),
        "songs": fields.List(fields.String),
    },
)

playlist_response_model = api.inherit(
    "PlaylistResponse",
    playlist_model,
    {
        "_id": fields.String(required=False),
        "createdAt": fields.DateTime(required=False),
        "updatedAt": fields.DateTime(required=False),
        "plays": fields.Integer(required=False, default=0),
        "isDeleted": fields.Boolean(required=False, default=False),
    },
)


@api.route("")
class Playlist(Resource):

    # @check_token
    @api.expect(playlist_model)
    @api.response(200, "Success", playlist_response_model)
    def post(self):
        """
        Create a new playlist
        """
        response, status_code = MediaRequester.post("playlists", request.json)
        return response, status_code


@api.route("/id/<id>", doc={"params": {"id": "Playlist id"}})
class PlaylistById(Resource):
    # @check_token
    @api.response(200, "Success", playlist_response_model)
    def get(self, id):
        response, status_code = MediaRequester.get(
            f"playlists/{id}", user_id=request.user.id
        )
        return response, status_code

    # @check_token
    @api.expect(playlist_model)
    @api.response(200, "Success", playlist_response_model)
    def put(self, id):
        response, status_code = MediaRequester.put(f"playlists/{id}", request.json)
        return response, status_code

    # @check_token
    @api.response(200, "Success", playlist_response_model)
    def delete(self, id):
        response, status_code = MediaRequester.delete(f"playlists/{id}")
        return response, status_code


@api.route("/user/<id>", doc={"params": {"id": "User/Artist id"}})
class PlaylistByUser(Resource):
    # @check_token
    @api.response(200, "Success", playlist_response_model)
    def get(self, id):
        response, status_code = MediaRequester.get(
            f"playlists/userId/{id}", user_id=request.user.id
        )
        return response, status_code
