"""Pruebas automatizadas para trazabilidad."""


def shipment_payload() -> dict:
    return {
        "sender_name": "Juan Perez",
        "sender_phone": "3001234567",
        "recipient_name": "Maria Gomez",
        "recipient_phone": "3107654321",
        "origin_address": "Calle 10 # 20-30, Medellin",
        "destination_address": "Carrera 50 # 40-20, Bogota",
        "package_description": "Caja con documentos",
        "weight_kg": 2.5,
    }


def create_shipment(client) -> dict:
    response = client.post("/api/v1/shipments", json=shipment_payload())
    assert response.status_code == 201
    return response.json()


def test_tracking_history_created_on_shipment_creation(client):
    """Al crear un envío debe existir un evento inicial de trazabilidad."""
    created = create_shipment(client)

    response = client.get(f"/api/v1/shipments/{created['id']}/tracking")

    assert response.status_code == 200
    events = response.json()
    assert len(events) == 1
    assert events[0]["previous_status"] == "PENDING"
    assert events[0]["new_status"] == "PENDING"


def test_tracking_history_records_status_change(client):
    """Un cambio de estado debe agregar un evento al historial."""
    created = create_shipment(client)
    client.patch(
        f"/api/v1/shipments/{created['id']}/status",
        json={"new_status": "PICKED_UP", "observation": "Recogido"},
    )

    response = client.get(f"/api/v1/shipments/{created['id']}/tracking")

    assert response.status_code == 200
    events = response.json()
    assert len(events) == 2
    assert events[1]["previous_status"] == "PENDING"
    assert events[1]["new_status"] == "PICKED_UP"
    assert events[1]["observation"] == "Recogido"


def test_tracking_by_tracking_number(client):
    """Debe consultar trazabilidad usando el número de guía."""
    created = create_shipment(client)

    response = client.get(f"/api/v1/tracking/{created['tracking_number']}")

    assert response.status_code == 200
    events = response.json()
    assert len(events) >= 1
    assert events[0]["shipment_id"] == created["id"]


def test_tracking_nonexistent_shipment_returns_404(client):
    """Debe responder 404 al consultar trazabilidad de un envío inexistente."""
    response = client.get("/api/v1/shipments/999999/tracking")
    assert response.status_code == 404

    response_by_guide = client.get("/api/v1/tracking/MCF-20990101-000000")
    assert response_by_guide.status_code == 404
