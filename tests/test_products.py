def test_create_product(client, test_product):
    """Test creating a product."""

    response = client.post(
        "/products",
        json=test_product,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == test_product["name"]
    assert data["description"] == test_product["description"]
    assert data["price"] == test_product["price"]
    assert data["stock"] == test_product["stock"]


def test_list_products(client, test_product):
    """Test listing products."""

    client.post(
        "/products",
        json=test_product,
    )

    response = client.get("/products")

    assert response.status_code == 200

    data = response.json()

    assert len(data) >= 1
    assert data[0]["name"] == test_product["name"]


def test_get_product(client, test_product):
    """Test getting a single product."""

    create_response = client.post(
        "/products",
        json=test_product,
    )

    product_id = create_response.json()["id"]

    response = client.get(
        f"/products/{product_id}"
    )

    assert response.status_code == 200
    assert response.json()["name"] == test_product["name"]


def test_get_product_not_found(client):
    """Test getting a product that does not exist."""

    response = client.get("/products/99999")

    assert response.status_code == 404


def test_update_product(client, test_product):
    """Test updating a product."""

    create_response = client.post(
        "/products",
        json=test_product,
    )

    product_id = create_response.json()["id"]

    update_data = {
        "name": "Updated Product",
        "description": "Updated description",
        "price": 149.99,
        "stock": 20,
    }

    response = client.patch(
        f"/products/{product_id}",
        json=update_data,
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Updated Product"
    assert response.json()["price"] == 149.99


def test_delete_product(client, test_product):
    """Test deleting a product."""

    create_response = client.post(
        "/products",
        json=test_product,
    )

    product_id = create_response.json()["id"]

    response = client.delete(
        f"/products/{product_id}"
    )

    assert response.status_code == 204

    response = client.get(
        f"/products/{product_id}"
    )

    assert response.status_code == 404# Lab 10: Product CRUD tests
