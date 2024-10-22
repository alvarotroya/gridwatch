from uuid import UUID

from sqlalchemy.orm import Session

from gridwatch.crud.exceptions import DatabaseEntityNotFound
from gridwatch.models.connections import ConnectionModel
from gridwatch.schemas.connections import (
    ConnectionCreateSchema,
    ConnectionSchema,
    ConnectionUpdateSchema,
)


def get_connections(db: Session) -> list[ConnectionSchema]:
    return [
        ConnectionSchema.model_validate(connection)
        for connection in db.query(ConnectionModel).all()
    ]


def get_connection(db: Session, connection_id: UUID) -> ConnectionSchema:
    connection = (
        db.query(ConnectionModel).filter(ConnectionModel.id == connection_id).first()
    )

    if connection is None:
        raise DatabaseEntityNotFound(
            f"Could not find Connection with id {connection_id}"
        )

    return ConnectionSchema.model_validate(connection)


def create_connection(
    db: Session, connection_create: ConnectionCreateSchema
) -> ConnectionSchema:
    connection = ConnectionModel(**connection_create.model_dump())
    db.add(connection)
    db.commit()

    db.refresh(connection)

    return ConnectionSchema.model_validate(connection)


def update_connection(
    db: Session, connection_id: UUID, connection_update: ConnectionUpdateSchema
) -> ConnectionSchema:
    connection = (
        db.query(ConnectionModel).filter(ConnectionModel.id == connection_id).first()
    )

    if connection is None:
        raise DatabaseEntityNotFound(
            f"Could not find Connection with id {connection_id}"
        )

    # Update only the fields that are provided in the request
    for key, value in connection_update.model_dump(exclude_unset=True).items():
        setattr(connection, key, value)

    db.commit()
    db.refresh(connection)

    return ConnectionSchema.model_validate(connection)


def delete_connection(db: Session, connection_id: UUID) -> ConnectionSchema:
    connection = (
        db.query(ConnectionModel).filter(ConnectionModel.id == connection_id).first()
    )

    if connection is None:
        raise DatabaseEntityNotFound(
            f"Could not find Connection with id {connection_id}"
        )

    db.delete(connection)
    db.commit()

    return ConnectionSchema.model_validate(connection)
