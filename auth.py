import os
from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from database import get_db
from models import KorisnikDB

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
TRAJANJE_TOKENA_MIN = 30

oauth2_shema = OAuth2PasswordBearer(tokenUrl="login")


def napravi_token(korisnicko_ime: str) -> str:
    istice = datetime.now(timezone.utc) + timedelta(minutes=TRAJANJE_TOKENA_MIN)
    podaci = {"sub": korisnicko_ime, "exp": istice}
    return jwt.encode(podaci, SECRET_KEY, algorithm=ALGORITHM)


def trenutni_korisnik(token: str = Depends(oauth2_shema), db: Session = Depends(get_db)):
    greska = HTTPException(status_code=401, detail="Neispravan ili istekao token")
    try:
        podaci = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        korisnicko_ime = podaci.get("sub")
    except jwt.PyJWTError:
        raise greska
    if korisnicko_ime is None:
        raise greska
    korisnik = db.query(KorisnikDB).filter(KorisnikDB.korisnicko_ime == korisnicko_ime).first()
    if korisnik is None:
        raise greska
    return korisnik