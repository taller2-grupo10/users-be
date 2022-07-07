from project.models.subscription import Subscription


def test_create_subscription(init_database, _db):
    subscription = Subscription(name="Test Sub", price_in_ethers=1.0)
    assert subscription.name == "Test Sub"
    assert subscription.price_in_ethers == 1.0
    assert subscription.__repr__() == "<Subscription Test Sub 1.0>"
