from uuid import uuid4

from sqlalchemy import UUID, Column, String

from gridwatch.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(UUID, primary_key=True, default=uuid4, index=True)
    name = Column(String)
