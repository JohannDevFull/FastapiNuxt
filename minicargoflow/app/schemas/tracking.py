"""Esquemas Pydantic para trazabilidad."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class TrackingEventResponse(BaseModel):
    """Datos que la API devuelve para un evento de trazabilidad."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    shipment_id: int
    previous_status: str
    new_status: str
    observation: Optional[str]
    created_at: datetime
