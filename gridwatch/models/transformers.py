from sqlalchemy import TIMESTAMP, UUID, Column, ForeignKey, String, func

from gridwatch.database import Base


class TransformerModel(Base):
    __tablename__ = "transformers"

    id = Column(UUID, primary_key=True, index=True)
    name = Column(String)
    customer_id = Column(UUID, ForeignKey("customers.id"))
    station_id = Column(UUID, ForeignKey("stations.id"), nullable=False)

    external_id = Column(String, nullable=True)

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(
        TIMESTAMP, server_default=func.now(), server_onupdate=func.now()
    )
