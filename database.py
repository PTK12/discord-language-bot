import json

__all__ = ["vocab", "vocabtitle", "vocaball"]

with open("vocab.json", "r") as f:  # Assume json is correctly formatted
    vocab: dict[str, list[list[str]]] = json.load(f)
    vocabtitle = list(vocab.keys())
    vocaball = sum(vocab.values(), [])
