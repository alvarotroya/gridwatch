from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ConnectionSchema(BaseModel):
    id: UUID
    transformer_id: UUID
    name: str
    external_id: str | None

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ConnectionAPICreateSchema(BaseModel):
    name: str
    external_id: str | None = None


class ConnectionCreateSchema(BaseModel):
    transformer_id: UUID
    name: str
    external_id: str | None = None


class ConnectionUpdateSchema(BaseModel):
    transformer_id: UUID | None = None
    name: str | None = None
    external_id: str | None = None
