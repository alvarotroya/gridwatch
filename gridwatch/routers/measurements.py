from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

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

DatabaseDep = Annotated[Session, Depends(get_db)]


@router.get("/measurements", response_model=list[MeasurementSchema])
def get_measurements(db: DatabaseDep) -> list[MeasurementSchema]:
    return crud_measurements.get_measurements(db)


@router.get("/measurements/{measurement_id}", response_model=MeasurementSchema)
def get_measurement(measurement_id: UUID, db: DatabaseDep) -> MeasurementSchema:
    return crud_measurements.get_measurement(db, measurement_id)


@router.post("/measurements", response_model=MeasurementSchema)
def post_measurement(
    measurement_create: MeasurementAPICreateSchema, db: DatabaseDep
) -> MeasurementSchema:
    return create_database_measurement(db, measurement_create)


@router.post("/measurements/bulk", response_model=list[MeasurementSchema])
def post_measurements(
    measurements_create: list[MeasurementAPICreateSchema], db: DatabaseDep
) -> list[MeasurementSchema]:
    results = []

    for measurement in measurements_create:
        results.append(create_database_measurement(db, measurement))

    return results


@router.delete("/measurements/{measurement_id}", response_model=MeasurementSchema)
def delete_measurement(measurement_id: UUID, db: DatabaseDep) -> MeasurementSchema:
    return crud_measurements.delete_measurement(db, measurement_id)


# TODO: extract to a separate method/file and write tests for this
def create_database_measurement(
    db: Session, measurement: MeasurementAPICreateSchema
) -> MeasurementSchema:
    device = db.query(DeviceModel).filter(DeviceModel.id == measurement.device_id).one()

    match device.component_type:
        case ComponentType.CONNECTION:
            connection = (
                db.query(ConnectionModel)
                .filter(ConnectionModel.id == device.component_id)
                .one()
            )
            connection_id = UUID(str(connection.id))
            transformer_id = connection.transformer.id
            station_id = connection.transformer.station.id

        case ComponentType.TRANSFORMER:
            transformer = (
                db.query(TransformerModel)
                .filter(TransformerModel.id == device.component_id)
                .one()
            )
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

    return crud_measurements.create_measurement(db, measurement_db_create)
