from project.helpers.helper_date import date_to_str, today


def test_get_all_users(test_client, init_database, _db, user):
    response = test_client.get("/admin/users")
    assert response.status_code == 200
    assert response.json == [
        {
            "id": 1,
            "uid": "test_user",
            "artist_id": "1",
            "roles": [],
            "permissions": [],
            "active": True,
            "is_deleted": False,
            "created_at": date_to_str(today()),
            "updated_at": None,
            "email": None,
            "notification_token": "123",
        }
    ]
