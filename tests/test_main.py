def test_root(client):
    """Test the root endpoint."""

    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "Product API is running"