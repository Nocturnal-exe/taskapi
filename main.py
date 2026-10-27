from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from database import engine, Base, get_db
from models import ZadatakDB
from schemas import Zadatak, ZadatakUnos

from pwdlib import PasswordHash
from models import KorisnikDB
from schemas import Korisnik, KorisnikUnos

from fastapi.security import OAuth2PasswordRequestForm
from auth import napravi_token

Base.metadata.create_all(bind=engine)

app = FastAPI()

password_hash = PasswordHash.recommended()

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

@app.post("/registracija", response_model=Korisnik)
def registracija(unos: KorisnikUnos, db: Session = Depends(get_db)):
    postoji = db.query(KorisnikDB).filter(KorisnikDB.korisnicko_ime == unos.korisnicko_ime).first()
    if postoji:
        raise HTTPException(status_code=400, detail="Korisničko ime je zauzeto")
    korisnik = KorisnikDB(
        korisnicko_ime=unos.korisnicko_ime,
        hash_lozinke=password_hash.hash(unos.lozinka),
    )
    db.add(korisnik)
    db.commit()
    db.refresh(korisnik)
    return korisnik

@app.post("/login")
def login(forma: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    korisnik = db.query(KorisnikDB).filter(KorisnikDB.korisnicko_ime == forma.username).first()
    if korisnik is None or not password_hash.verify(forma.password, korisnik.hash_lozinke):
        raise HTTPException(status_code=401, detail="Pogrešno korisničko ime ili lozinka")
    token = napravi_token(korisnik.korisnicko_ime)
    return {"access_token": token, "token_type": "bearer"} 