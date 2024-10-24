from typing import Annotated
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from gridwatch.crud import measurements as crud_measurements
from gridwatch.database import get_db
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
    # TODO: do some magic to determine component information
    measurement_db_create = MeasurementDatabaseCreateSchema(
        **measurement.model_dump(),
        station_id=uuid4(),
        transformer_id=uuid4(),
        connection_id=uuid4(),
    )
    return crud_measurements.create_measurement(db, measurement_db_create)
