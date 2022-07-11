from pydoc import doc
from urllib import response
from flask import Blueprint, request
from project.helpers.helper_artist import delete_artist, edit_artist
from project.helpers.helper_auth import check_token
from project.helpers.helper_media import MediaRequester
from flask import jsonify
from flask_restx import Namespace, Resource, fields


api = Namespace(
    name="Artists", path="/media/artists", description="Artists related endpoints"
)

artist_post_model = api.model(
    "Artist Post",
    {
        "name": fields.String(required=True, description="Artist name"),
        "uid": fields.String(
            required=True, description="Artist identifier provided by Firebase"
        ),
        "isDeleted": fields.Boolean(required=False, description="Artist is deleted"),
        "plays": fields.Integer(required=False, description="Artist plays"),
        "location": fields.String(
            required=False,
            description="Any of these locations: 'North America','South America','Central America','Europe','Asia','Africa','Oceania','Antarctica'",
        ),
    },
)

artist_put_model = api.model(
    "Artist Put",
    {
        "name": fields.String(required=True, description="Artist name"),
    },
)

artist_response_model = api.inherit(
    "Artist Response",
    artist_post_model,
    {
        "_id": fields.String(required=False, description="Artist id"),
        "createdAt": fields.DateTime(required=False, description="Artist created at"),
        "updatedAt": fields.DateTime(required=False, description="Artist updated at"),
    },
)

artist_put_response_model = api.model(
    "Artist Put Response",
    {
        "code": fields.String(
            required=True,
            description="Artist updated",
            example="Artist, albums and songs updated",
        ),
        "data": fields.Nested(artist_response_model),
    },
)

artist_delete_response_model = api.model(
    "Artist Delete Response",
    {
        "code": fields.String(
            required=True,
            description="Artist updated",
            example="Artist, albums and songs deleted",
        ),
        "data": fields.Nested(artist_response_model),
    },
)
# ----------------------------------------------------------------------
# Routes


@api.route("")
class Artists(Resource):
    @check_token
    @api.response(200, "Success", artist_response_model)
    def get(self):
        response, status_code = MediaRequester.get(f"artists")
        return response, status_code

    @check_token
    @api.expect(artist_post_model)
    @api.response(200, "Success", artist_response_model)
    def post(self):
        response, status_code = MediaRequester.post("artists", data=request.json)
        return response, status_code


@api.route("/id/<id>", doc={"params": {"id": "Artist id"}})
class ArtistById(Resource):
    @check_token
    @api.response(200, "Success", artist_response_model)
    def get(self, id):
        response, status_code = MediaRequester.get(f"artists/{id}")
        return response, status_code

    @check_token
    @api.expect(artist_put_model)
    @api.response(200, "Success", artist_put_response_model)
    def put(self, id):
        artist, status_code = MediaRequester.get(f"artists/{id}")
        albums, status_code = MediaRequester.get(f"albums/artistId/{id}")
        songs, status_code = MediaRequester.get(f"songs/artistId/{id}")
        edit_artist(request, albums, songs, artist)

        artist_modification_response, status_code = MediaRequester.put(
            f"artists/{id}", data=request.json
        )

        return (
            {
                "code": "DATA_UPDATED",
                "data": artist_modification_response,
            },
            200,
        )

    @check_token
    @api.response(200, "Success", artist_delete_response_model)
    def delete(self, id):
        albums, status_code = MediaRequester.get(f"albums/artistId/{id}")
        songs, status_code = MediaRequester.get(f"songs/artistId/{id}")
        delete_artist(albums, songs)

        artist_delete_response, status_code = MediaRequester.delete(f"artists/{id}")

        return (
            {
                "message": "Artist, albums and songs deleted",
                "data": artist_delete_response,
            },
            200,
        )


@api.route("/name/<name>", doc={"params": {"name": "Artist name"}})
class ArtistByName(Resource):
    @check_token
    @api.response(200, "Success", artist_response_model)
    def get(self, name):
        response, status_code = MediaRequester.get(f"artists/name/{name}")
        return response, status_code
