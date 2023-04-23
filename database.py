import json

__all__ = ["vocab", "vocabtitle", "vocaball"]

with open("vocab.json", "r") as f:
    vocab: dict = json.load(f)
    vocabtitle = list(vocab.keys())
    vocaball = sum(vocab.values(), [])
