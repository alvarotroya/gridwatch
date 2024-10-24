from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from gridwatch.crud import devices as crud_devices
from gridwatch.database import get_db
from gridwatch.schemas.devices import (
    DeviceCreateSchema,
    DeviceSchema,
    DeviceUpdateSchema,
)

router = APIRouter()

DatabaseDep = Annotated[Session, Depends(get_db)]


@router.get("/devices", response_model=list[DeviceSchema])
def get_devices(db: DatabaseDep) -> list[DeviceSchema]:
    return crud_devices.get_devices(db)


@router.get("/devices/{device_id}", response_model=DeviceSchema)
def get_device(device_id: UUID, db: DatabaseDep) -> DeviceSchema:
    return crud_devices.get_device(db, device_id)


@router.post("/devices", response_model=DeviceSchema)
def post_device(device_create: DeviceCreateSchema, db: DatabaseDep) -> DeviceSchema:
    return crud_devices.create_device(db, device_create)


@router.patch("/devices/{device_id}", response_model=DeviceSchema)
def patch_device(
    device_id: UUID, device_update: DeviceUpdateSchema, db: DatabaseDep
) -> DeviceSchema:
    # NOTE: updates to config/specs will overwrite the whole config/specs.
    # TODO: fix this
    return crud_devices.update_device(db, device_id, device_update)


@router.delete("/devices/{device_id}", response_model=DeviceSchema)
def delete_device(device_id: UUID, db: DatabaseDep) -> DeviceSchema:
    return crud_devices.delete_device(db, device_id)
