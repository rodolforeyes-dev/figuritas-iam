import json
from pathlib import Path

DATA_DIR = Path("data")
SALITAS_FILE = DATA_DIR / "salitas.json"
DEFAULT_SALITAS = [
    "Sala Blanca",
    "Sala Verde",
    "Sala Roja",
]

def load_salitas() -> list[str]:
    DATA_DIR.mkdir(exist_ok=True)
    if not SALITAS_FILE.exists():
        save_salitas(DEFAULT_SALITAS)
        return DEFAULT_SALITAS
    with open(SALITAS_FILE) as f:
        return json.load(f)

def save_salitas(salitas: list[str]):
    DATA_DIR.mkdir(exist_ok=True)
    with open(SALITAS_FILE, "w") as f:
        json.dump(salitas, f, indent=2, ensure_ascii=False)
