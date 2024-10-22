from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from gridwatch.crud import stations as crud_stations
from gridwatch.database import get_db
from gridwatch.schemas.stations import (
    StationCreateSchema,
    StationSchema,
    StationUpdateSchema,
)

router = APIRouter()

DatabaseDep = Annotated[Session, Depends(get_db)]


@router.get("/stations", response_model=list[StationSchema])
def get_stations(db: DatabaseDep) -> list[StationSchema]:
    return crud_stations.get_stations(db)


@router.get("/station/{station_id}", response_model=StationSchema)
def get_station(station_id: UUID, db: DatabaseDep) -> StationSchema:
    return crud_stations.get_station(db, station_id)


@router.post("/station", response_model=StationSchema)
def post_station(station_create: StationCreateSchema, db: DatabaseDep) -> StationSchema:
    return crud_stations.create_station(db, station_create)


@router.patch("/station/{station_id}", response_model=StationSchema)
def patch_station(
    station_id: UUID, station_update: StationUpdateSchema, db: DatabaseDep
) -> StationSchema:
    return crud_stations.update_station(db, station_id, station_update)


@router.delete("/station/{station_id}", response_model=StationSchema)
def delete_station(station_id: UUID, db: DatabaseDep) -> StationSchema:
    return crud_stations.delete_station(db, station_id)
