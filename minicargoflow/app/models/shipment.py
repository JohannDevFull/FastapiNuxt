"""Modelo ORM para la tabla de envíos.

Conceptos clave:
- Clase: plantilla que define atributos y comportamientos. Aquí define
  la estructura de la tabla "shipments".
- Instancia: objeto creado a partir de una clase; cada instancia
  representa una fila en la tabla.
- mapped_column: define una columna de la tabla con su tipo y opciones.
- relationship: define la relación entre modelos (un envío tiene muchos
  eventos de trazabilidad).
"""

from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, Float, Integer, String, Text, func
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ShipmentStatus(str, Enum):
    """Estados posibles de un envío.

    Heredar de str y Enum permite usar el enum como texto en JSON
    y compararlo fácilmente con cadenas.
    """

    PENDING = "PENDING"
    PICKED_UP = "PICKED_UP"
    IN_TRANSIT = "IN_TRANSIT"
    OUT_FOR_DELIVERY = "OUT_FOR_DELIVERY"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"


# Diccionario con las transiciones permitidas.
# La clave es el estado actual y el valor es una lista de estados destino válidos.
# Esto evita cambios incoherentes, por ejemplo pasar de DELIVERED a PENDING.
ALLOWED_STATUS_TRANSITIONS: dict[ShipmentStatus, list[ShipmentStatus]] = {
    ShipmentStatus.PENDING: [ShipmentStatus.PICKED_UP, ShipmentStatus.CANCELLED],
    ShipmentStatus.PICKED_UP: [ShipmentStatus.IN_TRANSIT, ShipmentStatus.CANCELLED],
    ShipmentStatus.IN_TRANSIT: [ShipmentStatus.OUT_FOR_DELIVERY, ShipmentStatus.CANCELLED],
    ShipmentStatus.OUT_FOR_DELIVERY: [ShipmentStatus.DELIVERED, ShipmentStatus.CANCELLED],
    ShipmentStatus.DELIVERED: [],
    ShipmentStatus.CANCELLED: [],
}


class Shipment(Base):
    """Modelo de base de datos para envíos."""

    __tablename__ = "shipments"

    # primary_key=True identifica de forma única cada fila.
    # index=True acelera las búsquedas por esta columna.
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    tracking_number: Mapped[str] = mapped_column(String(30), unique=True, index=True, nullable=False)

    sender_name: Mapped[str] = mapped_column(String(100), nullable=False)
    sender_phone: Mapped[str] = mapped_column(String(20), nullable=False)
    recipient_name: Mapped[str] = mapped_column(String(100), nullable=False)
    recipient_phone: Mapped[str] = mapped_column(String(20), nullable=False)
    origin_address: Mapped[str] = mapped_column(String(255), nullable=False)
    destination_address: Mapped[str] = mapped_column(String(255), nullable=False)
    package_description: Mapped[str] = mapped_column(Text, nullable=False)
    weight_kg: Mapped[float] = mapped_column(Float, nullable=False)

    # SqlEnum guarda el valor del enum en la base de datos.
    status: Mapped[ShipmentStatus] = mapped_column(
        SqlEnum(ShipmentStatus, name="shipment_status"),
        nullable=False,
        default=ShipmentStatus.PENDING,
    )

    # server_default=func.now() hace que MySQL asigne la fecha al insertar.
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )

    # Relación uno-a-muchos: un envío tiene varios eventos de trazabilidad.
    # cascade="all, delete-orphan" elimina eventos si se elimina el envío.
    # order_by ordena el historial por fecha ascendente.
    tracking_events: Mapped[list["TrackingEvent"]] = relationship(
        "TrackingEvent",
        back_populates="shipment",
        cascade="all, delete-orphan",
        order_by="TrackingEvent.created_at.asc()",
    )
