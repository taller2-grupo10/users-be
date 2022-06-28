import os
import requests
from project.models.user_payment import UserPayment

PAYMENT_URL = os.getenv("PAYMENT_ENDPOINT", "http://0.0.0.0:7000")


class PaymentRequester:
    @staticmethod
    def create_wallet():
        response = requests.post(
            f"{PAYMENT_URL}/wallet",
            headers={"api_payments": os.getenv("API_TOKEN")},
        )
        return response.json(), response.status_code

    @staticmethod
    def get_address(wallet_id):
        response = requests.get(
            f"{PAYMENT_URL}/wallet/{wallet_id}",
            headers={"api_payments": os.getenv("API_TOKEN")},
        )
        return response.json(), response.status_code

    @staticmethod
    def deposit(sender_id, amount_in_ethers):
        response = requests.post(
            f"{PAYMENT_URL}/deposit",
            json={"senderId": sender_id, "amountInEthers": str(amount_in_ethers)},
            headers={"api_payments": os.getenv("API_TOKEN")},
        )
        return response.json(), response.status_code

    @staticmethod
    def get_balance(wallet_id):
        response = requests.get(
            f"{PAYMENT_URL}/balance/{wallet_id}",
            headers={"api_payments": os.getenv("API_TOKEN")},
        )
        return response.json(), response.status_code

    @staticmethod
    def get_subscription_level(user_id):
        payments = UserPayment.query.filter_by(user_id=user_id).all()
        payments.sort(key=lambda x: x.created_at)
        max_subscription_level = 0
        for payment in payments:
            response = requests.get(
                f"{PAYMENT_URL}/deposit/{payment.transaction_hash}",
                headers={"api_payments": os.getenv("API_TOKEN")},
            )
            if (
                response.status_code == 200
                and payment.subscription_id > max_subscription_level
            ):
                max_subscription_level = payment.subscription_id
        return max_subscription_level, 200
