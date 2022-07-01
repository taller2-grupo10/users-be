import base64
import json
import os

import requests

from project.helpers.helper_payments import PaymentRequester

MEDIA_URL = os.getenv("MEDIA_ENDPOINT", "http://localhost:3000")
from project.helpers.helper_api_token import API_TOKEN


class MediaRequester:
    @staticmethod
    def get(endpoint, user_id=None):
        subscription_query = ""
        if user_id is not None:
            (
                max_subscription_level,
                status_code,
            ) = PaymentRequester.get_subscription_level(user_id)
            if status_code == 200:
                subscription_query = "?subscriptionLevel=" + str(max_subscription_level)
        response = requests.get(f"{MEDIA_URL}/{endpoint}{subscription_query}", 
              headers={
                "api_media": API_TOKEN,
              },)
        return response.json(), response.status_code

    @staticmethod
    def post(endpoint, data):
        response = requests.post(
            f"{MEDIA_URL}/{endpoint}",
            headers={
                "Content-Type": "application/json",
                "api_media": API_TOKEN,
            },
            json=data,
        )
        return response.json(), response.status_code

    @staticmethod
    def post_file(endpoint, files):
        filename = json.loads(files["data"])["filename"]
        base64_bytes = files["files"].encode("ascii")
        message_bytes = base64.b64decode(base64_bytes)
        response = requests.post(
            f"{MEDIA_URL}/{endpoint}",
            files={
                "files": (
                    filename,
                    message_bytes,
                ),
                "data": files["data"],
            },
            headers={"api_media": API_TOKEN},
        )
        return response.json(), response.status_code

    @staticmethod
    def put(endpoint, data):
        response = requests.put(
            f"{MEDIA_URL}/{endpoint}",
            headers={
                "Content-Type": "application/json",
                "api_media": API_TOKEN,
            },
            json=data,
        )
        return response.json(), response.status_code

    @staticmethod
    def delete(endpoint):
        response = response = requests.put(
            f"{MEDIA_URL}/{endpoint}",
            headers={
                "Content-Type": "application/json",
                "api_media": API_TOKEN,
            },
            json={"isDeleted": True},
        )
        return response.json(), response.status_code
