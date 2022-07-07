from project.models.user_payment import UserPayment


def test_create_user_payment(init_database, _db, user, subscription):
    user_payment = UserPayment(
        user_id=user.id, transaction_hash="hash", subscription_id=subscription.id
    )
    _db.session.add(user_payment)
    _db.session.commit()
    assert user_payment.id == 1
    assert user_payment.user_id == user.id
    assert user_payment.subscription_id == subscription.id
    assert user_payment.transaction_hash == "hash"
    assert user_payment.__repr__() == "<UserPayment 1 1 hash>"


"""
project/models/user_payment.py                     13      4    69%   13, 16-18
project/models/password_reset_request.py           10      3    70%   14, 17-18
project/models/base_model.py                       25      4    84%   26, 32, 36, 56
project/models/subscription.py                      9      1    89%   13
project/models/user_role.py                        13      1    92%   15
project/models/role.py                             17      1    94%   20
project/models/user.py                             31      1    97%   33
"""
