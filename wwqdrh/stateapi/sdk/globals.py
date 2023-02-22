import hashlib


def sha256(word: str) -> str:
    return hashlib.sha256(word.encode("utf-8")).hexdigest()
