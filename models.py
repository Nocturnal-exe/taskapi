from sqlalchemy import Column, Integer, String, Boolean
from database import Base


class ZadatakDB(Base):
    __tablename__ = "zadaci"

    id = Column(Integer, primary_key=True, index=True)
    naslov = Column(String, nullable=False)
    zavrsen = Column(Boolean, default=False)