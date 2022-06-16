from project.controllers.user_controller import UserController
from project.blueprints.media_artist_blueprint import ArtistById
from exponent_server_sdk import (
    DeviceNotRegisteredError,
    PushClient,
    PushMessage,
    PushServerError,
    PushTicketError,
)


def send_notification(user, title, message):
    """
    Send notification to user
    """
    response = None
    try:
        response = PushClient().publish(
            PushMessage(
                to=user.notification_token,
                title=title,
                body=message,
            )
        )
    except PushServerError as err:
        return False

    try:
        # We got a response back, but we don't know whether it's an error yet.
        # This call raises errors so we can handle them with normal exception
        # flows.
        if response is None:
            return False
        response.validate_response()
        return True
    except (DeviceNotRegisteredError, PushTicketError) as err:
        # Mark the push token as inactive
        # TODO: logger
        pass
        return False
