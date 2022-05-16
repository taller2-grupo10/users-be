from urllib import response
from flask import Blueprint, request
from project.helpers.helper_auth import check_token
from project.helpers.helper_media import MediaRequester
from flask import jsonify
from flask_restx import Namespace, Resource, fields

namespace = Namespace(
    name="Songs", path="media/songs", description="Songs related endpoints"
)


@namespace.route("")
class Songs(Resource):
    # @check_token
    def post(self):
        if "files" not in request.files:
            return (
                jsonify({"message": "Error while creating Song. Missing file."}),
                422,
            )
        if "data" not in request.files:
            return jsonify({"message": "Error while creating Song. Missing data."}), 422
        file = request.files["files"]
        if file.filename == "":
            return (
                jsonify({"message": "Error while creating Song. File without name."}),
                422,
            )
        response, status_code = MediaRequester.post_file("songs", files=request.files)
        return response, status_code


@namespace.route("/id/<id>")
class SongsById(Resource):
    # @check_token
    def get(self, id):
        response, status_code = MediaRequester.get(f"songs/{id}")
        return response, status_code

    # @check_token
    def put(self, id):
        response, status_code = MediaRequester.put(f"songs/{id}", data=request.json)
        return response, status_code

    # @check_token
    def delete(self, id):
        response, status_code = MediaRequester.delete(f"songs/{id}")
        return response, status_code


@namespace.route("/name/<name>")
class SongsByName(Resource):
    # @check_token
    def get(self, name):
        response, status_code = MediaRequester.get(f"songs/name/{name}")
        return response, status_code


@namespace.route("/album/<albumId>")
class SongsByAlbumId(Resource):
    # @check_token
    def get(self, albumId):
        response, status_code = MediaRequester.get(f"songs/albumId/{albumId}")
        return response, status_code


@namespace.route("/artist/<artistId>")
class SongsByArtistId(Resource):
    # @check_token
    def get(self, artistId):
        response, status_code = MediaRequester.get(f"songs/artistId/{artistId}")
        return response, status_code
