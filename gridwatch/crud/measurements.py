from uuid import UUID

from sqlalchemy import desc
from sqlalchemy.orm import Session

from gridwatch.crud.exceptions import DatabaseEntityNotFound
from gridwatch.models.measurements import MeasurementModel
from gridwatch.schemas.measurements import (
    MeasurementDatabaseCreateSchema,
    MeasurementSchema,
    MeasurementUpdateSchema,
)


def get_measurements(db: Session) -> list[MeasurementSchema]:
    return [
        MeasurementSchema.model_validate(measurement)
        for measurement in db.query(MeasurementModel)
        .order_by(desc(MeasurementModel.measured_at))
        .all()
    ]


def get_measurement(db: Session, measurement_id: UUID) -> MeasurementSchema:
    measurement = (
        db.query(MeasurementModel).filter(MeasurementModel.id == measurement_id).first()
    )

    if measurement is None:
        raise DatabaseEntityNotFound(
            f"Could not find Measurement with id {measurement_id}"
        )

    return MeasurementSchema.model_validate(measurement)


def create_measurement(
    db: Session, measurement_create: MeasurementDatabaseCreateSchema
) -> MeasurementSchema:
    measurement = MeasurementModel(**measurement_create.model_dump())
    db.add(measurement)
    db.commit()

    db.refresh(measurement)

    return MeasurementSchema.model_validate(measurement)


def update_measurement(
    db: Session, measurement_id: UUID, measurement_update: MeasurementUpdateSchema
) -> MeasurementSchema:
    measurement = (
        db.query(MeasurementModel).filter(MeasurementModel.id == measurement_id).first()
    )

    if measurement is None:
        raise DatabaseEntityNotFound(
            f"Could not find Measurement with id {measurement_id}"
        )

    # Update only the fields that are provided in the request
    for key, value in measurement_update.model_dump(exclude_unset=True).items():
        setattr(measurement, key, value)

    db.commit()
    db.refresh(measurement)

    return MeasurementSchema.model_validate(measurement)


def delete_measurement(db: Session, measurement_id: UUID) -> MeasurementSchema:
    measurement = (
        db.query(MeasurementModel).filter(MeasurementModel.id == measurement_id).first()
    )

    if measurement is None:
        raise DatabaseEntityNotFound(
            f"Could not find Measurement with id {measurement_id}"
        )

    db.delete(measurement)
    db.commit()

    return MeasurementSchema.model_validate(measurement)
