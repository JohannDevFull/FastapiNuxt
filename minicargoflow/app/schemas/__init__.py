"""Paquete de esquemas Pydantic.

Los esquemas Pydantic validan datos de entrada/salida de la API.
Son diferentes de los modelos ORM: el modelo representa la tabla en BD,
el esquema representa la forma de los datos que entran o salen por HTTP.
"""

from app.schemas.shipment import (
    ShipmentCreate,
    ShipmentResponse,
    ShipmentStatusUpdate,
    ShipmentUpdate,
)
from app.schemas.tracking import TrackingEventResponse

__all__ = [
    "ShipmentCreate",
    "ShipmentResponse",
    "ShipmentStatusUpdate",
    "ShipmentUpdate",
    "TrackingEventResponse",
]
