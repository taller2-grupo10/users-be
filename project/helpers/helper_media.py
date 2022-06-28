import base64
import json
import os

import requests
from flask import jsonify

from project.helpers.helper_payments import PaymentRequester

MEDIA_URL = os.getenv("MEDIA_ENDPOINT", "http://localhost:3000")


class MediaRequester:
    @staticmethod
    def get(endpoint, request):
        max_subscription_level, status_code = PaymentRequester.get_subscription_level(
            request.user.id
        )
        subscription_query = "?subscriptionLevel=" + str(max_subscription_level)
        if status_code != 200:
            subscription_query = ""
        response = requests.get(f"{MEDIA_URL}/{endpoint}{subscription_query}")
        return response.json(), response.status_code

    @staticmethod
    def post(endpoint, data):
        response = requests.post(
            f"{MEDIA_URL}/{endpoint}",
            headers={"Content-Type": "application/json"},
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
        )
        return response.json(), response.status_code

    @staticmethod
    def put(endpoint, data):
        response = requests.put(
            f"{MEDIA_URL}/{endpoint}",
            headers={"Content-Type": "application/json"},
            json=data,
        )
        return response.json(), response.status_code

    @staticmethod
    def delete(endpoint):
        response = response = requests.put(
            f"{MEDIA_URL}/{endpoint}",
            headers={"Content-Type": "application/json"},
            json={"isDeleted": True},
        )
        return response.json(), response.status_code
