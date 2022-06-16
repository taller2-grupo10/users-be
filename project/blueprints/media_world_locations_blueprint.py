from flask_restx import Namespace, Resource, fields
from project.helpers.helper_auth import check_token
from project.helpers.helper_media import MediaRequester

api = Namespace(
    name="World Locations",
    path="/media/locations",
    description="World Locations related endpoints",
)

world_locations_response_model = fields.List(
    fields.String(
        required=False,
        description="World Locations",
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
class WorldLocations(Resource):
    # @check_token
    @api.response(200, "Success", world_locations_response_model)
    def get(self):
        response, status_code = MediaRequester.get(f"locations")
        return response, status_code
