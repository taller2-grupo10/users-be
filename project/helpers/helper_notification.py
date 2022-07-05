from exponent_server_sdk import (
    DeviceNotRegisteredError,
    PushClient,
    PushMessage,
    PushServerError,
    PushTicketError,
)
from project.helpers.helper_logger import Logger


def send_notification(user, title, message, data):
    """
    Send notification to user
    """
    response = None
    if not user or not user.notification_token:
        return True  # no user/notificion token found -> does not mean erorr
    try:
        response = PushClient().publish(
            PushMessage(
                to=user.notification_token, title=title, body=message, data=data
            )
        )
    except PushServerError as err:
        Logger.warn(f"Failed to send notification to user {user.uid}")
        return False

    try:
        # We got a response back, but we don't know whether it's an error yet.
        # This call raises errors so we can handle them with normal exception
        # flows.
        if response is None:
            Logger.warn(
                f"Failed to obtain response from Push Notification Service {user.uid}"
            )
            return False
        response.validate_response()
        return True
    except (DeviceNotRegisteredError, PushTicketError) as err:
        Logger.warn(f"Failed to send notification to user {user.uid}")
        return False
