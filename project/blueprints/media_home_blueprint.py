import random
from urllib import response

from flask import Blueprint, jsonify, request
from flask_restx import Namespace, Resource, fields
from project.blueprints.media_album_blueprint import album_response_model
from project.blueprints.media_playlist_blueprint import playlist_response_model
from project.blueprints.media_song_blueprint import song_response_model
from project.controllers.user_controller import UserController
from project.helpers.helper_auth import check_token
from project.helpers.helper_media import MediaRequester
from project.helpers.helper_notification import send_notification

api = Namespace(
    name="Media Home", path="media/home", description="Home related endpoints"
)

home_model = api.model(
    "Home",
    {
        "songs": fields.List(
            fields.Nested(song_response_model, required=False, description="Songs")
        ),
        "playlists": fields.List(
            fields.Nested(
                playlist_response_model, required=False, description="Playlists"
            )
        ),
        "albums": fields.List(
            fields.Nested(album_response_model, required=False, description="Albums")
        ),
    },
)


@api.route("/<id>")
class Home(Resource):
    @check_token
    @api.response(200, "Success", home_model)
    def get(self, id):
        """
        Returns 5 random songs, 5 random playlists and 5 random albums.
        They are based on the user's preferences (location and genres).
        """
        data, status_code = MediaRequester.get(f"home/{id}", user_id=request.user.id)
        data["songs"] = random.sample(data["songs"], min(5, len(data["songs"])))
        data["playlists"] = random.sample(
            data["playlists"], min(5, len(data["playlists"]))
        )
        data["albums"] = random.sample(data["albums"], min(5, len(data["albums"])))

        return data, status_code
