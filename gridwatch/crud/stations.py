from uuid import UUID

from sqlalchemy.orm import Session

from gridwatch.crud.exceptions import DatabaseEntityNotFound
from gridwatch.models.stations import StationModel
from gridwatch.schemas.stations import (
    StationCreateSchema,
    StationSchema,
    StationUpdateSchema,
)


def get_stations(db: Session) -> list[StationSchema]:
    return [
        StationSchema.model_validate(station)
        for station in db.query(StationModel).all()
    ]


def get_station(db: Session, station_id: UUID) -> StationSchema:
    station = db.query(StationModel).filter(StationModel.id == station_id).first()

    if station is None:
        raise DatabaseEntityNotFound(f"Could not find Station with id {station_id}")

    return StationSchema.model_validate(station)


def create_station(db: Session, station_create: StationCreateSchema) -> StationSchema:
    station = StationModel(**station_create.model_dump())
    db.add(station)
    db.commit()

    db.refresh(station)

    return StationSchema.model_validate(station)


def update_station(
    db: Session, station_id: UUID, station_update: StationUpdateSchema
) -> StationSchema:
    station = db.query(StationModel).filter(StationModel.id == station_id).first()

    if station is None:
        raise DatabaseEntityNotFound(f"Could not find Station with id {station_id}")

    # Update only the fields that are provided in the request
    for key, value in station_update.model_dump(exclude_unset=True).items():
        setattr(station, key, value)

    db.commit()
    db.refresh(station)

    return StationSchema.model_validate(station)


def delete_station(db: Session, station_id: UUID) -> StationSchema:
    station = db.query(StationModel).filter(StationModel.id == station_id).first()

    if station is None:
        raise DatabaseEntityNotFound(f"Could not find Station with id {station_id}")

    db.delete(station)
    db.commit()

    return StationSchema.model_validate(station)
