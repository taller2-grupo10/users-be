from flask_restx import Namespace, Resource, fields
from project.helpers.helper_auth import check_token
from project.helpers.helper_media import MediaRequester

api = Namespace(
    name="Locations",
    path="/media/locations",
    description="Location related endpoints",
)

locations_model = fields.List(
    fields.String(
        required=False,
        description="Location",
    ),
    example=[
        "North America",
        "South America",
        "Central America",
        "Europe",
        "Asia",
        "Africa",
        "Oceania",
        "Antarctica",
    ],
)


# ----------------------------------------------------------------------
# Routes


@api.route("")
class Locations(Resource):
    # @check_token
    @api.response(200, "Success", locations_model)
    def get(self):
        response, status_code = MediaRequester.get(f"locations")
        return response, status_code
