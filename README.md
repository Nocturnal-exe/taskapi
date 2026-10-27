\# TaskAPI



Jednostavan REST API za upravljanje zadacima, napravljen u Pythonu s FastAPI-jem i SQLite bazom.



\## Mogućnosti



\- Dodavanje, pregled, izmjena i brisanje zadataka (CRUD)

\- Validacija podataka preko Pydantic modela

\- Trajno čuvanje u SQLite bazi preko SQLAlchemy-ja

\- Automatska dokumentacija na `/docs`



\## Pokretanje



1\. Kloniraj repozitorij:



&#x20;  git clone https://github.com/Nocturnal-exe/taskapi.git

&#x20;  cd taskapi



2\. Napravi i aktiviraj virtualno okruženje (Windows):



&#x20;  py -m venv venv

&#x20;  venv\\Scripts\\activate



3\. Instaliraj biblioteke:



&#x20;  pip install -r requirements.txt



4\. Pokreni server:



&#x20;  uvicorn main:app --reload



5\. Otvori `http://127.0.0.1:8000/docs` u browseru.



\## Endpointi



\- GET /zadaci: lista svih zadataka

\- GET /zadaci/{id}: jedan zadatak

\- POST /zadaci: novi zadatak

\- PUT /zadaci/{id}: izmjena zadatka

\- DELETE /zadaci/{id}: brisanje zadatka



\## Tehnologije



Python, FastAPI, SQLAlchemy, SQLite, Pydantic

