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

def find_wanted_matches(pid: str) -> dict:
    me = get_participant(pid)
    if not me:
        return {"tienen_lo_que_busco": [], "buscan_lo_que_tengo": []}
    participants = [p for p in get_all_participants() if p["id"] != pid]
    my_wanted = me.get("figuritas_que_quiero", {})
    my_have = me.get("figuritas_repetidas", {})

    tienen = []
    buscan = []
    for other in participants:
        other_have = other.get("figuritas_repetidas", {})
        other_wanted = other.get("figuritas_que_quiero", {})

        common_have = _overlap(my_wanted, other_have)
        if common_have:
            tienen.append({
                "persona": _person_info(other),
                "figuritas": common_have,
            })

        common_want = _overlap(my_have, other_wanted)
        if common_want:
            buscan.append({
                "persona": _person_info(other),
                "figuritas": common_want,
            })

    return {"tienen_lo_que_busco": tienen, "buscan_lo_que_tengo": buscan}

def _overlap(a: dict, b: dict) -> list[dict]:
    result = []
    for num, qty_a in a.items():
        qty_b = b.get(num, 0)
        if qty_a > 0 and qty_b > 0:
            result.append({"numero": int(num), "cantidad_a": qty_a, "cantidad_b": qty_b})
    result.sort(key=lambda x: x["numero"])
    return result

def _person_info(p: dict) -> dict:
    return {
        "id": p["id"],
        "responsable": p["responsable"],
        "alumno": p["alumno"],
        "salita": p["salita"],
    }

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
        "p1": _person_info(p1),
        "p2": _person_info(p2),
        "figuritas_en_comun": common,
    }
