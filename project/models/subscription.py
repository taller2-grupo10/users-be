from os import name
from project import db
from project.models.base_model import BaseModel


class Subscription(BaseModel):
    __tablename__ = "subscription"

    name = db.Column(db.String(50), nullable=False)
    price_in_ethers = db.Column(db.Float)

    def __repr__(self):
        return f"<Subscription {self.name} {self.price_in_ethers}>"
