from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from gridwatch.crud import transformers as crud_transformers
from gridwatch.database import get_db
from gridwatch.schemas.transformers import (
    TransformerSchema,
    TransformerUpdateSchema,
)

router = APIRouter()

DatabaseDep = Annotated[Session, Depends(get_db)]


@router.get("/transformers", response_model=list[TransformerSchema])
def get_transformers(db: DatabaseDep) -> list[TransformerSchema]:
    return crud_transformers.get_transformers(db)


@router.get("/transformers/{transformer_id}", response_model=TransformerSchema)
def get_transformer(transformer_id: UUID, db: DatabaseDep) -> TransformerSchema:
    return crud_transformers.get_transformer(db, transformer_id)


@router.patch("/transformers/{transformer_id}", response_model=TransformerSchema)
def patch_transformer(
    transformer_id: UUID, transformer_update: TransformerUpdateSchema, db: DatabaseDep
) -> TransformerSchema:
    return crud_transformers.update_transformer(db, transformer_id, transformer_update)


@router.delete("/transformers/{transformer_id}", response_model=TransformerSchema)
def delete_transformer(transformer_id: UUID, db: DatabaseDep) -> TransformerSchema:
    return crud_transformers.delete_transformer(db, transformer_id)
