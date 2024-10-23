from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from gridwatch.crud import measurements as crud_measurements
from gridwatch.database import get_db
from gridwatch.schemas.measurements import (
    MeasurementCreateSchema,
    MeasurementSchema,
)

router = APIRouter()

DatabaseDep = Annotated[Session, Depends(get_db)]


@router.get("/measurements", response_model=list[MeasurementSchema])
def get_measurements(db: DatabaseDep) -> list[MeasurementSchema]:
    return crud_measurements.get_measurements(db)


@router.get("/measurement/{measurement_id}", response_model=MeasurementSchema)
def get_measurement(measurement_id: UUID, db: DatabaseDep) -> MeasurementSchema:
    return crud_measurements.get_measurement(db, measurement_id)


@router.post("/measurement", response_model=MeasurementSchema)
def post_measurement(
    measurement_create: MeasurementCreateSchema, db: DatabaseDep
) -> MeasurementSchema:
    return crud_measurements.create_measurement(db, measurement_create)


@router.delete("/measurement/{measurement_id}", response_model=MeasurementSchema)
def delete_measurement(measurement_id: UUID, db: DatabaseDep) -> MeasurementSchema:
    return crud_measurements.delete_measurement(db, measurement_id)
