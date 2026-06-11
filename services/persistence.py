import json
import uuid
import threading
from datetime import datetime
from pathlib import Path

DATA_DIR = Path("data")
PARTICIPANTS_FILE = DATA_DIR / "participants.json"
_lock = threading.Lock()

def _ensure_dir():
    DATA_DIR.mkdir(exist_ok=True)

def _load_all() -> dict:
    _ensure_dir()
    if not PARTICIPANTS_FILE.exists():
        return {}
    with open(PARTICIPANTS_FILE) as f:
        return json.load(f)

def _save_all(data: dict):
    _ensure_dir()
    with _lock:
        tmp = PARTICIPANTS_FILE.with_suffix(".tmp")
        with open(tmp, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        tmp.rename(PARTICIPANTS_FILE)

def create_participant(responsable: str, telefono: str, alumno: str, salita: str) -> dict:
    data = _load_all()
    pid = uuid.uuid4().hex[:8]
    participant = {
        "id": pid,
        "responsable": responsable,
        "telefono": telefono,
        "alumno": alumno,
        "salita": salita,
        "figuritas_repetidas": {},
        "fecha_actualizacion": datetime.now().isoformat(timespec="seconds"),
    }
    data[pid] = participant
    _save_all(data)
    return participant

def update_participant(pid: str, **kwargs) -> dict | None:
    data = _load_all()
    if pid not in data:
        return None
    data[pid].update(kwargs)
    data[pid]["fecha_actualizacion"] = datetime.now().isoformat(timespec="seconds")
    _save_all(data)
    return data[pid]

def get_participant(pid: str) -> dict | None:
    data = _load_all()
    return data.get(pid)

def get_all_participants() -> list[dict]:
    data = _load_all()
    return list(data.values())

def lookup_participants(query: str) -> list[dict]:
    data = _load_all()
    q = query.lower().strip()
    results = []
    for p in data.values():
        if q in p["responsable"].lower() or q in p["alumno"].lower():
            results.append(p)
    return results
