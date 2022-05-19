import base64
import json
import os

import requests
from flask import jsonify

MEDIA_URL = os.getenv("MEDIA_ENDPOINT", "http://localhost:3000")


class MediaRequester:
    @staticmethod
    def get(endpoint):
        response = requests.get(f"{MEDIA_URL}/{endpoint}")
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
        name = json.loads(files["data"])["title"]
        base64_bytes = files["files"].encode("ascii")
        message_bytes = base64.b64decode(base64_bytes)
        response = requests.post(
            f"{MEDIA_URL}/{endpoint}",
            files={
                "files": (
                    f"{name}.mp3",
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
        response = requests.delete(f"{MEDIA_URL}/{endpoint}")
        return response.json(), response.status_code
