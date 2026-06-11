from services.persistence import get_all_participants

def get_stats() -> dict:
    participants = get_all_participants()
    total_participants = len(participants)

    por_salita = {}
    for p in participants:
        s = p.get("salita", "Sin salita")
        por_salita[s] = por_salita.get(s, 0) + 1

    figuritas_count = {}
    figuritas_owners = {}
    total_stickers = 0
    for p in participants:
        for num, qty in p.get("figuritas_repetidas", {}).items():
            figuritas_count[num] = figuritas_count.get(num, 0) + qty
            figuritas_owners[num] = figuritas_owners.get(num, 0) + 1
            total_stickers += qty

    sorted_by_qty = sorted(figuritas_count.items(), key=lambda x: -x[1])
    most_repeated = [
        {"numero": int(n), "total": v, "owners": figuritas_owners.get(n, 0)}
        for n, v in sorted_by_qty[:10]
    ]

    sorted_by_qty_asc = sorted(figuritas_count.items(), key=lambda x: x[1])
    least_registered = [
        {"numero": int(n), "total": v, "owners": figuritas_owners.get(n, 0)}
        for n, v in sorted_by_qty_asc[:10]
    ]

    all_numbers = set(str(i) for i in range(1, 205))
    registered = set(figuritas_count.keys())
    not_registered = sorted(int(n) for n in all_numbers - registered)

    sorted_participants = sorted(
        participants, key=lambda p: p.get("fecha_actualizacion", ""), reverse=True
    )
    last_updates = [
        {
            "responsable": p["responsable"],
            "alumno": p["alumno"],
            "fecha": p.get("fecha_actualizacion", ""),
        }
        for p in sorted_participants[:10]
    ]

    return {
        "total_participantes": total_participants,
        "total_figuritas": total_stickers,
        "por_salita": dict(sorted(por_salita.items())),
        "mas_repetidas": most_repeated,
        "menos_registradas": least_registered,
        "sin_registros": not_registered,
        "ultimas_actualizaciones": last_updates,
        "figuritas_con_datos": len(figuritas_count),
        "figuritas_sin_datos": len(not_registered),
    }
