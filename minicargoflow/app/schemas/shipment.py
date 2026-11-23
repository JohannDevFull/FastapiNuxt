"""Esquemas Pydantic para envíos.

Conceptos clave:
- Pydantic: biblioteca que valida datos usando anotaciones de tipos.
- BaseModel: clase base de Pydantic; al heredar de ella definimos
  la estructura y reglas de validación de los datos.
- Esquema de entrada vs salida: los de entrada validan lo que el cliente
  envía; los de salida definen lo que la API responde.
- model_config/from_attributes: permite crear un esquema a partir de
  un objeto ORM de SQLAlchemy.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.models.shipment import ShipmentStatus


class ShipmentCreate(BaseModel):
    """Datos necesarios para crear un envío."""

    # Field(...) permite agregar reglas de validación, como longitud mínima.
    sender_name: str = Field(..., min_length=2, max_length=100)
    sender_phone: str = Field(..., min_length=7, max_length=20)
    recipient_name: str = Field(..., min_length=2, max_length=100)
    recipient_phone: str = Field(..., min_length=7, max_length=20)
    origin_address: str = Field(..., min_length=5, max_length=255)
    destination_address: str = Field(..., min_length=5, max_length=255)
    package_description: str = Field(..., min_length=3, max_length=500)
    weight_kg: float = Field(..., gt=0, description="Peso del paquete en kilogramos")


class ShipmentUpdate(BaseModel):
    """Datos para actualizar la información de un envío.

    Todos los campos son opcionales para permitir actualizaciones parciales
    a través del endpoint PUT de esta V1 (se actualiza solo lo enviado).
    """

    sender_name: Optional[str] = Field(None, min_length=2, max_length=100)
    sender_phone: Optional[str] = Field(None, min_length=7, max_length=20)
    recipient_name: Optional[str] = Field(None, min_length=2, max_length=100)
    recipient_phone: Optional[str] = Field(None, min_length=7, max_length=20)
    origin_address: Optional[str] = Field(None, min_length=5, max_length=255)
    destination_address: Optional[str] = Field(None, min_length=5, max_length=255)
    package_description: Optional[str] = Field(None, min_length=3, max_length=500)
    weight_kg: Optional[float] = Field(None, gt=0)


class ShipmentStatusUpdate(BaseModel):
    """Datos para cambiar el estado de un envío."""

    new_status: ShipmentStatus
    observation: Optional[str] = Field(None, max_length=255)


class ShipmentResponse(BaseModel):
    """Datos que la API devuelve al consultar un envío."""

    # from_attributes=True permite construir este esquema desde un objeto
    # SQLAlchemy, leyendo sus atributos (shipment.id, shipment.status, etc.).
    model_config = ConfigDict(from_attributes=True)

    id: int
    tracking_number: str
    sender_name: str
    sender_phone: str
    recipient_name: str
    recipient_phone: str
    origin_address: str
    destination_address: str
    package_description: str
    weight_kg: float
    status: ShipmentStatus
    created_at: datetime
    updated_at: datetime


class ShipmentListResponse(BaseModel):
    """Respuesta paginada para el listado de envíos."""

    items: list[ShipmentResponse]
    total: int
    page: int
    page_size: int
