"""Router de trazabilidad.

Expone el endpoint para consultar el historial por número de guía.
El historial por ID de envío se definió en el router de envíos para
mantener la ruta /api/v1/shipments/{shipment_id}/tracking.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.tracking import TrackingEventResponse
from app.services import tracking_service

router = APIRouter(prefix="/api/v1/tracking", tags=["Tracking"])


@router.get("/{tracking_number}", response_model=list[TrackingEventResponse])
def get_tracking_by_tracking_number(
    tracking_number: str, db: Session = Depends(get_db)
) -> list[TrackingEventResponse]:
    """Consulta el historial de trazabilidad usando el número de guía."""
    return tracking_service.get_tracking_events_by_tracking_number(db, tracking_number)
