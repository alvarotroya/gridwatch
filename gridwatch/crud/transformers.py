from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from gridwatch.crud.exceptions import DatabaseEntityNotFound
from gridwatch.models.transformers import TransformerModel
from gridwatch.schemas.transformers import (
    TransformerCreateSchema,
    TransformerSchema,
    TransformerUpdateSchema,
)


async def get_transformers(db: AsyncSession) -> list[TransformerSchema]:
    result = await db.execute(select(TransformerModel))
    transformers = result.scalars().all()
    return [
        TransformerSchema.model_validate(transformer) for transformer in transformers
    ]


async def get_transformer(db: AsyncSession, transformer_id: UUID) -> TransformerSchema:
    result = await db.execute(
        select(TransformerModel).where(TransformerModel.id == transformer_id)
    )
    transformer = result.scalar()

    if transformer is None:
        raise DatabaseEntityNotFound(
            f"Could not find Transformer with id {transformer_id}"
        )

    return TransformerSchema.model_validate(transformer)


async def create_transformer(
    db: AsyncSession, transformer_create: TransformerCreateSchema
) -> TransformerSchema:
    transformer = TransformerModel(**transformer_create.model_dump())
    db.add(transformer)
    await db.commit()
    await db.refresh(transformer)
    return TransformerSchema.model_validate(transformer)


async def update_transformer(
    db: AsyncSession, transformer_id: UUID, transformer_update: TransformerUpdateSchema
) -> TransformerSchema:
    result = await db.execute(
        select(TransformerModel).where(TransformerModel.id == transformer_id)
    )
    transformer = result.scalar()

    if transformer is None:
        raise DatabaseEntityNotFound(
            f"Could not find Transformer with id {transformer_id}"
        )

    # Update only the fields that are provided in the request
    for key, value in transformer_update.model_dump(exclude_unset=True).items():
        setattr(transformer, key, value)

    await db.commit()
    await db.refresh(transformer)
    return TransformerSchema.model_validate(transformer)


async def delete_transformer(
    db: AsyncSession, transformer_id: UUID
) -> TransformerSchema:
    result = await db.execute(
        select(TransformerModel).where(TransformerModel.id == transformer_id)
    )
    transformer = result.scalar()

    if transformer is None:
        raise DatabaseEntityNotFound(
            f"Could not find Transformer with id {transformer_id}"
        )

    await db.delete(transformer)
    await db.commit()
    return TransformerSchema.model_validate(transformer)
