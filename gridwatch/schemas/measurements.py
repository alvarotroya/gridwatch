from datetime import datetime, timezone
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from gridwatch.models.enums import MeasurementType


class MeasurementSchema(BaseModel):
    id: UUID
    station_id: UUID | None
    transformer_id: UUID | None
    connection_id: UUID | None
    device_id: UUID | None

    value: float
    measurement_type: MeasurementType

    measured_at: datetime
    sent_at: datetime
    received_at: datetime

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MeasurementAPICreateSchema(BaseModel):
    """This is the payload used to create a new measurement."""

    device_id: UUID

    value: float
    measurement_type: MeasurementType

    measured_at: datetime
    sent_at: datetime


class MeasurementDatabaseCreateSchema(MeasurementAPICreateSchema):
    """This model is used to attach component information to a measurement before persisting it to the DB."""

    station_id: UUID | None = None
    transformer_id: UUID | None = None
    connection_id: UUID | None = None

    received_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class MeasurementUpdateSchema(BaseModel):
    """Assumption: measurements can be made and deleted, but not edited"""

    pass
