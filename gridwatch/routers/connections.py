from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from gridwatch.crud import connections as crud_connections
from gridwatch.database import get_db
from gridwatch.schemas.connections import (
    ConnectionSchema,
    ConnectionUpdateSchema,
)

router = APIRouter()

DatabaseDep = Annotated[AsyncSession, Depends(get_db)]


@router.get("/connections", response_model=list[ConnectionSchema])
async def get_connections(db: DatabaseDep) -> list[ConnectionSchema]:
    return await crud_connections.get_connections(db)


@router.get("/connections/{connection_id}", response_model=ConnectionSchema)
async def get_connection(connection_id: UUID, db: DatabaseDep) -> ConnectionSchema:
    return await crud_connections.get_connection(db, connection_id)


@router.patch("/connections/{connection_id}", response_model=ConnectionSchema)
async def patch_connection(
    connection_id: UUID, connection_update: ConnectionUpdateSchema, db: DatabaseDep
) -> ConnectionSchema:
    return await crud_connections.update_connection(
        db, connection_id, connection_update
    )


@router.delete("/connections/{connection_id}", response_model=ConnectionSchema)
async def delete_connection(connection_id: UUID, db: DatabaseDep) -> ConnectionSchema:
    return await crud_connections.delete_connection(db, connection_id)
