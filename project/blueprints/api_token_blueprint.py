from flask import request
from flask_restx import Namespace, Resource
from project.helpers.helper_api_token import ApiTokenRequester
from project.helpers.helper_auth import check_token

api = Namespace(name="Api Token", path="api", description="Api Token related endpoints")


@api.route("/generate")
class GenerateToken(Resource):
    @check_token
    def post(self):
        description = request.json.get("description")
        return ApiTokenRequester.create_new_api_token(description)


@api.route("/delete/<token>")
class DeleteToken(Resource):
    @check_token
    def post(self, token):
        return ApiTokenRequester.delete_api_token(token)


@api.route("/activate/<token>")
class ActivateToken(Resource):
    @check_token
    def post(self, token):
        return ApiTokenRequester.activate_token(token)


@api.route("/list")
class ListTokens(Resource):
    @check_token
    def get(self):
        return ApiTokenRequester.get_tokens()
