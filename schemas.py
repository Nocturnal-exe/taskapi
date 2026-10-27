from pydantic import BaseModel, ConfigDict


class ZadatakUnos(BaseModel):
    naslov: str
    zavrsen: bool = False


class Zadatak(ZadatakUnos):
    id: int
    model_config = ConfigDict(from_attributes=True)


class KorisnikUnos(BaseModel):
    korisnicko_ime: str
    lozinka: str


class Korisnik(BaseModel):
    id: int
    korisnicko_ime: str
    model_config = ConfigDict(from_attributes=True)