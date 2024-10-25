from uuid import uuid4

from sqlalchemy import TIMESTAMP, UUID, Column, Enum, Float, ForeignKey, func
from sqlalchemy.orm import relationship

from gridwatch.database import Base
from gridwatch.models.enums import MeasurementType


class MeasurementModel(Base):
    __tablename__ = "measurements"

    id = Column(UUID, primary_key=True, default=uuid4, index=True)
    station_id = Column(UUID, ForeignKey("stations.id"), nullable=True)
    transformer_id = Column(UUID, ForeignKey("transformers.id"), nullable=True)
    connection_id = Column(UUID, ForeignKey("connections.id"), nullable=True)
    device_id = Column(UUID, ForeignKey("devices.id"))

    value = Column(Float)
    measurement_type = Column(Enum(MeasurementType))
    measured_at = Column(TIMESTAMP)
    sent_at = Column(TIMESTAMP)

    customer_id = Column(UUID, ForeignKey("customers.id"))

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(
        TIMESTAMP, server_default=func.now(), server_onupdate=func.now()
    )

    station = relationship("StationModel", back_populates="measurements", cascade="all")
    transformer = relationship(
        "TransformerModel", back_populates="measurements", cascade="all"
    )
    connection = relationship(
        "ConnectionModel", back_populates="measurements", cascade="all"
    )
    device = relationship("DeviceModel", back_populates="measurements", cascade="all")
