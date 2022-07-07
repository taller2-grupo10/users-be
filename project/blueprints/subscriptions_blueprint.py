from flask_restx import Namespace, Resource, fields
from project.helpers.helper_auth import check_token
from project.models.subscription import Subscription

api = Namespace(
    name="Subscriptions",
    path="/media/subscriptions",
    description="Subscriptions related endpoints",
)

subscription_model = api.model(
    "Subscription",
    {
        "id": fields.Integer(required=True, description="Subscription identifier"),
        "name": fields.String(required=True, description="Subscription name"),
        "price_in_ethers": fields.Float(
            required=True, description="Subscription price"
        ),
    },
)


def subscription_schema(subscription):
    return {
        "id": subscription.id,
        "name": subscription.name,
        "price_in_ethers": subscription.price_in_ethers,
    }


# ----------------------------------------------------------------------
# Routes


@api.route("")
class Subscriptions(Resource):
    @check_token
    @api.response(200, "Success", subscription_model)
    def get(self):
        subscriptions = Subscription.query.all()
        return [subscription_schema(subscription) for subscription in subscriptions]
