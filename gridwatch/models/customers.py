from sqlalchemy import UUID, Column, String

from gridwatch.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(UUID, primary_key=True, index=True)
    name = Column(String)
