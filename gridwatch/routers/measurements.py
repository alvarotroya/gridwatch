from datetime import datetime
from typing import Annotated
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from gridwatch.crud import measurements as crud_measurements
from gridwatch.database import get_db
from gridwatch.models.measurements import MeasurementModel
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


@router.get("/measurements/{station_id}", response_model=list[MeasurementSchema])
def get_measurements_by_station_id(
    station_id: UUID,
    db: DatabaseDep,
    transformer_id: UUID | None = None,
    connection_id: UUID | None = None,
    device_id: UUID | None = None,
    since: datetime | None = None,
    until: datetime | None = None,
    limit: int = 100,
    skip: int = 0,
) -> list[MeasurementSchema]:
    query = db.query(MeasurementModel).filter(MeasurementModel.station_id == station_id)

    if since:
        query = query.filter(MeasurementModel.measured_at >= since)
    if until:
        query = query.filter(MeasurementModel.measured_at <= until)

    if transformer_id:
        query = query.filter(MeasurementModel.transformer_id == transformer_id)
    if connection_id:
        query = query.filter(MeasurementModel.connection_id == connection_id)
    if device_id:
        query = query.filter(MeasurementModel.device_id == device_id)

    measurements = query.limit(limit).offset(skip).all()

    return [MeasurementSchema.model_validate(model) for model in measurements]


@router.get("/measurement/{measurement_id}", response_model=MeasurementSchema)
def get_measurement(measurement_id: UUID, db: DatabaseDep) -> MeasurementSchema:
    return crud_measurements.get_measurement(db, measurement_id)


@router.post("/measurement", response_model=MeasurementSchema)
def post_measurement(
    measurement_create: MeasurementAPICreateSchema, db: DatabaseDep
) -> MeasurementSchema:
    return create_database_measurement(db, measurement_create)


@router.post("/measurement:bulk", response_model=list[MeasurementSchema])
def post_measurements(
    measurements_create: list[MeasurementAPICreateSchema], db: DatabaseDep
) -> list[MeasurementSchema]:
    results = []

    for measurement in measurements_create:
        results.append(create_database_measurement(db, measurement))

    return results


@router.delete("/measurement/{measurement_id}", response_model=MeasurementSchema)
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
