"""Machine de Turing déterministe (ruban dict bi-infini). À COMPLÉTER : run.
-> Jour 4 (E4.1)."""
from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class TMResult:
    accepted: bool
    tape: str
    steps: int
    trace: list = field(default_factory=list)


@dataclass
class TuringMachine:
    transitions: dict           # (q, a) -> (q', b, d in {'L','R','S'})
    start: str
    accept: set
    blank: str = "_"
    reject: set = field(default_factory=set)

    # ----- fourni -------------------------------------------------------------
    def _read(self, tape: dict) -> str:
        if not tape:
            return ""
        lo, hi = min(tape), max(tape)
        return "".join(tape.get(i, self.blank) for i in range(lo, hi + 1)).strip(self.blank)

    def _window(self, tape: dict) -> str:
        if not tape:
            return ""
        lo, hi = min(tape), max(tape)
        return "".join(tape.get(i, self.blank) for i in range(lo, hi + 1))

    # ----- à compléter --------------------------------------------------------
    def run(self, word: str, max_steps: int = 1_000_000, trace: bool = False) -> "TMResult":
        tape = {i: c for i, c in enumerate(word)}
        pos = 0
        state = self.start
        trc = []
        steps = 0
        while True:
            if trace:
                trc.append((steps, state, self._window(tape), pos))
            if state in self.accept or state in self.reject:
                break
            a = tape.get(pos, self.blank)
            key = (state, a)
            if key not in self.transitions:
                break  # arrêt : pas de transition (mot rejeté si état non final)
            new_state, b, d = self.transitions[key]
            tape[pos] = b
            if d == "L":
                pos -= 1
            elif d == "R":
                pos += 1
            state = new_state
            steps += 1
            if steps > max_steps:
                raise RuntimeError(
                    f"TuringMachine.run : max_steps={max_steps} dépassé (boucle infinie ?)"
                )
        return TMResult(accepted=state in self.accept, tape=self._read(tape),
                         steps=steps, trace=trc)
