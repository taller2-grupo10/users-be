from flask import request
from flask_restx import Namespace, Resource, fields
from project.controllers.user_controller import UserController
from project.helpers.helper_auth import check_token
from project.helpers.helper_media import MediaRequester
from project.helpers.helper_notification import send_notification

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
        "isActive": fields.Boolean(required=False, default=True),
    },
)


@api.route("")
class Playlist(Resource):
    @check_token
    @api.expect(playlist_model)
    @api.response(201, "Success", playlist_response_model)
    def post(self):
        """
        Create a new playlist
        """
        response, status_code = MediaRequester.post("playlists", request.json)
        if status_code != 201:
            return response, status_code

        playlist_data = response
        for collaborator_artist_id in playlist_data.get("collaborators") or []:
            send_new_collaborator_notification(
                request.user,
                collaborator_artist_id,
                playlist_data.get("title"),
                playlist_data.get("_id"),
            )
        return response, status_code

    @check_token
    @api.response(200, "Success", playlist_response_model)
    def get(self):
        response, status_code = MediaRequester.get(f"playlists")
        return response, status_code


@api.route("/id/<id>", doc={"params": {"id": "Playlist id"}})
class PlaylistById(Resource):
    @check_token
    @api.response(200, "Success", playlist_response_model)
    def get(self, id):
        response, status_code = MediaRequester.get(
            f"playlists/{id}", user_id=request.user.id
        )
        return response, status_code

    @check_token
    @api.expect(playlist_model)
    @api.response(200, "Success", playlist_response_model)
    def put(self, id):
        playlist_old_data, status_code = MediaRequester.get(f"playlists/{id}")

        response, status_code = MediaRequester.put(f"playlists/{id}", request.json)
        if status_code != 200:
            return response, status_code

        playlist_new_data = response
        for collaborator_artist_id in playlist_new_data.get("collaborators") or []:
            if collaborator_artist_id not in playlist_old_data.get("collaborators"):
                send_new_collaborator_notification(
                    request.user,
                    collaborator_artist_id,
                    playlist_new_data.get("title"),
                    id,
                )
        return response, status_code

    @check_token
    @api.response(200, "Success", playlist_response_model)
    def delete(self, id):
        response, status_code = MediaRequester.delete(f"playlists/{id}")
        return response, status_code


@api.route("/user/<id>", doc={"params": {"id": "User/Artist id"}})
class PlaylistByUser(Resource):
    @check_token
    @api.response(200, "Success", playlist_response_model)
    def get(self, id):
        response, status_code = MediaRequester.get(
            f"playlists/userId/{id}", user_id=request.user.id
        )
        return response, status_code


def send_new_collaborator_notification(
    sender_user, collaborator, playlist_title, playlist_id
):
    """
    Send a notification to the collaborator that they have been added to a playlist
    """
    sender_uid = sender_user.uid
    sender_artist_id = sender_user.artist_id
    sender_artist, status_code = MediaRequester.get(f"artists/{sender_artist_id}")
    sender_name = sender_artist.get("name")
    recv_user = UserController.load_by_artist_id(collaborator)
    if recv_user is None:
        return True

    title = f"{sender_name} added you as collaborator to their Playlist!"
    data = {
        "uid": sender_uid,
        "name": sender_name,
        "type": "playlist_add",
        "playlistId": playlist_id,
    }
    message = (
        f"{sender_name} added you as collaborator to their Playlist: {playlist_title}"
    )
    return send_notification(recv_user, title, message, data)
