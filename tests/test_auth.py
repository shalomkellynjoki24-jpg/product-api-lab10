def test_register_user(client):
    response = client.post(
        "/register",
        json={
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "password123",
            "full_name": "New User",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["username"] == "newuser"
    assert data["email"] == "newuser@example.com"
    assert data["full_name"] == "New User"

    # Password must not be returned
    assert "password" not in data
    assert "hashed_password" not in data


def test_duplicate_registration(client):
    user = {
        "username": "duplicateuser",
        "email": "duplicate@example.com",
        "password": "password123",
        "full_name": "Duplicate User",
    }

    first_response = client.post(
        "/register",
        json=user,
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/register",
        json=user,
    )

    assert second_response.status_code == 409


def test_login_success(client):
    client.post(
        "/register",
        json={
            "username": "loginuser",
            "email": "login@example.com",
            "password": "password123",
            "full_name": "Login User",
        },
    )

    response = client.post(
        "/login",
        data={
            "username": "loginuser",
            "password": "password123",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_password(client):
    client.post(
        "/register",
        json={
            "username": "wrongpassword",
            "email": "wrong@example.com",
            "password": "password123",
            "full_name": "Wrong Password",
        },
    )

    response = client.post(
        "/login",
        data={
            "username": "wrongpassword",
            "password": "wrongpassword",
        },
    )

    assert response.status_code == 401# Lab 10: Authentication tests
