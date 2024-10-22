from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict


class TransformerSchema(BaseModel):
    id: UUID
    station_id: UUID
    name: str
    external_id: str | None

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TransformerCreateSchema(BaseModel):
    id: UUID = uuid4()
    station_id: UUID
    name: str
    external_id: str | None = None


class TransformerUpdateSchema(BaseModel):
    station_id: UUID | None = None
    name: str | None = None
    external_id: str | None = None
