from flask import Blueprint, request
from flask_restx import Namespace, Resource, fields
from project import db
from project.helpers.helper_auth import check_token
from project.helpers.helper_logger import Logger
from project.helpers.helper_payments import PaymentRequester
from project.models.subscription import Subscription
from project.models.user_payment import UserPayment

api = Namespace(
    name="Payments", path="payments", description="Payments related endpoints"
)


@api.route("/deposit/<subscription_id>")
class PaymentDeposit(Resource):
    # @api.doc(security="Bearer")
    @check_token
    def post(self, subscription_id):
        wallet_id = request.user.wallet_id
        if not wallet_id:
            Logger.error(f"User {request.user.uid} has no wallet_id")
            return {"code": "NO_WALLET_FOUND"}, 404
        if not Subscription.query.filter_by(id=subscription_id).first():
            Logger.error(f"Subscription {subscription_id} not found")
            return {"code": "SUBSCRIPTION_NOT_FOUND"}, 404

        subscription = Subscription.query.get(subscription_id)
        response, status_code = PaymentRequester.deposit(
            wallet_id, subscription.price_in_ethers
        )
        if status_code != 200:
            code_error = response["code"]
            Logger.error(
                f"User {request.user.uid} failed to deposit {subscription.price_in_ethers} ethers to wallet {wallet_id}, with error: {code_error}"
            )
            return {"code": code_error}, status_code

        payment = UserPayment(request.user.id, subscription_id, response["hash"])
        try:
            db.session.add(payment)
            db.session.commit()
        except Exception as e:
            Logger.critical(f"Failed to add payment to database: {e}")
            return {"code": "DB_ERROR"}, 500
        return {"code": "SUCCESS"}, 201


@api.route("/balance")
class PaymentBalance(Resource):
    @check_token
    def get(self):
        wallet_id = request.user.wallet_id
        if not wallet_id:
            return {"code": "NO_WALLET_FOUND"}, 400
        response, status_code = PaymentRequester.get_balance(wallet_id)
        return response, status_code


@api.route("/check")
class PaymentChecker(Resource):
    @check_token
    def get(self):
        user_id = request.user.id
        response, status_code = PaymentRequester.get_subscription_level(user_id)
        return response, status_code
