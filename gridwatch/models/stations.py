from sqlalchemy import TIMESTAMP, UUID, Column, Float, ForeignKey, String, func

from gridwatch.database import Base


class StationModel(Base):
    __tablename__ = "stations"

    id = Column(UUID, primary_key=True, index=True)
    name = Column(String)
    customer_id = Column(UUID, ForeignKey("customers.id"))
    street = Column(String)
    house_number = Column(String)
    city = Column(String)
    state = Column(String)
    zip_code = Column(String)
    country = Column(String)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(
        TIMESTAMP, server_default=func.now(), server_onupdate=func.now()
    )
