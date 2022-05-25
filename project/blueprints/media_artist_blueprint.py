from pydoc import doc
from urllib import response
from flask import Blueprint, request
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
        "message": fields.String(
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
        "message": fields.String(
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
    # @check_token
    @api.response(200, "Success", artist_response_model)
    def get(self):
        response, status_code = MediaRequester.get(f"artists")
        return response, status_code

    # @check_token
    @api.expect(artist_post_model)
    @api.response(200, "Success", artist_response_model)
    def post(self):
        response, status_code = MediaRequester.post("artists", data=request.json)
        return response, status_code


@api.route("/id/<id>", doc={"params": {"id": "Artist id"}})
class ArtistById(Resource):
    # @check_token
    @api.response(200, "Success", artist_response_model)
    def get(self, id):
        response, status_code = MediaRequester.get(f"artists/{id}")
        return response, status_code

    # @check_token
    @api.expect(artist_put_model)
    @api.response(200, "Success", artist_put_response_model)
    def put(self, id):
        artist, status_code = MediaRequester.get(f"artists/{id}")
        albums, status_code = MediaRequester.get(f"albums/artistId/{id}")
        songs, status_code = MediaRequester.get(f"songs/artistId/{id}")

        for album in albums:
            album_id = album["_id"]
            album_request = {"artist.name": request.json["name"]}
            _put_album(album_id, album_request)

        for song in songs:
            song_id = song["_id"]
            artist_name = artist[0]["name"]
            # Modify song artist name if it's the main artist
            if artist_name == song["artist"]["name"]:
                song_request = {"artist.name": request.json["name"]}
                _put_song(song_id, song_request)
            # Modify song collaborator name if it's a featured artist
            elif artist_name in song["artist"]["collaboratorsNames"]:
                song_collaborators_names = song["artist"]["collaboratorsNames"]
                song_collaborators_names = list(
                    filter(lambda x: x != artist_name, song_collaborators_names)
                )
                song_collaborators_names.append(request.json["name"])
                song_request = {"artist.collaboratorsNames": song_collaborators_names}
                _put_song(song_id, song_request)

        artist_modification_response, status_code = MediaRequester.put(
            f"artists/{id}", data=request.json
        )

        return (
            jsonify(
                {
                    "message": "Artist, albums and songs updated",
                    "data": artist_modification_response,
                }
            ),
            200,
        )

    # @check_token
    @api.response(200, "Success", artist_delete_response_model)
    def delete(self, id):
        albums, status_code = MediaRequester.get(f"albums/artistId/{id}")
        songs, status_code = MediaRequester.get(f"songs/artistId/{id}")

        for album in albums:
            album_id = album["_id"]
            _delete_album(album_id)

        for song in songs:
            song_id = song["_id"]
            _delete_song(song_id)

        artist_delete_response, status_code = MediaRequester.delete(f"artists/{id}")

        return (
            jsonify(
                {
                    "message": "Artist, albums and songs deleted",
                    "data": artist_delete_response,
                }
            ),
            200,
        )


@api.route("/name/<name>", doc={"params": {"name": "Artist name"}})
class ArtistByName(Resource):
    # @check_token
    @api.response(200, "Success", artist_response_model)
    def get(self, name):
        response, status_code = MediaRequester.get(f"artists/name/{name}")
        return response, status_code


def _delete_album(album_id):
    return MediaRequester.delete(f"albums/{album_id}")


def _delete_song(song_id):
    return MediaRequester.delete(f"songs/{song_id}")


def _put_album(album_id, request):
    return MediaRequester.put(f"albums/{album_id}", data=request)


def _put_song(song_id, request):
    return MediaRequester.put(f"songs/{song_id}", data=request)
