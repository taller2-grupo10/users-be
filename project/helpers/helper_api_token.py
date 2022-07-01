import os

import requests

API_TOKEN_URL = os.getenv("API_TOKEN_URL")
API_TOKEN = os.getenv("API_TOKEN")


class ApiTokenRequester:
    @staticmethod
    def get_tokens():
        response = requests.get(
            f"{API_TOKEN_URL}/list",
            headers={
                "Authorization": f"Bearer {API_TOKEN}",
            },
        )
        return response.json(), response.status_code

    @staticmethod
    def create_new_api_token(description):
        response = requests.post(
            f"{API_TOKEN_URL}/generate",
            headers={
                "Authorization": f"Bearer {API_TOKEN}",
            },
            json={"description": description},
        )
        return response.json(), response.status_code

    @staticmethod
    def delete_api_token(token):
        response = requests.post(
            f"{API_TOKEN_URL}/delete/{token}",
            headers={
                "Authorization": f"Bearer {API_TOKEN}",
            },
        )
        return response.json(), response.status_code

    @staticmethod
    def activate_token(token):
        response = requests.post(
            f"{API_TOKEN_URL}/activate/{token}",
            headers={
                "Authorization": f"Bearer {API_TOKEN}",
            },
        )
        return response.json(), response.status_code
