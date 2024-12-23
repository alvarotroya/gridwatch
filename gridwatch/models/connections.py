from uuid import uuid4

from sqlalchemy import TIMESTAMP, UUID, Column, ForeignKey, String, func
from sqlalchemy.orm import relationship

from gridwatch.database import Base


class ConnectionModel(Base):
    __tablename__ = "connections"

    id = Column(UUID, primary_key=True, default=uuid4, index=True)
    name = Column(String)
    customer_id = Column(UUID, ForeignKey("customers.id"))
    transformer_id = Column(UUID, ForeignKey("transformers.id"), nullable=False)

    external_id = Column(String, nullable=True)

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(
        TIMESTAMP, server_default=func.now(), server_onupdate=func.now()
    )

    transformer = relationship(
        "TransformerModel", back_populates="connections", cascade="all"
    )
    measurements = relationship(
        "MeasurementModel", back_populates="connection", cascade="all, delete-orphan"
    )
