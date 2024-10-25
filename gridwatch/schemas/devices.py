from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from gridwatch.models.enums import ComponentType, DeviceType, HealthStatus


class DeviceSchema(BaseModel):
    id: UUID
    device_type: DeviceType
    component_id: UUID
    component_type: ComponentType
    name: str
    external_id: str | None

    device_specs: dict
    device_config: dict

    health_status: HealthStatus
    last_healthcheck_at: datetime
    installed_at: datetime

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DeviceCreateSchema(BaseModel):
    device_type: DeviceType
    component_id: UUID
    component_type: ComponentType
    name: str
    external_id: str | None

    device_specs: dict | None = None
    device_config: dict | None = None

    health_status: HealthStatus = HealthStatus.OK


class DeviceUpdateSchema(BaseModel):
    name: str | None = None
    external_id: str | None = None
    component_id: UUID | None = None
    component_type: ComponentType | None = None
    device_specs: dict | None = None
    device_config: dict | None = None
