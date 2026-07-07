"""Machine universelle. À COMPLÉTER : encode/decode et run.  -> Jour 4 (E4.2)."""
from __future__ import annotations
import json
from .turing import TuringMachine, TMResult


def encode(machine: "TuringMachine") -> str:
    d = {
        "transitions": {
            f"{q}|{a}": [nq, b, mv]
            for (q, a), (nq, b, mv) in sorted(machine.transitions.items())
        },
        "start": machine.start,
        "accept": sorted(machine.accept),
        "blank": machine.blank,
        "reject": sorted(machine.reject),
    }
    return json.dumps(d, sort_keys=True)


def decode(desc: str) -> "TuringMachine":
    d = json.loads(desc)
    transitions = {}
    for key, (nq, b, mv) in d["transitions"].items():
        q, a = key.split("|", 1)
        transitions[(q, a)] = (nq, b, mv)
    return TuringMachine(
        transitions=transitions,
        start=d["start"],
        accept=set(d["accept"]),
        blank=d["blank"],
        reject=set(d["reject"]),
    )


class UniversalTM:
    def run(self, encoded_machine: str, word: str, **kw) -> "TMResult":
        machine = decode(encoded_machine)
        return machine.run(word, **kw)
