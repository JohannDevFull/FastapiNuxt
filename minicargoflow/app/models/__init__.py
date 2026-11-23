"""Paquete de modelos ORM.

Los modelos representan tablas de la base de datos usando SQLAlchemy.
Se importan aquí para facilitar su acceso desde otros módulos.
"""

from app.models.shipment import Shipment
from app.models.tracking import TrackingEvent

__all__ = ["Shipment", "TrackingEvent"]
