from uuid import UUID

from sqlalchemy.orm import Session

from gridwatch.crud.exceptions import DatabaseEntityNotFound
from gridwatch.models.transformers import TransformerModel
from gridwatch.schemas.transformers import (
    TransformerCreateSchema,
    TransformerSchema,
    TransformerUpdateSchema,
)


def get_transformers(db: Session) -> list[TransformerSchema]:
    return [
        TransformerSchema.model_validate(transformer)
        for transformer in db.query(TransformerModel).all()
    ]


def get_transformer(db: Session, transformer_id: UUID) -> TransformerSchema:
    transformer = (
        db.query(TransformerModel).filter(TransformerModel.id == transformer_id).first()
    )

    if transformer is None:
        raise DatabaseEntityNotFound(
            f"Could not find Transformer with id {transformer_id}"
        )

    return TransformerSchema.model_validate(transformer)


def create_transformer(
    db: Session, transformer_create: TransformerCreateSchema
) -> TransformerSchema:
    transformer = TransformerModel(**transformer_create.model_dump())
    db.add(transformer)
    db.commit()

    db.refresh(transformer)

    return TransformerSchema.model_validate(transformer)


def update_transformer(
    db: Session, transformer_id: UUID, transformer_update: TransformerUpdateSchema
) -> TransformerSchema:
    transformer = (
        db.query(TransformerModel).filter(TransformerModel.id == transformer_id).first()
    )

    if transformer is None:
        raise DatabaseEntityNotFound(
            f"Could not find Transformer with id {transformer_id}"
        )

    # Update only the fields that are provided in the request
    for key, value in transformer_update.model_dump(exclude_unset=True).items():
        setattr(transformer, key, value)

    db.commit()
    db.refresh(transformer)

    return TransformerSchema.model_validate(transformer)


def delete_transformer(db: Session, transformer_id: UUID) -> TransformerSchema:
    transformer = (
        db.query(TransformerModel).filter(TransformerModel.id == transformer_id).first()
    )

    if transformer is None:
        raise DatabaseEntityNotFound(
            f"Could not find Transformer with id {transformer_id}"
        )

    db.delete(transformer)
    db.commit()

    return TransformerSchema.model_validate(transformer)
