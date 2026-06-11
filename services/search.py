from services.persistence import get_all_participants

def search_sticker(num: int) -> list[dict]:
    participants = get_all_participants()
    key = str(num)
    results = []
    for p in participants:
        figuritas = p.get("figuritas_repetidas", {})
        if key in figuritas and figuritas[key] > 0:
            results.append({
                "id": p["id"],
                "responsable": p["responsable"],
                "alumno": p["alumno"],
                "salita": p["salita"],
                "telefono": p["telefono"],
                "cantidad": figuritas[key],
                "fecha_actualizacion": p.get("fecha_actualizacion", ""),
            })
    results.sort(key=lambda r: r["fecha_actualizacion"], reverse=True)
    return results

def search_sticker_detail(num: int) -> dict:
    participants = get_all_participants()
    key = str(num)
    owners = []
    total_units = 0
    for p in participants:
        figuritas = p.get("figuritas_repetidas", {})
        if key in figuritas and figuritas[key] > 0:
            cantidad = figuritas[key]
            total_units += cantidad
            owners.append({
                "responsable": p["responsable"],
                "alumno": p["alumno"],
                "salita": p["salita"],
                "telefono": p["telefono"],
                "cantidad": cantidad,
            })
    owners.sort(key=lambda o: o["responsable"])
    return {
        "numero": num,
        "total_unidades": total_units,
        "total_participantes": len(owners),
        "owners": owners,
    }
