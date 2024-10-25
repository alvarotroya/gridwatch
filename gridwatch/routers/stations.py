from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy import desc
from sqlalchemy.orm import Session

from gridwatch.crud import stations as crud_stations
from gridwatch.crud import transformers as crud_transformers
from gridwatch.database import get_db
from gridwatch.models.measurements import MeasurementModel
from gridwatch.schemas.measurements import MeasurementSchema
from gridwatch.schemas.stations import (
    StationCreateSchema,
    StationSchema,
    StationUpdateSchema,
)
from gridwatch.schemas.transformers import (
    TransformerAPICreateSchema,
    TransformerCreateSchema,
    TransformerSchema,
)

router = APIRouter()

DatabaseDep = Annotated[Session, Depends(get_db)]


# CRUD endpoints


@router.get("/stations", response_model=list[StationSchema])
def get_stations(db: DatabaseDep) -> list[StationSchema]:
    return crud_stations.get_stations(db)


@router.get("/stations/{station_id}", response_model=StationSchema)
def get_station(station_id: UUID, db: DatabaseDep) -> StationSchema:
    return crud_stations.get_station(db, station_id)


@router.post("/stations", response_model=StationSchema)
def post_station(station_create: StationCreateSchema, db: DatabaseDep) -> StationSchema:
    return crud_stations.create_station(db, station_create)


@router.patch("/stations/{station_id}", response_model=StationSchema)
def patch_station(
    station_id: UUID, station_update: StationUpdateSchema, db: DatabaseDep
) -> StationSchema:
    return crud_stations.update_station(db, station_id, station_update)


@router.delete("/stations/{station_id}", response_model=StationSchema)
def delete_station(station_id: UUID, db: DatabaseDep) -> StationSchema:
    return crud_stations.delete_station(db, station_id)


# Navigations


@router.post("/stations/{station_id}/transformers", response_model=TransformerSchema)
def post_transformer(
    station_id: UUID, transformer_create: TransformerAPICreateSchema, db: DatabaseDep
) -> TransformerSchema:
    transformer_db_create = TransformerCreateSchema(
        **transformer_create.model_dump(), station_id=station_id
    )
    return crud_transformers.create_transformer(db, transformer_db_create)


@router.get(
    "/station/{station_id}/measurements", response_model=list[MeasurementSchema]
)
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

    measurements = (
        query.order_by(desc(MeasurementModel.measured_at))
        .limit(limit)
        .offset(skip)
        .all()
    )

    return [MeasurementSchema.model_validate(model) for model in measurements]
