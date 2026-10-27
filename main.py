from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from database import engine, Base, get_db
from models import ZadatakDB
from schemas import Zadatak, ZadatakUnos

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def home():
    return {"poruka": "Radi!"}


@app.get("/zadaci", response_model=list[Zadatak])
def svi_zadaci(db: Session = Depends(get_db)):
    return db.query(ZadatakDB).all()


@app.get("/zadaci/{zadatak_id}", response_model=Zadatak)
def jedan_zadatak(zadatak_id: int, db: Session = Depends(get_db)):
    zadatak = db.get(ZadatakDB, zadatak_id)
    if zadatak is None:
        raise HTTPException(status_code=404, detail="Zadatak nije pronađen")
    return zadatak


@app.post("/zadaci", response_model=Zadatak)
def dodaj_zadatak(unos: ZadatakUnos, db: Session = Depends(get_db)):
    zadatak = ZadatakDB(**unos.model_dump())
    db.add(zadatak)
    db.commit()
    db.refresh(zadatak)
    return zadatak


@app.put("/zadaci/{zadatak_id}", response_model=Zadatak)
def izmijeni_zadatak(zadatak_id: int, unos: ZadatakUnos, db: Session = Depends(get_db)):
    zadatak = db.get(ZadatakDB, zadatak_id)
    if zadatak is None:
        raise HTTPException(status_code=404, detail="Zadatak nije pronađen")
    zadatak.naslov = unos.naslov
    zadatak.zavrsen = unos.zavrsen
    db.commit()
    db.refresh(zadatak)
    return zadatak


@app.delete("/zadaci/{zadatak_id}")
def obrisi_zadatak(zadatak_id: int, db: Session = Depends(get_db)):
    zadatak = db.get(ZadatakDB, zadatak_id)
    if zadatak is None:
        raise HTTPException(status_code=404, detail="Zadatak nije pronađen")
    db.delete(zadatak)
    db.commit()
    return {"poruka": "Obrisano"}