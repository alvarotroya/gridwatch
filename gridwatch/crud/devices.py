from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from gridwatch.crud.exceptions import DatabaseEntityNotFound
from gridwatch.models.devices import DeviceModel
from gridwatch.schemas.devices import (
    DeviceCreateSchema,
    DeviceSchema,
    DeviceUpdateSchema,
)


async def get_devices(db: AsyncSession) -> list[DeviceSchema]:
    result = await db.execute(select(DeviceModel))
    devices = result.scalars().all()
    return [DeviceSchema.model_validate(device) for device in devices]


async def get_device(db: AsyncSession, device_id: UUID) -> DeviceSchema:
    result = await db.execute(select(DeviceModel).where(DeviceModel.id == device_id))
    device = result.scalar()

    if device is None:
        raise DatabaseEntityNotFound(f"Could not find Device with id {device_id}")

    return DeviceSchema.model_validate(device)


async def create_device(
    db: AsyncSession, device_create: DeviceCreateSchema
) -> DeviceSchema:
    device = DeviceModel(**device_create.model_dump())
    db.add(device)
    await db.commit()
    await db.refresh(device)
    return DeviceSchema.model_validate(device)


async def update_device(
    db: AsyncSession, device_id: UUID, device_update: DeviceUpdateSchema
) -> DeviceSchema:
    result = await db.execute(select(DeviceModel).where(DeviceModel.id == device_id))
    device = result.scalar()

    if device is None:
        raise DatabaseEntityNotFound(f"Could not find Device with id {device_id}")

    # Update only the fields that are provided in the request
    for key, value in device_update.model_dump(exclude_unset=True).items():
        setattr(device, key, value)

    await db.commit()
    await db.refresh(device)
    return DeviceSchema.model_validate(device)


async def delete_device(db: AsyncSession, device_id: UUID) -> DeviceSchema:
    result = await db.execute(select(DeviceModel).where(DeviceModel.id == device_id))
    device = result.scalar()

    if device is None:
        raise DatabaseEntityNotFound(f"Could not find Device with id {device_id}")

    await db.delete(device)
    await db.commit()
    return DeviceSchema.model_validate(device)
