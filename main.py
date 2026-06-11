import re
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from config import load_salitas
from services.persistence import (
    create_participant,
    update_participant,
    get_participant,
    get_all_participants,
    lookup_participants,
    export_all,
    import_all,
)
from services.search import search_sticker, search_sticker_detail
from services.matches import find_matches, find_matches_for_participant, find_wanted_matches
from services.stats import get_stats
from services.metrics import get_metrics

app = FastAPI(title="Intercambio figuritas IAM")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class StickersUpdate(BaseModel):
    figuritas_repetidas: dict[str, int]


def normalize_phone(phone: str) -> str:
    digits = re.sub(r"\D", "", phone)
    if not digits.startswith("549"):
        digits = "549" + digits
    return digits


# ─── Pages ─────────────────────────────────────────────


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request, "index.html")


@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    salitas = load_salitas()
    return templates.TemplateResponse(request, "register.html", {"salitas": salitas})


@app.get("/edit/{pid}", response_class=HTMLResponse)
async def edit_page(request: Request, pid: str):
    participant = get_participant(pid)
    if not participant:
        return HTMLResponse("Participante no encontrado", status_code=404)
    return templates.TemplateResponse(
        request, "edit.html", {"participant": participant}
    )


@app.get("/search", response_class=HTMLResponse)
async def search_page(request: Request):
    return templates.TemplateResponse(request, "search.html")


@app.get("/sticker/{num}", response_class=HTMLResponse)
async def sticker_detail_page(request: Request, num: int):
    if num < 1 or num > 204:
        return HTMLResponse("Número inválido (1-204)", status_code=400)
    data = search_sticker_detail(num)
    for o in data["owners"]:
        o["wa_link"] = f"https://wa.me/{normalize_phone(o['telefono'])}"
    return templates.TemplateResponse(request, "sticker_detail.html", {"data": data})


@app.get("/matches", response_class=HTMLResponse)
async def matches_page(request: Request):
    return templates.TemplateResponse(request, "matches.html")


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    return templates.TemplateResponse(request, "dashboard.html")


# ─── API ───────────────────────────────────────────────


@app.post("/api/participants")
async def api_create_participant(
    responsable: str = Form(...),
    telefono: str = Form(...),
    alumno: str = Form(...),
    salita: str = Form(...),
):
    if not all([responsable.strip(), telefono.strip(), alumno.strip(), salita.strip()]):
        raise HTTPException(400, "Todos los campos son obligatorios")

    if salita not in load_salitas():
        raise HTTPException(400, "Salita no válida")

    participant = create_participant(
        responsable=responsable.strip(),
        telefono=telefono.strip(),
        alumno=alumno.strip(),
        salita=salita,
    )
    return participant


@app.get("/api/participant/{pid}")
async def api_get_participant(pid: str):
    p = get_participant(pid)
    if not p:
        raise HTTPException(404, "No encontrado")
    return p


@app.post("/api/participants/{pid}/stickers")
async def api_update_stickers(pid: str, data: StickersUpdate):
    p = update_participant(pid, figuritas_repetidas=data.figuritas_repetidas)
    if not p:
        raise HTTPException(404, "No encontrado")
    return p

@app.post("/api/participants/{pid}/wanted")
async def api_update_wanted(pid: str, data: StickersUpdate):
    p = update_participant(pid, figuritas_que_quiero=data.figuritas_repetidas)
    if not p:
        raise HTTPException(404, "No encontrado")
    return p


@app.post("/api/participants/lookup")
async def api_lookup(query: str = Form(...)):
    results = lookup_participants(query.strip())
    return results


@app.get("/api/search/{num}")
async def api_search_sticker(num: int):
    if num < 1 or num > 204:
        raise HTTPException(400, "Número de figurita inválido (1-204)")
    results = search_sticker(num)
    for r in results:
        r["wa_link"] = f"https://wa.me/{normalize_phone(r['telefono'])}"
    return results


@app.get("/api/matches")
async def api_matches():
    return find_matches()

@app.get("/api/matches/{pid}")
async def api_matches_for_participant(pid: str):
    return find_matches_for_participant(pid)

@app.get("/api/matches/wanted/{pid}")
async def api_wanted_matches(pid: str):
    return find_wanted_matches(pid)


@app.get("/api/metrics")
async def api_metrics():
    return get_metrics()

@app.get("/api/export")
async def api_export():
    return export_all()

@app.post("/api/import")
async def api_import(data: dict):
    count = import_all(data)
    return {"importados": count}

@app.get("/api/dashboard")
async def api_dashboard():
    return get_stats()


if __name__ == "__main__":
    import os
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
