from flask import Blueprint, request
from project.helpers.helper_auth import check_token
from flask_restx import Namespace, Resource, fields
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
        if not wallet_id or not subscription_id:
            return {"message": "No wallet/subscription id found"}, 400

        subscription = Subscription.query.get(subscription_id)
        response, status_code = PaymentRequester.deposit(
            wallet_id, subscription.price_in_ethers
        )
        payment = UserPayment(request.user.id, subscription_id, response["hash"])
        # TODO: move to controller
        from project import db

        db.session.add(payment)
        db.session.commit()
        #
        return response, status_code


@api.route("/balance")
class PaymentBalance(Resource):
    @check_token
    def get(self):
        wallet_id = request.user.wallet_id
        if not wallet_id:
            return {"message": "No wallet id found"}, 400
        response, status_code = PaymentRequester.get_balance(wallet_id)
        return response, status_code


# TODO: no need to be endpoint, just return the subscription level
@api.route("/check")
class PaymentChecker(Resource):
    @check_token
    def get(self):
        user_id = request.user.id
        response, status_code = PaymentRequester.get_subscription_level(user_id)
        return response, status_code
