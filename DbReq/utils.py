import logging
from copy import deepcopy
from typing import List, Dict, Any


__all__ = []

def parse_hafas_lid(lid: str) -> Dict[str, Any]:
    s = lid.strip().strip('"').strip("'")
    # Normalize a few known oddities
    s = s.replace("\u00d7", "x")  # × → x
    # Split into K=V segments bounded by '@'
    parts = [p for p in s.split('@') if p]
    kv: Dict[str, str] = {}
    for p in parts:
        if '=' in p:
            k, v = p.split('=', 1)
            kv[k] = v

    out: Dict[str, Any] = {"raw": lid}

    # Common fields
    if "A" in kv:
        try:
            out["A"] = int(kv["A"])
        except ValueError:
            out["A"] = kv["A"]

    out["name"] = kv.get("O")  # stop/address name

    # Coordinates (microdegrees → degrees)
    def _as_int(x: str) -> int:
        return int(float(x))  # tolerate “-122.0” variants

    if "X" in kv:
        out["X"] = _as_int(kv["X"])
    if "Y" in kv:
        out["Y"] = _as_int(kv["Y"])
    if "X" in out and "Y" in out:
        out["lon"] = out["X"] / 1e6
        out["lat"] = out["Y"] / 1e6

    # External stop id (EVA/IBNR or backend extId)
    if "L" in kv:
        try:
            out["extId"] = int(kv["L"].lstrip("0") or "0")
        except ValueError:
            out["extId"] = kv["L"]

    # Timestamp-like field (often Unix seconds)
    if "p" in kv:
        try:
            out["timestamp"] = int(kv["p"])
        except ValueError:
            out["timestamp"] = kv["p"]

    return out


def get_from_list(buckets: List[Dict], mappings: Dict[str, list], log_prefix="parse_data_fields",soft_errors = True) -> List[Dict[str, Any]]:
    final_list = []
    mappings = deepcopy(mappings)

    for bucket in buckets:
        dict_temp = {}
        for key,mapping in mappings.items():
            bucket_sub = bucket
            mapping_ind = deepcopy(mapping)
            
            while mapping_ind:
                map = mapping_ind.pop(0)
                if map not in bucket_sub:
                    bucket_sub = None
                    break
                bucket_sub = bucket_sub[map]
            
            dict_temp[key] = bucket_sub

        final_list.append(dict_temp)

    return final_list
            
