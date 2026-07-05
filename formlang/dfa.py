"""AFD. À COMPLÉTER : run, accepts, minimize (Moore).  -> Jour 1 (E1.1, E1.2)."""
from __future__ import annotations
from dataclasses import dataclass, field
from collections import deque


@dataclass
class DFA:
    transitions: dict            # (state, sym) -> state
    start: str
    accept: set
    alphabet: set = field(default_factory=set)

    def __post_init__(self):
        if not self.alphabet:
            self.alphabet = {a for (_, a) in self.transitions}

    def run(self, w: str):
        state = self.start
        for a in w:
            state = self.transitions.get((state, a))
            if state is None:
                return None
        return state

    def accepts(self, w: str) -> bool:
        return self.run(w) in self.accept

    # ----- fourni : utilitaires pour la minimisation --------------------------
    def _reachable(self) -> set:
        seen, todo = {self.start}, deque([self.start])
        while todo:
            s = todo.popleft()
            for a in self.alphabet:
                t = self.transitions.get((s, a))
                if t is not None and t not in seen:
                    seen.add(t)
                    todo.append(t)
        return seen

    def _completed(self):
        SINK = "__sink__"
        trans = dict(self.transitions)
        states = self._reachable()
        need = False
        for s in states:
            for a in self.alphabet:
                if (s, a) not in trans:
                    trans[(s, a)] = SINK
                    need = True
        if need:
            states = states | {SINK}
            for a in self.alphabet:
                trans[(SINK, a)] = SINK
        return states, trans

    def minimize(self) -> "DFA":
        states, trans = self._completed()
        finals = {s for s in states if s in self.accept}
        non_finals = states - finals
        partition = [p for p in (finals, non_finals) if p]

        while True:
            block_of = {s: i for i, block in enumerate(partition) for s in block}
            new_partition = []
            for block in partition:
                groups = {}
                for s in block:
                    sig = tuple(block_of[trans[(s, a)]] for a in sorted(self.alphabet))
                    groups.setdefault(sig, set()).add(s)
                new_partition.extend(groups.values())
            if len(new_partition) == len(partition):
                partition = new_partition
                break
            partition = new_partition

        rep = {}
        for block in partition:
            r = min(block)
            for s in block:
                rep[s] = r

        new_start = rep[self.start]
        new_accept = {rep[s] for s in finals}
        new_trans = {}
        for block in partition:
            r = min(block)
            for a in self.alphabet:
                new_trans[(r, a)] = rep[trans[(r, a)]]

        return DFA(transitions=new_trans, start=new_start,
                    accept=new_accept, alphabet=set(self.alphabet))

    def num_states(self) -> int:
        st = {self.start}
        for (s, _), t in self.transitions.items():
            st.add(s)
            st.add(t)
        return len(st)
