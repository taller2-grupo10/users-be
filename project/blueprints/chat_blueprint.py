from datetime import datetime

from firebase_admin import db
from flask import request
from flask_restx import Namespace, Resource, fields
from project.blueprints.media_artist_blueprint import ArtistById
from project.config import Config
from project.helpers.helper_auth import check_token
from project.helpers.helper_notification import send_notification
from project.models.user import User

api = Namespace(name="Chat", path="/chat", description="Chat related endpoints")

chat_model = api.model(
    "Chat",
    {
        "uid": fields.String(required=True, description="User ID"),
        "receiver": fields.String(required=True, description="Receiver ID"),
        "message": fields.String(required=True, description="Message"),
    },
)


def send_new_message_notification(sender_artist_id, recv_artist_id, message):
    """
    Send notification to user
    """
    sender_artist = ArtistById.get(sender_artist_id)
    sender_name = sender_artist.get("name")
    recv_user = User.query.filter_by(artist_id=recv_artist_id).first()

    title = (f"New message from {sender_name}!",)
    send_notification(recv_user, title, message)


def upload_message(sender_artist_id, recv_artist_id, message):
    """
    Upload message to firebase realtime database
    """
    try:
        db_ref = db.reference(url=Config.FIREBASE_DATABASE_URL)
        joined_uid = sender_artist_id + "|" + recv_artist_id
        if recv_artist_id < sender_artist_id:
            joined_uid = recv_artist_id + "|" + sender_artist_id

        db_ref.child("messages").child(f"{joined_uid}").child(
            f"{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
        ).set(
            {
                "from": sender_artist_id,
                "to": recv_artist_id,
                "message": message,
            }
        )
        return True
    except:
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
        sender_artist_id = request.user.artist_id
        recv_artist_id = request.get_json().get("receiver")
        message = request.get_json().get("message")

        upload_ok = upload_message(sender_artist_id, recv_artist_id, message)
        notification_ok = send_new_message_notification(
            sender_artist_id, recv_artist_id, message
        )
        if not upload_ok:
            return {"status": "error", "message": "Error sending message"}, 400
        elif not notification_ok:
            return {"status": "error", "message": "Error sending notification"}, 400
        else:
            return {
                "status": "success",
                "message": "Message and notification sent",
            }, 200
