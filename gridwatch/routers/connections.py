from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from gridwatch.crud import connections as crud_connections
from gridwatch.database import get_db
from gridwatch.schemas.connections import (
    ConnectionCreateSchema,
    ConnectionSchema,
    ConnectionUpdateSchema,
)

router = APIRouter()

DatabaseDep = Annotated[Session, Depends(get_db)]


@router.get("/connections", response_model=list[ConnectionSchema])
def get_connections(db: DatabaseDep) -> list[ConnectionSchema]:
    return crud_connections.get_connections(db)


@router.get("/connections/{connection_id}", response_model=ConnectionSchema)
def get_connection(connection_id: UUID, db: DatabaseDep) -> ConnectionSchema:
    return crud_connections.get_connection(db, connection_id)


@router.post("/connections", response_model=ConnectionSchema)
def post_connection(
    connection_create: ConnectionCreateSchema, db: DatabaseDep
) -> ConnectionSchema:
    return crud_connections.create_connection(db, connection_create)


@router.patch("/connections/{connection_id}", response_model=ConnectionSchema)
def patch_connection(
    connection_id: UUID, connection_update: ConnectionUpdateSchema, db: DatabaseDep
) -> ConnectionSchema:
    return crud_connections.update_connection(db, connection_id, connection_update)


@router.delete("/connections/{connection_id}", response_model=ConnectionSchema)
def delete_connection(connection_id: UUID, db: DatabaseDep) -> ConnectionSchema:
    return crud_connections.delete_connection(db, connection_id)
