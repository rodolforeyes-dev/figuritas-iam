from services.persistence import get_all_participants, get_participant

def find_matches() -> list[dict]:
    participants = get_all_participants()
    matches = []
    for i, p1 in enumerate(participants):
        for p2 in participants[i + 1:]:
            common = _common_stickers(p1, p2)
            if common:
                matches.append(_build_match(p1, p2, common))
    return matches

def find_matches_for_participant(pid: str) -> list[dict]:
    me = get_participant(pid)
    if not me:
        return []
    participants = [p for p in get_all_participants() if p["id"] != pid]
    matches = []
    for other in participants:
        common = _common_stickers(me, other)
        if common:
            matches.append(_build_match(me, other, common))
    return matches

def _common_stickers(p1: dict, p2: dict) -> list[dict]:
    f1 = p1.get("figuritas_repetidas", {})
    f2 = p2.get("figuritas_repetidas", {})
    common = []
    for num, q1 in f1.items():
        q2 = f2.get(num, 0)
        if q1 > 0 and q2 > 0:
            common.append({
                "numero": int(num),
                "cantidad_p1": q1,
                "cantidad_p2": q2,
            })
    common.sort(key=lambda x: x["numero"])
    return common

def _build_match(p1: dict, p2: dict, common: list[dict]) -> dict:
    return {
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
    }
