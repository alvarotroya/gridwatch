from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from gridwatch.crud import measurements as crud_measurements
from gridwatch.database import get_db
from gridwatch.models.connections import ConnectionModel
from gridwatch.models.devices import DeviceModel
from gridwatch.models.enums import ComponentType
from gridwatch.models.transformers import TransformerModel
from gridwatch.schemas.measurements import (
    MeasurementAPICreateSchema,
    MeasurementDatabaseCreateSchema,
    MeasurementSchema,
)

router = APIRouter()

DatabaseDep = Annotated[AsyncSession, Depends(get_db)]


@router.get("/measurements", response_model=list[MeasurementSchema])
async def get_measurements(db: DatabaseDep) -> list[MeasurementSchema]:
    return await crud_measurements.get_measurements(db)


@router.get("/measurements/{measurement_id}", response_model=MeasurementSchema)
async def get_measurement(measurement_id: UUID, db: DatabaseDep) -> MeasurementSchema:
    return await crud_measurements.get_measurement(db, measurement_id)


@router.post("/measurements", response_model=MeasurementSchema)
async def post_measurement(
    measurement_create: MeasurementAPICreateSchema, db: DatabaseDep
) -> MeasurementSchema:
    return await create_database_measurement(db, measurement_create)


@router.post("/measurements/bulk", response_model=list[MeasurementSchema])
async def post_measurements(
    measurements_create: list[MeasurementAPICreateSchema], db: DatabaseDep
) -> list[MeasurementSchema]:
    results = []

    for measurement in measurements_create:
        measurement_result = await create_database_measurement(db, measurement)
        results.append(measurement_result)

    return results


@router.delete("/measurements/{measurement_id}", response_model=MeasurementSchema)
async def delete_measurement(
    measurement_id: UUID, db: DatabaseDep
) -> MeasurementSchema:
    return await crud_measurements.delete_measurement(db, measurement_id)


# TODO: extract to a separate method/file and write tests for this
async def create_database_measurement(
    db: AsyncSession, measurement: MeasurementAPICreateSchema
) -> MeasurementSchema:
    device_result = await db.execute(
        select(DeviceModel).filter(DeviceModel.id == measurement.device_id)
    )
    device = device_result.scalar_one()

    match device.component_type:
        case ComponentType.CONNECTION:
            # Eagerly load the transformer and station to avoid lazy-loading issues
            connection_result = await db.execute(
                select(ConnectionModel)
                .options(
                    joinedload(ConnectionModel.transformer).joinedload(
                        TransformerModel.station
                    )
                )
                .filter(ConnectionModel.id == device.component_id)
            )
            connection = connection_result.scalar_one()
            connection_id = UUID(str(connection.id))
            transformer_id = connection.transformer.id
            station_id = connection.transformer.station.id

        case ComponentType.TRANSFORMER:
            # Eagerly load the station to avoid lazy-loading issues
            transformer_result = await db.execute(
                select(TransformerModel)
                .options(joinedload(TransformerModel.station))
                .filter(TransformerModel.id == device.component_id)
            )
            transformer = transformer_result.scalar_one()
            connection_id = None
            transformer_id = UUID(str(transformer.id))
            station_id = transformer.station.id

        case _:
            raise ValueError(
                f"Device of component type '{str(device.component_type)}' is not supported."
            )

    measurement_db_create = MeasurementDatabaseCreateSchema(
        **measurement.model_dump(),
        station_id=station_id,
        transformer_id=transformer_id,
        connection_id=connection_id,
    )

    return await crud_measurements.create_measurement(db, measurement_db_create)
