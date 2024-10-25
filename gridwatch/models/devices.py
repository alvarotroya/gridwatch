from uuid import uuid4

from sqlalchemy import TIMESTAMP, UUID, Column, Enum, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from gridwatch.database import Base
from gridwatch.models.enums import ComponentType, DeviceType, HealthStatus


class DeviceModel(Base):
    __tablename__ = "devices"

    id = Column(UUID, primary_key=True, default=uuid4, index=True)
    name = Column(String)
    device_type = Column(Enum(DeviceType))
    component_id = Column(UUID)
    component_type = Column(Enum(ComponentType))
    device_specs = Column(JSONB)
    device_config = Column(JSONB)

    health_status = Column(Enum(HealthStatus))
    last_healthcheck_at = Column(TIMESTAMP, server_default=func.now())
    installed_at = Column(TIMESTAMP, server_default=func.now())

    external_id = Column(String, nullable=True)
    customer_id = Column(UUID, ForeignKey("customers.id"))

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(
        TIMESTAMP, server_default=func.now(), server_onupdate=func.now()
    )

    measurements = relationship(
        "MeasurementModel", back_populates="device", cascade="all, delete-orphan"
    )
