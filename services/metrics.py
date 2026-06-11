from services.persistence import get_all_participants
from services.matches import find_matches

def get_metrics() -> dict:
    participants = get_all_participants()
    total_usuarios = len(participants)

    total_figuritas = 0
    for p in participants:
        for qty in p.get("figuritas_repetidas", {}).values():
            total_figuritas += qty

    matches = find_matches()
    intercambiadas = set()
    for m in matches:
        for f in m["figuritas_en_comun"]:
            intercambiadas.add(f["numero"])

    return {
        "total_usuarios_registrados": total_usuarios,
        "total_figuritas_registradas": total_figuritas,
        "total_figuritas_intercambiadas": len(intercambiadas),
        "total_intercambios_posibles": len(matches),
    }
