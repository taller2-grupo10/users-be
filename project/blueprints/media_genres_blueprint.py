from flask_restx import Namespace, Resource, fields
from project.helpers.helper_auth import check_token
from project.helpers.helper_media import MediaRequester

api = Namespace(
    name="Music Genres",
    path="/media/genres",
    description="Music Genres related endpoints",
)

music_genres_response_model = fields.List(
    fields.String(
        required=False,
        description="Music Genres",
    ),
    example=[
        "Alternative",
        "Blues",
        "Classical",
        "Country",
        "Dance",
        "Electronic",
        "Folk",
        "Funk",
        "Hip-Hop",
        "Heavy Metal",
        "Instrumental",
        "Jazz",
        "Pop",
        "R&B",
        "Reggae",
        "Rock",
        "Soul",
        "Trap",
        "Other",
    ],
)


# ----------------------------------------------------------------------
# Routes


@api.route("")
class MusicGenres(Resource):
    @api.response(200, "Success", music_genres_response_model)
    def get(self):
        response, status_code = MediaRequester.get(f"genres")
        return response, status_code
