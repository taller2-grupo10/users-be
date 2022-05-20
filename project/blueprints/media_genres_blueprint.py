from flask_restx import Namespace, Resource, fields
from project.helpers.helper_auth import check_token
from project.helpers.helper_media import MediaRequester

api = Namespace(
    name="Music Genres",
    path="/media/genres",
    description="Music Genres related endpoints",
)


# ----------------------------------------------------------------------
# Routes


@api.route("")
class MusicGenres(Resource):
    # @check_token
    @api.response(200, "Success", [])
    def get(self):
        response, status_code = MediaRequester.get(f"genres")
        return response, status_code
