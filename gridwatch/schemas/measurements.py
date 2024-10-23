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


class MeasurementAPICreateSchema(BaseModel):
    """This is the payload used to create a new measurement."""

    id: UUID = uuid4()
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


class MeasurementUpdateSchema(BaseModel):
    """Assumption: measurements can be made and deleted, but not edited"""

    pass
