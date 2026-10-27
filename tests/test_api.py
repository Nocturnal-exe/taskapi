from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from database import Base, get_db

# Privremena baza u memoriji, ne dira pravu zadaci.db
engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestSession = sessionmaker(bind=engine, autoflush=False)


def get_test_db():
    db = TestSession()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = get_test_db
client = TestClient(app)


def setup_function():
    # Prije svakog testa napravi praznu bazu
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def prijavi_korisnika(ime="hamza", lozinka="tajna123"):
    client.post("/registracija", json={"korisnicko_ime": ime, "lozinka": lozinka})
    odgovor = client.post("/login", data={"username": ime, "password": lozinka})
    token = odgovor.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_registracija():
    odgovor = client.post("/registracija", json={"korisnicko_ime": "hamza", "lozinka": "tajna123"})
    assert odgovor.status_code == 200
    assert odgovor.json()["korisnicko_ime"] == "hamza"
    assert "lozinka" not in odgovor.json()


def test_zauzeto_korisnicko_ime():
    client.post("/registracija", json={"korisnicko_ime": "hamza", "lozinka": "tajna123"})
    odgovor = client.post("/registracija", json={"korisnicko_ime": "hamza", "lozinka": "druga"})
    assert odgovor.status_code == 400


def test_login_pogresna_lozinka():
    client.post("/registracija", json={"korisnicko_ime": "hamza", "lozinka": "tajna123"})
    odgovor = client.post("/login", data={"username": "hamza", "password": "pogresna"})
    assert odgovor.status_code == 401


def test_zadaci_traze_prijavu():
    odgovor = client.get("/zadaci")
    assert odgovor.status_code == 401


def test_dodaj_i_dohvati_zadatak():
    zaglavlje = prijavi_korisnika()
    client.post("/zadaci", json={"naslov": "Test zadatak"}, headers=zaglavlje)
    odgovor = client.get("/zadaci", headers=zaglavlje)
    assert odgovor.status_code == 200
    assert len(odgovor.json()) == 1
    assert odgovor.json()[0]["naslov"] == "Test zadatak"


def test_korisnik_ne_vidi_tudje_zadatke():
    hamza = prijavi_korisnika("hamza", "tajna123")
    ana = prijavi_korisnika("ana", "tajna456")
    client.post("/zadaci", json={"naslov": "Hamzin zadatak"}, headers=hamza)
    odgovor = client.get("/zadaci", headers=ana)
    assert odgovor.json() == []