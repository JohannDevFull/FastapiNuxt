"""Pruebas automatizadas para el módulo de envíos.

Cada prueba usa el cliente de FastAPI y una base de datos de pruebas limpia.
Las funciones que empiezan con test_ son detectadas automáticamente por Pytest.
"""


def shipment_payload() -> dict:
    """Datos base reutilizables para crear envíos en pruebas."""
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
    """Helper para crear un envío y retornar la respuesta JSON."""
    response = client.post("/api/v1/shipments", json=shipment_payload())
    assert response.status_code == 201
    return response.json()


def test_create_shipment(client):
    """Debe crear un envío con estado inicial PENDING y número de guía."""
    response = client.post("/api/v1/shipments", json=shipment_payload())

    assert response.status_code == 201
    data = response.json()
    assert data["id"] > 0
    assert data["tracking_number"].startswith("MCF-")
    assert data["status"] == "PENDING"
    assert data["sender_name"] == "Juan Perez"


def test_list_shipments(client):
    """Debe listar envíos con paginación."""
    create_shipment(client)
    create_shipment(client)

    response = client.get("/api/v1/shipments?page=1&page_size=10")

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert data["page"] == 1
    assert data["page_size"] == 10
    assert len(data["items"]) == 2


def test_get_shipment_by_id(client):
    """Debe consultar un envío por su ID."""
    created = create_shipment(client)

    response = client.get(f"/api/v1/shipments/{created['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_get_shipment_by_tracking_number(client):
    """Debe buscar un envío por número de guía."""
    created = create_shipment(client)

    response = client.get(f"/api/v1/shipments/tracking/{created['tracking_number']}")

    assert response.status_code == 200
    assert response.json()["tracking_number"] == created["tracking_number"]


def test_update_shipment(client):
    """Debe actualizar la información de un envío."""
    created = create_shipment(client)

    response = client.put(
        f"/api/v1/shipments/{created['id']}",
        json={"recipient_name": "Ana Ruiz", "weight_kg": 3.0},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["recipient_name"] == "Ana Ruiz"
    assert data["weight_kg"] == 3.0


def test_update_shipment_status_valid_transition(client):
    """Debe permitir un cambio de estado válido y registrar trazabilidad."""
    created = create_shipment(client)

    response = client.patch(
        f"/api/v1/shipments/{created['id']}/status",
        json={"new_status": "PICKED_UP", "observation": "Paquete recogido"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "PICKED_UP"


def test_update_shipment_status_invalid_transition(client):
    """Debe rechazar una transición de estado inválida."""
    created = create_shipment(client)

    response = client.patch(
        f"/api/v1/shipments/{created['id']}/status",
        json={"new_status": "DELIVERED", "observation": "Intento inválido"},
    )

    assert response.status_code == 409


def test_cancel_shipment(client):
    """Debe cancelar un envío y responder 204."""
    created = create_shipment(client)

    response = client.delete(f"/api/v1/shipments/{created['id']}")

    assert response.status_code == 204

    get_response = client.get(f"/api/v1/shipments/{created['id']}")
    assert get_response.status_code == 200
    assert get_response.json()["status"] == "CANCELLED"


def test_get_nonexistent_shipment_returns_404(client):
    """Debe responder 404 cuando el envío no existe."""
    response = client.get("/api/v1/shipments/999999")
    assert response.status_code == 404
