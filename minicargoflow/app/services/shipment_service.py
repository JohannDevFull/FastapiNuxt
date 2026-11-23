"""Servicio de envíos.

Contiene la lógica de negocio relacionada con envíos: crear, consultar,
actualizar, cancelar y cambiar estados.

La sesión de SQLAlchemy (db: Session) se recibe como parámetro desde
el router, que a su vez la obtiene mediante Depends(get_db).
"""

from datetime import datetime
import random

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.shipment import ALLOWED_STATUS_TRANSITIONS, Shipment, ShipmentStatus
from app.models.tracking import TrackingEvent
from app.schemas.shipment import ShipmentCreate, ShipmentStatusUpdate, ShipmentUpdate


def generate_tracking_number() -> str:
    """Genera un número de guía único con formato MCF-YYYYMMDD-XXXXXX.

    Usamos la fecha actual y un número aleatorio de 6 dígitos.
    La unicidad final se valida contra la base de datos antes de guardar.
    """
    date_part = datetime.now().strftime("%Y%m%d")
    random_part = random.randint(100000, 999999)
    return f"MCF-{date_part}-{random_part}"


def generate_unique_tracking_number(db: Session) -> str:
    """Genera un número de guía y verifica que no exista en la base de datos.

    Se intenta varias veces para reducir la probabilidad de colisión.
    Si no se logra, se lanza una excepción HTTP 409.
    """
    for _ in range(10):
        tracking_number = generate_tracking_number()
        existing_shipment = get_shipment_by_tracking_number(db, tracking_number)
        if existing_shipment is None:
            return tracking_number

    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="No se pudo generar un número de guía único. Intente nuevamente.",
    )


def create_shipment(db: Session, shipment_data: ShipmentCreate) -> Shipment:
    """Crea un nuevo envío en estado PENDING y registra su trazabilidad inicial."""
    tracking_number = generate_unique_tracking_number(db)

    # Creamos una instancia del modelo ORM. Esto todavía no guarda en BD;
    # es un objeto Python que representa la fila que queremos insertar.
    new_shipment = Shipment(
        tracking_number=tracking_number,
        sender_name=shipment_data.sender_name,
        sender_phone=shipment_data.sender_phone,
        recipient_name=shipment_data.recipient_name,
        recipient_phone=shipment_data.recipient_phone,
        origin_address=shipment_data.origin_address,
        destination_address=shipment_data.destination_address,
        package_description=shipment_data.package_description,
        weight_kg=shipment_data.weight_kg,
        status=ShipmentStatus.PENDING,
    )

    # add() coloca el objeto en la sesión; commit() confirma la transacción;
    # refresh() recarga datos generados por la BD (id, fechas).
    db.add(new_shipment)
    db.commit()
    db.refresh(new_shipment)

    # Registramos el evento inicial de trazabilidad.
    initial_event = TrackingEvent(
        shipment_id=new_shipment.id,
        previous_status=ShipmentStatus.PENDING.value,
        new_status=ShipmentStatus.PENDING.value,
        observation="Envío registrado en el sistema.",
    )
    db.add(initial_event)
    db.commit()
    db.refresh(new_shipment)

    return new_shipment


def get_shipments(db: Session, page: int = 1, page_size: int = 10) -> tuple[list[Shipment], int]:
    """Obtiene envíos con paginación sencilla.

    Retorna una tupla: (lista de envíos, total de registros).
    offset indica cuántos registros saltar; limit cuántos traer.
    """
    if page < 1:
        page = 1
    if page_size < 1:
        page_size = 10
    if page_size > 100:
        page_size = 100

    query = db.query(Shipment).order_by(Shipment.created_at.desc())
    total = query.count()
    offset = (page - 1) * page_size
    shipments = query.offset(offset).limit(page_size).all()
    return shipments, total


def get_shipment_by_id(db: Session, shipment_id: int) -> Shipment | None:
    """Busca un envío por su ID. Retorna None si no existe."""
    return db.query(Shipment).filter(Shipment.id == shipment_id).first()


def get_shipment_by_tracking_number(db: Session, tracking_number: str) -> Shipment | None:
    """Busca un envío por su número de guía."""
    return db.query(Shipment).filter(Shipment.tracking_number == tracking_number).first()


def update_shipment(db: Session, shipment_id: int, shipment_data: ShipmentUpdate) -> Shipment:
    """Actualiza la información de un envío existente.

    No permite actualizar envíos cancelados o entregados para mantener
    coherencia con el negocio.
    """
    shipment = get_shipment_by_id(db, shipment_id)
    if shipment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Envío no encontrado.")

    if shipment.status in [ShipmentStatus.CANCELLED, ShipmentStatus.DELIVERED]:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se puede actualizar un envío entregado o cancelado.",
        )

    # model_dump(exclude_unset=True) obtiene solo los campos que el cliente envió.
    # Esto evita sobrescribir campos con None cuando no se incluyeron en la petición.
    update_data = shipment_data.model_dump(exclude_unset=True)

    # setattr(objeto, "campo", valor) asigna dinámicamente un atributo.
    # Es útil aquí porque recorremos los campos enviados en el request.
    for field_name, value in update_data.items():
        setattr(shipment, field_name, value)

    db.commit()
    db.refresh(shipment)
    return shipment


def validate_status_transition(current_status: ShipmentStatus, new_status: ShipmentStatus) -> None:
    """Valida que la transición de estado sea permitida por las reglas de negocio."""
    allowed_transitions = ALLOWED_STATUS_TRANSITIONS.get(current_status, [])
    if new_status not in allowed_transitions:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                f"Transición de estado no permitida: {current_status.value} -> {new_status.value}."
            ),
        )


def change_shipment_status(
    db: Session, shipment_id: int, status_data: ShipmentStatusUpdate
) -> Shipment:
    """Cambia el estado de un envío y registra el evento de trazabilidad."""
    shipment = get_shipment_by_id(db, shipment_id)
    if shipment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Envío no encontrado.")

    current_status = shipment.status
    new_status = status_data.new_status

    if current_status == new_status:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El envío ya se encuentra en el estado solicitado.",
        )

    validate_status_transition(current_status, new_status)

    shipment.status = new_status

    tracking_event = TrackingEvent(
        shipment_id=shipment.id,
        previous_status=current_status.value,
        new_status=new_status.value,
        observation=status_data.observation,
    )

    db.add(tracking_event)
    db.commit()
    db.refresh(shipment)
    return shipment


def cancel_shipment(db: Session, shipment_id: int) -> None:
    """Cancela un envío si la transición es válida.

    El endpoint DELETE usa esta función y responde 204 sin contenido.
    """
    shipment = get_shipment_by_id(db, shipment_id)
    if shipment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Envío no encontrado.")

    if shipment.status == ShipmentStatus.CANCELLED:
        return

    validate_status_transition(shipment.status, ShipmentStatus.CANCELLED)

    previous_status = shipment.status
    shipment.status = ShipmentStatus.CANCELLED

    tracking_event = TrackingEvent(
        shipment_id=shipment.id,
        previous_status=previous_status.value,
        new_status=ShipmentStatus.CANCELLED.value,
        observation="Envío cancelado por el usuario.",
    )
    db.add(tracking_event)
    db.commit()
