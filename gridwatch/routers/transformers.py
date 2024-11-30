from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from gridwatch.crud import connections as crud_connections
from gridwatch.crud import transformers as crud_transformers
from gridwatch.database import get_db
from gridwatch.schemas.connections import (
    ConnectionAPICreateSchema,
    ConnectionCreateSchema,
    ConnectionSchema,
)
from gridwatch.schemas.transformers import (
    TransformerSchema,
    TransformerUpdateSchema,
)

router = APIRouter()

DatabaseDep = Annotated[AsyncSession, Depends(get_db)]


@router.get("/transformers", response_model=list[TransformerSchema])
async def get_transformers(db: DatabaseDep) -> list[TransformerSchema]:
    return await crud_transformers.get_transformers(db)


@router.get("/transformers/{transformer_id}", response_model=TransformerSchema)
async def get_transformer(transformer_id: UUID, db: DatabaseDep) -> TransformerSchema:
    return await crud_transformers.get_transformer(db, transformer_id)


@router.patch("/transformers/{transformer_id}", response_model=TransformerSchema)
async def patch_transformer(
    transformer_id: UUID, transformer_update: TransformerUpdateSchema, db: DatabaseDep
) -> TransformerSchema:
    return await crud_transformers.update_transformer(
        db, transformer_id, transformer_update
    )


@router.delete("/transformers/{transformer_id}", response_model=TransformerSchema)
async def delete_transformer(
    transformer_id: UUID, db: DatabaseDep
) -> TransformerSchema:
    return await crud_transformers.delete_transformer(db, transformer_id)


@router.post(
    "/transformers/{transformer_id}/connections", response_model=ConnectionSchema
)
async def post_connection(
    transformer_id: UUID, connection_create: ConnectionAPICreateSchema, db: DatabaseDep
) -> ConnectionSchema:
    connection_db_create = ConnectionCreateSchema(
        **connection_create.model_dump(), transformer_id=transformer_id
    )
    return await crud_connections.create_connection(db, connection_db_create)
