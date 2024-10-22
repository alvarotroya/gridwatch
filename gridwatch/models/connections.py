from sqlalchemy import TIMESTAMP, UUID, Column, ForeignKey, String, func

from gridwatch.database import Base


class ConnectionModel(Base):
    __tablename__ = "connections"

    id = Column(UUID, primary_key=True, index=True)
    name = Column(String)
    customer_id = Column(UUID, ForeignKey("customers.id"))
    transformer_id = Column(UUID, ForeignKey("transformer.id"), nullable=False)

    external_id = Column(String, nullable=True)

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(
        TIMESTAMP, server_default=func.now(), server_onupdate=func.now()
    )
