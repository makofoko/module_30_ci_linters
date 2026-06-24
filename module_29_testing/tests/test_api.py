import pytest

@pytest.mark.parametrize("endpoint", ["/clients", "/parkings"])
def test_get_endpoints(client, endpoint):
    response = client.get(endpoint)
    assert response.status_code == 200

def test_create_client(client):
    response = client.post("/clients", json={
        "name": "Test",
        "surname": "User",
        "credit_card": "1234",
        "car_number": "A123BC"
    })
    assert response.status_code == 201

def test_create_parking(client):
    response = client.post("/parkings", json={
        "address": "Main Street 1",
        "opened": True,
        "count_places": 50,
        "count_available_places": 50
    })
    assert response.status_code == 201

@pytest.mark.parking
def test_enter_parking(client):
    client.post("/clients", json={"name": "Driver", "surname": "Test", "credit_card": "5678", "car_number": "B456CD"})
    client.post("/parkings", json={"address": "Central Parking", "opened": True, "count_places": 10, "count_available_places": 10})
    response = client.post("/client_parkings", json={"client_id": 1, "parking_id": 1})
    assert response.status_code == 201

@pytest.mark.parking
def test_exit_parking(client):
    client.post("/clients", json={"name": "Driver", "surname": "Test", "credit_card": "5678", "car_number": "B456CD"})
    client.post("/parkings", json={"address": "Central Parking", "opened": True, "count_places": 10, "count_available_places": 10})
    client.post("/client_parkings", json={"client_id": 1, "parking_id": 1})
    response = client.delete("/client_parkings", json={"client_id": 1, "parking_id": 1})
    assert response.status_code == 200
