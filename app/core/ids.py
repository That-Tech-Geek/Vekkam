from hashlib import sha256


def stable_id(kind: str, *parts: str) -> str:
    raw = "::".join((kind, *parts))
    return f"{kind}_{sha256(raw.encode('utf-8')).hexdigest()[:16]}"
