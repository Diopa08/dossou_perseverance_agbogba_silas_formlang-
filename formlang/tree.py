"""Automate d'arbres ascendant (BUTA) générique. À COMPLÉTER : run, accepts,
product.  -> Jour 3 (E3.1, E3.4)."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Hashable


@dataclass(frozen=True)
class Term:
    symbol: str
    children: tuple["Term", ...] = ()
    label: Optional[str] = None


class _Reject:
    __slots__ = ()
    def __repr__(self):
        return "REJECT"


REJECT = _Reject()


class TreeAutomaton:
    def __init__(self, final_states):
        self.delta: dict[tuple[str, tuple], Hashable] = {}
        self.final: set = set(final_states)

    def add_rule(self, symbol: str, child_states, result) -> None:
        # FOURNI
        self.delta[(symbol, tuple(child_states))] = result

    def run(self, t: "Term"):
        child_states = []
        for c in t.children:
            s = self.run(c)
            if s is REJECT:
                return REJECT
            child_states.append(s)
        key = (t.symbol, tuple(child_states))
        if key not in self.delta:
            return REJECT
        return self.delta[key]

    def accepts(self, t: "Term") -> bool:
        return self.run(t) in self.final


def product(a1: "TreeAutomaton", a2: "TreeAutomaton") -> "TreeAutomaton":
    finals = {(f1, f2) for f1 in a1.final for f2 in a2.final}
    A = TreeAutomaton(final_states=finals)
    symbols = {sym for (sym, _) in a1.delta} & {sym for (sym, _) in a2.delta}
    for sym in symbols:
        arities1 = {states for (s, states) in a1.delta if s == sym}
        arities2 = {states for (s, states) in a2.delta if s == sym}
        for states1 in arities1:
            for states2 in arities2:
                if len(states1) != len(states2):
                    continue
                pair_states = tuple(zip(states1, states2))
                r1 = a1.delta[(sym, states1)]
                r2 = a2.delta[(sym, states2)]
                A.add_rule(sym, pair_states, (r1, r2))
    return A
