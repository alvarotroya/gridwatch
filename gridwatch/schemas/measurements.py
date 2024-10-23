from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict

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

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MeasurementCreateSchema(BaseModel):
    id: UUID = uuid4()
    station_id: UUID | None = None
    transformer_id: UUID | None = None
    connection_id: UUID | None = None
    device_id: UUID

    value: float
    measurement_type: MeasurementType

    measured_at: datetime
    sent_at: datetime


class MeasurementUpdateSchema(BaseModel):
    """Assumption: measurements can be made and deleted, but not edited"""

    pass
