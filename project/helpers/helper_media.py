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
        print("a")
        response = requests.post(
            f"{MEDIA_URL}/{endpoint}",
            files={
                "files": ("pepe", bytes(files["files"],"utf-8")),
                "data": files["data"],
            },
        )
        print("b")
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
