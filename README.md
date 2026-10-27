# TaskAPI

REST API za upravljanje zadacima s registracijom i prijavom korisnika. Napravljen u Pythonu s FastAPI-jem, SQLAlchemy-jem i SQLite bazom.

## Mogućnosti

- Registracija i prijava korisnika (JWT token)
- Lozinke se čuvaju kao argon2 hash, nikad kao običan tekst
- CRUD nad zadacima, svaki korisnik vidi i mijenja samo svoje
- Validacija podataka preko Pydantic modela
- Automatska dokumentacija na `/docs`
- Automatski testovi (pytest)

## Pokretanje

1. Kloniraj repozitorij:

   git clone https://github.com/Nocturnal-exe/taskapi.git
   cd taskapi

2. Napravi i aktiviraj virtualno okruženje (Windows):

   py -m venv venv
   venv\Scripts\activate

3. Instaliraj biblioteke:

   pip install -r requirements.txt

4. Napravi fajl `.env` s tajnim ključem:

   SECRET_KEY=neki_dugacak_nasumican_niz_znakova

   Ključ možeš generisati ovako:

   py -c "import secrets; print(secrets.token_hex(32))"

5. Pokreni server:

   uvicorn main:app --reload

6. Otvori `http://127.0.0.1:8000/docs` u browseru.

## Korištenje

1. Registruj se preko POST /registracija
2. Klikni Authorize i upiši korisničko ime i lozinku
3. Koristi endpointe za zadatke

## Endpointi

- POST /registracija: novi korisnik
- POST /login: prijava, vraća token
- GET /zadaci: lista mojih zadataka
- GET /zadaci/{id}: jedan zadatak
- POST /zadaci: novi zadatak
- PUT /zadaci/{id}: izmjena zadatka
- DELETE /zadaci/{id}: brisanje zadatka

## Docker

Projekat se može pokrenuti i u Docker kontejneru:

   docker build -t taskapi .
   docker run -p 8000:8000 -e SECRET_KEY=neki_tajni_kljuc taskapi

Tajni ključ se šalje preko `-e`, jer se `.env` namjerno ne kopira u kontejner.

## Testovi

pytest

Testovi koriste privremenu bazu u memoriji, pa ne diraju pravu bazu.

## Struktura projekta

- main.py: aplikacija i endpointi
- auth.py: tokeni i provjera prijavljenog korisnika
- database.py: veza s bazom
- models.py: tabele u bazi
- schemas.py: Pydantic modeli
- tests/: automatski testovi

## Tehnologije

Python, FastAPI, SQLAlchemy, SQLite, Pydantic, JWT, pytest