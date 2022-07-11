import logging
from datetime import datetime

from firebase_admin import db
from flask import request
from flask_restx import Namespace, Resource, fields
from project.blueprints.media_artist_blueprint import ArtistById
from project.config import Config
from project.controllers.user_controller import UserController
from project.helpers.helper_auth import check_token
from project.helpers.helper_media import MediaRequester
from project.helpers.helper_notification import send_notification

api = Namespace(name="Chat", path="/chat", description="Chat related endpoints")

chat_model = api.model(
    "Chat",
    {
        "uid": fields.String(required=True, description="User ID"),
        "receiver": fields.String(required=True, description="Receiver ID"),
        "message": fields.String(required=True, description="Message"),
    },
)


def send_new_message_notification(sender_user, recv_uid, message):
    """
    Send notification to user
    """
    sender_uid = sender_user.uid
    sender_artist_id = sender_user.artist_id
    sender_artist, status_code = MediaRequester.get(f"artists/{sender_artist_id}")
    sender_name = sender_artist.get("name")
    recv_user = UserController.load_by_uid(recv_uid)

    title = f"New message from {sender_name}!"
    data = {"uid": sender_uid, "name": sender_name, "type": "message"}
    return send_notification(recv_user, title, message, data)


def upload_message(sender_uid, recv_uid, message):
    """
    Upload message to firebase realtime database
    """
    try:
        db_ref = db.reference(url=Config.FIREBASE_DATABASE_URL)
        joined_uid = sender_uid + "|" + recv_uid
        if recv_uid < sender_uid:
            joined_uid = recv_uid + "|" + sender_uid

        db_ref.child("messages").child(f"{joined_uid}").child(
            f"{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
        ).set(
            {
                "from": sender_uid,
                "to": recv_uid,
                "message": message,
            }
        )
        return True
    except:
        logging.error(f"Error uploading message to firebase. Chat: {joined_uid}")
        return False


@api.route("")
class ChatHandler(Resource):
    @check_token
    @api.expect(chat_model)
    @api.doc(
        responses={
            200: "{status: success, message: Message and notification sent}",
            400: "{status: error, message: Error sending notification / message}",
        }
    )
    def post(self):
        """
        Uploads a chat message to the database and sends a notification to the other user
        """
        sender_uid = request.user.uid
        recv_uid = request.get_json().get("receiver")
        message = request.get_json().get("message")

        upload_ok = upload_message(sender_uid, recv_uid, message)
        notification_ok = send_new_message_notification(request.user, recv_uid, message)
        if not upload_ok:
            return {"code": "FAILED_TO_UPLOAD_MESSAGE"}, 500
        if not notification_ok:
            return {"code": "FAILED_TO_SEND_NOTIFICATION"}, 500
        return {"code": "SUCCESS"}, 200


@api.route("/debug")
class ChatDebugHandler(Resource):
    def post(self):
        print(request.get_json())
        return {}, 200
