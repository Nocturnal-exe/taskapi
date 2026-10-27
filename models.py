from sqlalchemy import Column, Integer, String, Boolean
from database import Base


class KorisnikDB(Base):
    __tablename__ = "korisnici"

    id = Column(Integer, primary_key=True, index=True)
    korisnicko_ime = Column(String, unique=True, nullable=False)
    hash_lozinke = Column(String, nullable=False)


class ZadatakDB(Base):
    __tablename__ = "zadaci"

    id = Column(Integer, primary_key=True, index=True)
    naslov = Column(String, nullable=False)
    zavrsen = Column(Boolean, default=False)