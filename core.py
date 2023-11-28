from random import randrange, randint, choice
from database import *

__all__ = ["mcq", "is_correct"]

ACCENTS = {
    224: 97,
    225: 97,
    226: 97,
    227: 97,
    228: 97,
    229: 97,
    232: 101,
    233: 101,
    234: 101,
    235: 101,
    236: 105,
    237: 105,
    238: 105,
    239: 105,
    242: 111,
    243: 111,
    244: 111,
    245: 111,
    246: 111,
    249: 117,
    250: 117,
    251: 117,
    252: 117,
    241: 110,
}


def r() -> int:
    '''Randomly generate numbers based on exponential distribution.'''
    return (65 - randrange(1 << 64).bit_length()) * (-1) ** randint(1, 2)


def retrieve(name: str | None = None) -> list[list[str]]:
    if name is None:
        return vocaball
    elif name.isdigit():
        return vocab[vocabtitle[int(name)]]
    else:
        return vocab[name]


def mcq(n: int = 4, name: str | None = None, reverse: bool = False):
    '''multiple choice question'''
    data = retrieve(name)
    mid = randint(0, len(data) - 1)
    picks: set[int] = set()
    while len(picks) < n:
        mid = (mid + r()) % len(data)
        picks.add(mid)

    pairs = [data[i] for i in picks]
    if reverse:
        pairs = [i[::-1] for i in pairs]

    correct = choice(pairs)
    public = (correct[1], [i[0] for i in pairs])
    private = correct[0]
    return public, private


def clean(inp: str) -> str:
    return "".join(i.lower() for i in inp if i.isalpha())


def is_correct(inp: str, correct: str) -> bool:
    inp = clean(inp)
    correct = clean(correct)

    if inp == correct: return True
    return inp == correct.translate(ACCENTS)
