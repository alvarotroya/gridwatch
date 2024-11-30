from uuid import UUID

from sqlalchemy import desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from gridwatch.crud.exceptions import DatabaseEntityNotFound
from gridwatch.models.measurements import MeasurementModel
from gridwatch.schemas.measurements import (
    MeasurementDatabaseCreateSchema,
    MeasurementSchema,
    MeasurementUpdateSchema,
)


async def get_measurements(db: AsyncSession) -> list[MeasurementSchema]:
    result = await db.execute(
        select(MeasurementModel).order_by(desc(MeasurementModel.measured_at))
    )
    measurements = result.scalars().all()
    return [
        MeasurementSchema.model_validate(measurement) for measurement in measurements
    ]


async def get_measurement(db: AsyncSession, measurement_id: UUID) -> MeasurementSchema:
    result = await db.execute(
        select(MeasurementModel).where(MeasurementModel.id == measurement_id)
    )
    measurement = result.scalar()

    if measurement is None:
        raise DatabaseEntityNotFound(
            f"Could not find Measurement with id {measurement_id}"
        )

    return MeasurementSchema.model_validate(measurement)


async def create_measurement(
    db: AsyncSession, measurement_create: MeasurementDatabaseCreateSchema
) -> MeasurementSchema:
    measurement = MeasurementModel(**measurement_create.model_dump())
    db.add(measurement)
    await db.commit()
    await db.refresh(measurement)
    return MeasurementSchema.model_validate(measurement)


async def update_measurement(
    db: AsyncSession, measurement_id: UUID, measurement_update: MeasurementUpdateSchema
) -> MeasurementSchema:
    result = await db.execute(
        select(MeasurementModel).where(MeasurementModel.id == measurement_id)
    )
    measurement = result.scalar()

    if measurement is None:
        raise DatabaseEntityNotFound(
            f"Could not find Measurement with id {measurement_id}"
        )

    # Update only the fields that are provided in the request
    for key, value in measurement_update.model_dump(exclude_unset=True).items():
        setattr(measurement, key, value)

    await db.commit()
    await db.refresh(measurement)
    return MeasurementSchema.model_validate(measurement)


async def delete_measurement(
    db: AsyncSession, measurement_id: UUID
) -> MeasurementSchema:
    result = await db.execute(
        select(MeasurementModel).where(MeasurementModel.id == measurement_id)
    )
    measurement = result.scalar()

    if measurement is None:
        raise DatabaseEntityNotFound(
            f"Could not find Measurement with id {measurement_id}"
        )

    await db.delete(measurement)
    await db.commit()
    return MeasurementSchema.model_validate(measurement)
