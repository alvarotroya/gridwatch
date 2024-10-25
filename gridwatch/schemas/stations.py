from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class StationSchema(BaseModel):
    id: UUID
    name: str
    street: str
    house_number: str
    city: str
    state: str
    zip_code: str
    country: str
    latitude: float | None = None
    longitude: float | None = None

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class StationCreateSchema(BaseModel):
    name: str
    street: str
    house_number: str
    city: str
    state: str
    zip_code: str
    country: str
    latitude: float | None = None
    longitude: float | None = None


class StationUpdateSchema(BaseModel):
    name: str | None = None
    street: str | None = None
    house_number: str | None = None
    city: str | None = None
    state: str | None = None
    zip_code: str | None = None
    country: str | None = None
