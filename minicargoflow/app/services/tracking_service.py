"""Servicio de trazabilidad.

Consulta el historial de eventos asociados a un envío.
"""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.tracking import TrackingEvent
from app.services.shipment_service import get_shipment_by_id, get_shipment_by_tracking_number


def get_tracking_events_by_shipment_id(db: Session, shipment_id: int) -> list[TrackingEvent]:
    """Retorna el historial de trazabilidad de un envío por su ID."""
    shipment = get_shipment_by_id(db, shipment_id)
    if shipment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Envío no encontrado.")

    events = (
        db.query(TrackingEvent)
        .filter(TrackingEvent.shipment_id == shipment_id)
        .order_by(TrackingEvent.created_at.asc())
        .all()
    )
    return events


def get_tracking_events_by_tracking_number(db: Session, tracking_number: str) -> list[TrackingEvent]:
    """Retorna el historial de trazabilidad buscando por número de guía."""
    shipment = get_shipment_by_tracking_number(db, tracking_number)
    if shipment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Envío no encontrado.")

    events = (
        db.query(TrackingEvent)
        .filter(TrackingEvent.shipment_id == shipment.id)
        .order_by(TrackingEvent.created_at.asc())
        .all()
    )
    return events
