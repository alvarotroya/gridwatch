from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from gridwatch.crud.exceptions import DatabaseEntityNotFound
from gridwatch.models.connections import ConnectionModel
from gridwatch.schemas.connections import (
    ConnectionCreateSchema,
    ConnectionSchema,
    ConnectionUpdateSchema,
)


async def get_connections(db: AsyncSession) -> list[ConnectionSchema]:
    result = await db.execute(select(ConnectionModel))
    connections = result.scalars().all()
    return [ConnectionSchema.model_validate(connection) for connection in connections]


async def get_connection(db: AsyncSession, connection_id: UUID) -> ConnectionSchema:
    result = await db.execute(
        select(ConnectionModel).where(ConnectionModel.id == connection_id)
    )
    connection = result.scalar()

    if connection is None:
        raise DatabaseEntityNotFound(
            f"Could not find Connection with id {connection_id}"
        )

    return ConnectionSchema.model_validate(connection)


async def create_connection(
    db: AsyncSession, connection_create: ConnectionCreateSchema
) -> ConnectionSchema:
    connection = ConnectionModel(**connection_create.model_dump())
    db.add(connection)
    await db.commit()
    await db.refresh(connection)
    return ConnectionSchema.model_validate(connection)


async def update_connection(
    db: AsyncSession, connection_id: UUID, connection_update: ConnectionUpdateSchema
) -> ConnectionSchema:
    result = await db.execute(
        select(ConnectionModel).where(ConnectionModel.id == connection_id)
    )
    connection = result.scalar()

    if connection is None:
        raise DatabaseEntityNotFound(
            f"Could not find Connection with id {connection_id}"
        )

    # Update only the fields that are provided in the request
    for key, value in connection_update.model_dump(exclude_unset=True).items():
        setattr(connection, key, value)

    await db.commit()
    await db.refresh(connection)
    return ConnectionSchema.model_validate(connection)


async def delete_connection(db: AsyncSession, connection_id: UUID) -> ConnectionSchema:
    result = await db.execute(
        select(ConnectionModel).where(ConnectionModel.id == connection_id)
    )
    connection = result.scalar()

    if connection is None:
        raise DatabaseEntityNotFound(
            f"Could not find Connection with id {connection_id}"
        )

    await db.delete(connection)
    await db.commit()
    return ConnectionSchema.model_validate(connection)
