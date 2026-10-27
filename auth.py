import os
from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
TRAJANJE_TOKENA_MIN = 30


def napravi_token(korisnicko_ime: str) -> str:
    istice = datetime.now(timezone.utc) + timedelta(minutes=TRAJANJE_TOKENA_MIN)
    podaci = {"sub": korisnicko_ime, "exp": istice}
    return jwt.encode(podaci, SECRET_KEY, algorithm=ALGORITHM)