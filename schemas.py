from pydantic import BaseModel, ConfigDict


class ZadatakUnos(BaseModel):
    naslov: str
    zavrsen: bool = False


class Zadatak(ZadatakUnos):
    id: int
    model_config = ConfigDict(from_attributes=True)