from datetime import datetime
from urllib import response
from flask import Blueprint, request
from project.blueprints.media_artist_blueprint import ArtistById
from project.helpers.helper_auth import check_token
from project.helpers.helper_media import MediaRequester
from flask import jsonify
from flask_restx import Namespace, Resource, fields
from project.blueprints.media_genres_blueprint import music_genres_response_model
from firebase_admin import db
from project.config import Config
from exponent_server_sdk import (
    DeviceNotRegisteredError,
    PushClient,
    PushMessage,
    PushServerError,
    PushTicketError,
)
from requests.exceptions import ConnectionError, HTTPError
from project.controllers.user_controller import UserController

api = Namespace(name="Chat", path="/chat", description="Chat related endpoints")


def send_notification(sender, receiver, message):
    """
    Send notification to user
    """
    user_sender = UserController.get_user_by_uid(sender)
    user_receiver = UserController.get_user_by_uid(receiver)
    if user_sender is None or user_receiver is None:
        return
    user_sender_artist, status_code = ArtistById.get(user_sender.artist_id)
    if status_code != 200:
        return
    user_sender_artist_name = user_sender_artist.get("name")

    response = PushClient().publish(
        PushMessage(
            to=user_receiver.notification_token,
            title=f"New message from {user_sender_artist_name}!",
            body=message,
        )
    )
    try:
        # We got a response back, but we don't know whether it's an error yet.
        # This call raises errors so we can handle them with normal exception
        # flows.
        response.validate_response()
    except (DeviceNotRegisteredError, PushTicketError):
        # Mark the push token as inactive
        # TODO: logger
        pass


def upload_message(sender, receiver, message):
    """
    Upload message to firebase realtime database
    """
    db_ref = db.reference(url=Config.FIREBASE_DATABASE_URL)
    joined_uid = sender + "|" + receiver
    if receiver < sender:
        joined_uid = receiver + "|" + sender

    db_ref.child("messages").child(f"{joined_uid}").child(
        f"{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
    ).set(
        {
            "from": sender,
            "to": receiver,
            "message": message,
        }
    )


@api.route("")
class ChatHandler(Resource):

    # @check_token
    def post(self):
        """
        Uploads a chat message to the database
        """
        message = request.get_json().get("message")
        receiver = request.get_json().get("receiver")
        sender = request.get_json().get("uid")
        upload_message(sender, receiver, message)
        send_notification(sender, receiver, message)
        return {"message": "Message sent"}, 200
