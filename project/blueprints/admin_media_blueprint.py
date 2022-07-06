from urllib import response
from flask import Blueprint, request
from project.helpers.helper_auth import check_permissions, check_token
from project.helpers.helper_media import MediaRequester
from flask import jsonify
from flask_restx import Namespace, Resource, fields
from project.blueprints.media_song_blueprint import song_response_model
from project.blueprints.media_playlist_blueprint import playlist_response_model
from project.blueprints.media_album_blueprint import album_response_model

api = Namespace(
    name="Admin Media", path="admin/media", description="Admin Media related endpoints"
)

# Songs
@api.route("/songs")
class AdminSong(Resource):
    @check_token
    @check_permissions(["admin_list"])
    @api.response(200, "Success", song_response_model)
    def get(self):
        response, status_code = MediaRequester.get("songs/noFilter/all")
        return response, status_code


@api.route("/songs/enable/<id>")
class AdminSongEnable(Resource):
    @check_token
    @check_permissions(["admin_modify"])
    @api.response(200, "Success", song_response_model)
    def post(self, id):
        response, status_code = MediaRequester.put(
            f"songs/{id}", data={"isActive": True}
        )
        return response, status_code


@api.route("/songs/disable/<id>")
class AdminSongDisable(Resource):
    @check_token
    @check_permissions(["admin_modify"])
    @api.response(200, "Success", song_response_model)
    def post(self, id):
        response, status_code = MediaRequester.put(
            f"songs/{id}", data={"isActive": False}
        )
        return response, status_code


# Playlists
@api.route("/playlists")
class AdminPlaylist(Resource):
    @check_token
    @check_permissions(["admin_list"])
    @api.response(200, "Success", playlist_response_model)
    def get(self):
        response, status_code = MediaRequester.get("playlists/noFilter/all")
        return response, status_code


@api.route("/playlists/enable/<id>")
class AdminPlaylistEnable(Resource):
    @check_token
    @check_permissions(["admin_modify"])
    @api.response(200, "Success", playlist_response_model)
    def post(self, id):
        response, status_code = MediaRequester.put(
            f"playlists/{id}", data={"isActive": True}
        )
        return response, status_code


@api.route("/playlists/disable/<id>")
class AdminPlaylistDisable(Resource):
    @check_token
    @check_permissions(["admin_modify"])
    @api.response(200, "Success", playlist_response_model)
    def post(self, id):
        response, status_code = MediaRequester.put(
            f"playlists/{id}", data={"isActive": False}
        )
        return response, status_code


# Albums
@api.route("/albums")
class AdminAlbum(Resource):
    @check_token
    @check_permissions(["admin_list"])
    @api.response(200, "Success", album_response_model)
    def get(self):
        response, status_code = MediaRequester.get("albums/noFilter/all")
        return response, status_code


@api.route("/albums/enable/<id>")
class AdminAlbumEnable(Resource):
    @check_token
    @check_permissions(["admin_modify"])
    @api.response(200, "Success", album_response_model)
    def post(self, id):
        response, status_code = MediaRequester.put(
            f"albums/{id}", data={"isActive": True}
        )
        return response, status_code


@api.route("/albums/disable/<id>")
class AdminAlbumDisable(Resource):
    @check_token
    @check_permissions(["admin_modify"])
    @api.response(200, "Success", album_response_model)
    def post(self, id):
        response, status_code = MediaRequester.put(
            f"albums/{id}", data={"isActive": False}
        )
        return response, status_code
