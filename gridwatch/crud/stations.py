from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from gridwatch.crud.exceptions import DatabaseEntityNotFound
from gridwatch.models.stations import StationModel
from gridwatch.schemas.stations import (
    StationCreateSchema,
    StationSchema,
    StationUpdateSchema,
)


async def get_stations(db: AsyncSession) -> list[StationSchema]:
    result = await db.execute(select(StationModel))
    stations = result.scalars().all()
    return [StationSchema.model_validate(station) for station in stations]


async def get_station(db: AsyncSession, station_id: UUID) -> StationSchema:
    result = await db.execute(select(StationModel).where(StationModel.id == station_id))
    station = result.scalar()

    if station is None:
        raise DatabaseEntityNotFound(f"Could not find Station with id {station_id}")

    return StationSchema.model_validate(station)


async def create_station(
    db: AsyncSession, station_create: StationCreateSchema
) -> StationSchema:
    station = StationModel(**station_create.model_dump())
    db.add(station)
    await db.commit()
    await db.refresh(station)
    return StationSchema.model_validate(station)


async def update_station(
    db: AsyncSession, station_id: UUID, station_update: StationUpdateSchema
) -> StationSchema:
    result = await db.execute(select(StationModel).where(StationModel.id == station_id))
    station = result.scalar()

    if station is None:
        raise DatabaseEntityNotFound(f"Could not find Station with id {station_id}")

    # Update only the fields that are provided in the request
    for key, value in station_update.model_dump(exclude_unset=True).items():
        setattr(station, key, value)

    await db.commit()
    await db.refresh(station)
    return StationSchema.model_validate(station)


async def delete_station(db: AsyncSession, station_id: UUID) -> StationSchema:
    result = await db.execute(select(StationModel).where(StationModel.id == station_id))
    station = result.scalar()

    if station is None:
        raise DatabaseEntityNotFound(f"Could not find Station with id {station_id}")

    await db.delete(station)
    await db.commit()
    return StationSchema.model_validate(station)
