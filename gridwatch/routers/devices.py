from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from gridwatch.crud import devices as crud_devices
from gridwatch.database import get_db
from gridwatch.schemas.devices import (
    DeviceCreateSchema,
    DeviceSchema,
    DeviceUpdateSchema,
)

router = APIRouter()

DatabaseDep = Annotated[AsyncSession, Depends(get_db)]


@router.get("/devices", response_model=list[DeviceSchema])
async def get_devices(db: DatabaseDep) -> list[DeviceSchema]:
    return await crud_devices.get_devices(db)


@router.get("/devices/{device_id}", response_model=DeviceSchema)
async def get_device(device_id: UUID, db: DatabaseDep) -> DeviceSchema:
    return await crud_devices.get_device(db, device_id)


@router.post("/devices", response_model=DeviceSchema)
async def post_device(
    device_create: DeviceCreateSchema, db: DatabaseDep
) -> DeviceSchema:
    return await crud_devices.create_device(db, device_create)


@router.patch("/devices/{device_id}", response_model=DeviceSchema)
async def patch_device(
    device_id: UUID, device_update: DeviceUpdateSchema, db: DatabaseDep
) -> DeviceSchema:
    # NOTE: updates to config/specs will overwrite the whole config/specs.
    # TODO: fix this
    return await crud_devices.update_device(db, device_id, device_update)


@router.delete("/devices/{device_id}", response_model=DeviceSchema)
async def delete_device(device_id: UUID, db: DatabaseDep) -> DeviceSchema:
    return await crud_devices.delete_device(db, device_id)
