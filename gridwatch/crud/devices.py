from uuid import UUID

from sqlalchemy.orm import Session

from gridwatch.crud.exceptions import DatabaseEntityNotFound
from gridwatch.models.devices import DeviceModel
from gridwatch.schemas.devices import (
    DeviceCreateSchema,
    DeviceSchema,
    DeviceUpdateSchema,
)


def get_devices(db: Session) -> list[DeviceSchema]:
    return [
        DeviceSchema.model_validate(device) for device in db.query(DeviceModel).all()
    ]


def get_device(db: Session, device_id: UUID) -> DeviceSchema:
    device = db.query(DeviceModel).filter(DeviceModel.id == device_id).first()

    if device is None:
        raise DatabaseEntityNotFound(f"Could not find Device with id {device_id}")

    return DeviceSchema.model_validate(device)


def create_device(db: Session, device_create: DeviceCreateSchema) -> DeviceSchema:
    device = DeviceModel(**device_create.model_dump())
    db.add(device)
    db.commit()

    db.refresh(device)

    return DeviceSchema.model_validate(device)


def update_device(
    db: Session, device_id: UUID, device_update: DeviceUpdateSchema
) -> DeviceSchema:
    device = db.query(DeviceModel).filter(DeviceModel.id == device_id).first()

    if device is None:
        raise DatabaseEntityNotFound(f"Could not find Device with id {device_id}")

    # Update only the fields that are provided in the request
    for key, value in device_update.model_dump(exclude_unset=True).items():
        setattr(device, key, value)

    db.commit()
    db.refresh(device)

    return DeviceSchema.model_validate(device)


def delete_device(db: Session, device_id: UUID) -> DeviceSchema:
    device = db.query(DeviceModel).filter(DeviceModel.id == device_id).first()

    if device is None:
        raise DatabaseEntityNotFound(f"Could not find Device with id {device_id}")

    db.delete(device)
    db.commit()

    return DeviceSchema.model_validate(device)
