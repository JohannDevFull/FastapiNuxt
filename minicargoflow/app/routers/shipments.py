"""Router de envíos.

Conceptos clave:
- APIRouter: permite organizar endpoints en módulos separados.
- Decoradores (@router.get, @router.post, etc.): indican el método HTTP,
  la ruta y metadatos del endpoint.
- Depends(get_db): inyección de dependencias. FastAPI llama a get_db,
  obtiene la sesión y la pasa al parámetro db del endpoint.
- response_model: define el esquema Pydantic usado para la respuesta;
  también ayuda a documentar la API en Swagger.
- status_code: código HTTP que devolverá el endpoint cuando sea exitoso.
"""

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.shipment import (
    ShipmentCreate,
    ShipmentListResponse,
    ShipmentResponse,
    ShipmentStatusUpdate,
    ShipmentUpdate,
)
from app.schemas.tracking import TrackingEventResponse
from app.services import shipment_service, tracking_service

# prefix agrupa todas las rutas bajo /api/v1/shipments.
# tags organiza los endpoints en la documentación Swagger.
router = APIRouter(prefix="/api/v1/shipments", tags=["Shipments"])


@router.post("", response_model=ShipmentResponse, status_code=status.HTTP_201_CREATED)
def create_shipment(shipment_data: ShipmentCreate, db: Session = Depends(get_db)) -> ShipmentResponse:
    """Registra un nuevo envío."""
    return shipment_service.create_shipment(db, shipment_data)


@router.get("", response_model=ShipmentListResponse)
def list_shipments(
    page: int = Query(1, ge=1, description="Número de página"),
    page_size: int = Query(10, ge=1, le=100, description="Cantidad de elementos por página"),
    db: Session = Depends(get_db),
) -> ShipmentListResponse:
    """Consulta envíos con paginación sencilla."""
    shipments, total = shipment_service.get_shipments(db, page=page, page_size=page_size)
    return ShipmentListResponse(items=shipments, total=total, page=page, page_size=page_size)


@router.get("/tracking/{tracking_number}", response_model=ShipmentResponse)
def get_shipment_by_tracking_number(tracking_number: str, db: Session = Depends(get_db)) -> ShipmentResponse:
    """Busca un envío por número de guía."""
    shipment = shipment_service.get_shipment_by_tracking_number(db, tracking_number)
    if shipment is None:
        from fastapi import HTTPException

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Envío no encontrado.")
    return shipment


@router.get("/{shipment_id}", response_model=ShipmentResponse)
def get_shipment_by_id(shipment_id: int, db: Session = Depends(get_db)) -> ShipmentResponse:
    """Consulta un envío por su identificador."""
    shipment = shipment_service.get_shipment_by_id(db, shipment_id)
    if shipment is None:
        from fastapi import HTTPException

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Envío no encontrado.")
    return shipment


@router.put("/{shipment_id}", response_model=ShipmentResponse)
def update_shipment(
    shipment_id: int,
    shipment_data: ShipmentUpdate,
    db: Session = Depends(get_db),
) -> ShipmentResponse:
    """Actualiza la información de un envío."""
    return shipment_service.update_shipment(db, shipment_id, shipment_data)


@router.patch("/{shipment_id}/status", response_model=ShipmentResponse)
def update_shipment_status(
    shipment_id: int,
    status_data: ShipmentStatusUpdate,
    db: Session = Depends(get_db),
) -> ShipmentResponse:
    """Actualiza el estado de un envío y registra la trazabilidad."""
    return shipment_service.change_shipment_status(db, shipment_id, status_data)


@router.delete("/{shipment_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancel_shipment(shipment_id: int, db: Session = Depends(get_db)) -> Response:
    """Cancela un envío. Responde 204 cuando la operación es exitosa."""
    shipment_service.cancel_shipment(db, shipment_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/{shipment_id}/tracking", response_model=list[TrackingEventResponse])
def get_shipment_tracking(shipment_id: int, db: Session = Depends(get_db)) -> list[TrackingEventResponse]:
    """Consulta el historial de trazabilidad de un envío por ID."""
    return tracking_service.get_tracking_events_by_shipment_id(db, shipment_id)
