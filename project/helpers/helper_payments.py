import os
import requests

PAYMENT_URL = os.getenv("PAYMENT_ENDPOINT", "http://0.0.0.0:7000")


class PaymentRequester:
    @staticmethod
    def create_wallet():
        response = requests.post(
            f"{PAYMENT_URL}/wallet",
        )
        return response.json(), response.status_code

    @staticmethod
    def get_address(wallet_id):
        response = requests.get(f"{PAYMENT_URL}/wallet/{wallet_id}")
        return response.json(), response.status_code

    @staticmethod
    def deposit(sender_id, amount_in_ethers):
        response = requests.post(
            f"{PAYMENT_URL}/deposit",
            json={"senderId": sender_id, "amountInEthers": amount_in_ethers},
        )
        return response.json(), response.status_code

    @staticmethod
    def get_balance(wallet_id):
        response = requests.get(f"{PAYMENT_URL}/balance/{wallet_id}")
        return response.json(), response.status_code
