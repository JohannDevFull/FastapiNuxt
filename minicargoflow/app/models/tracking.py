"""Modelo ORM para la tabla de eventos de trazabilidad.

Cada vez que un envío cambia de estado, se crea un registro en esta tabla.
Esto permite consultar el historial completo de un envío.
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class TrackingEvent(Base):
    """Modelo de base de datos para eventos de trazabilidad."""

    __tablename__ = "tracking_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # ForeignKey crea la relación con la tabla shipments a nivel de base de datos.
    shipment_id: Mapped[int] = mapped_column(
        ForeignKey("shipments.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Guardamos los estados como texto para conservar el historial aunque
    # la lógica de negocio evolucione en el futuro.
    previous_status: Mapped[str] = mapped_column(String(30), nullable=False)
    new_status: Mapped[str] = mapped_column(String(30), nullable=False)

    # Optional[str] indica que el valor puede ser texto o None.
    observation: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )

    # Relación inversa hacia Shipment. back_populates conecta ambos lados
    # de la relación para que SQLAlchemy los mantenga sincronizados.
    shipment: Mapped["Shipment"] = relationship("Shipment", back_populates="tracking_events")
