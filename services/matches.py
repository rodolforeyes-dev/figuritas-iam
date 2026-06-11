from services.persistence import get_all_participants

def find_matches() -> list[dict]:
    participants = get_all_participants()
    matches = []
    for i, p1 in enumerate(participants):
        for p2 in participants[i + 1:]:
            common = []
            f1 = p1.get("figuritas_repetidas", {})
            f2 = p2.get("figuritas_repetidas", {})
            all_nums = set(f1.keys()) | set(f2.keys())
            for num in all_nums:
                q1 = f1.get(num, 0)
                q2 = f2.get(num, 0)
                if q1 > 0 and q2 > 0:
                    common.append({
                        "numero": int(num),
                        "cantidad_p1": q1,
                        "cantidad_p2": q2,
                    })
            if common:
                matches.append({
                    "p1": {
                        "id": p1["id"],
                        "responsable": p1["responsable"],
                        "alumno": p1["alumno"],
                        "salita": p1["salita"],
                    },
                    "p2": {
                        "id": p2["id"],
                        "responsable": p2["responsable"],
                        "alumno": p2["alumno"],
                        "salita": p2["salita"],
                    },
                    "figuritas_en_comun": common,
                })
    return matches
