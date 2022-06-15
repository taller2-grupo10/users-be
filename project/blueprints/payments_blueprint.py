from urllib import response
from flask import Blueprint, request
from project.helpers.helper_auth import check_token
from flask import jsonify
from flask_restx import Namespace, Resource, fields
from project.blueprints.media_genres_blueprint import music_genres_response_model
from project.helpers.helper_payments import PaymentRequester

api = Namespace(
    name="Payments", path="payments", description="Payments related endpoints"
)


@api.route("/deposit")
class PaymentDeposit(Resource):
    # @api.doc(security="Bearer")
    @check_token
    def post(self):
        wallet_id = request.user.wallet_id
        if not wallet_id:
            return {"message": "No wallet id found"}, 400
        amount_in_ethers = request.json["amountInEthers"]
        response, status_code = PaymentRequester.deposit(wallet_id, amount_in_ethers)
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
