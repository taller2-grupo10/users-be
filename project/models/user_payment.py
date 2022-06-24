from project import db
from project.models.base_model import BaseModel


class UserPayment(BaseModel):
    __tablename__ = "user_payments"

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    subscription_id = db.Column(db.Integer, db.ForeignKey("subscription.id"))
    transaction_hash = db.Column(db.String(128))

    def __repr__(self):
        return f"<UserPayment {self.user_id} {self.subscription_id} {self.transaction_hash}>"

    def __init__(self, user_id, subscription_id, transaction_hash):
        self.user_id = user_id
        self.subscription_id = subscription_id
        self.transaction_hash = transaction_hash
