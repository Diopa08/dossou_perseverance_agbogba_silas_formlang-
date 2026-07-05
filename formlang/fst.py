"""Transducteur fini séquentiel. À COMPLÉTER : transduce.  -> Jour 1 (E1.4)."""
from __future__ import annotations
from dataclasses import dataclass


@dataclass
class SequentialFST:
    transitions: dict            # (state, in_sym) -> (next_state, out_sym)
    start: str
    finals: set
    identity_on_missing: bool = False

    def transduce(self, w: str) -> str:
        state = self.start
        out = []
        for a in w:
            if (state, a) in self.transitions:
                state, b = self.transitions[(state, a)]
                out.append(b)
            elif self.identity_on_missing:
                out.append(a)
            else:
                return None
        return "".join(out)


def compose(t1: "SequentialFST", t2: "SequentialFST") -> "SequentialFST":
    # FOURNI : t(w) = t2(t1(w)). États = paires.
    trans = {}
    for (s1, a), (s1n, b) in t1.transitions.items():
        for (s2, x), (s2n, c) in t2.transitions.items():
            if x == b:
                trans[((s1, s2), a)] = ((s1n, s2n), c)
    finals = {(f1, f2) for f1 in t1.finals for f2 in t2.finals}
    return SequentialFST(trans, (t1.start, t2.start), finals)


def leet_fst() -> "SequentialFST":
    trans = {
        ("q0", "4"): ("q0", "a"),
        ("q0", "0"): ("q0", "o"),
        ("q0", "3"): ("q0", "e"),
        ("q0", "1"): ("q0", "i"),
        ("q0", "5"): ("q0", "s"),
    }
    return SequentialFST(trans, "q0", {"q0"}, identity_on_missing=True)


def reverse_twoway(w: str) -> str:
    # FOURNI : renversement (modélise une transduction bidirectionnelle).
    return w[::-1]
