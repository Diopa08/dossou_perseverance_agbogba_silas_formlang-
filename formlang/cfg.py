"""Grammaire hors-contexte : génération bornée. À COMPLÉTER.  -> Jour 2 (E2.2)."""
from __future__ import annotations
from dataclasses import dataclass
from collections import deque


@dataclass
class CFG:
    rules: dict
    start: str
    nonterminals: set

    def generate(self, max_len: int) -> set:
        # Piège de l'énoncé : "S S S…" a 0 terminal et n'est jamais élagué par
        # la seule borne sur les terminaux -> on borne AUSSI le nombre de
        # symboles (donc de non-terminaux) de la forme sententielle.
        max_symbols = max_len + len(self.nonterminals) + 2
        results = set()
        visited = set()
        queue = deque([(self.start,)])

        while queue:
            form = queue.popleft()
            if form in visited:
                continue
            visited.add(form)

            has_nt = any(s in self.nonterminals for s in form)
            if not has_nt:
                word = "".join(form)
                if len(word) <= max_len:
                    results.add(word)
                continue

            if len(form) > max_symbols:
                continue  # forme trop longue : on élague

            # dérivation gauche : on développe le premier non-terminal
            idx = next(i for i, s in enumerate(form) if s in self.nonterminals)
            nt = form[idx]
            for rule in self.rules.get(nt, []):
                new_form = form[:idx] + tuple(rule) + form[idx + 1:]
                if new_form not in visited:
                    queue.append(new_form)

        return results


def balanced_cfg() -> "CFG":
    # FOURNI : S -> S S | [ S ] | ( S ) | a | o | r | eps
    return CFG(
        rules={"S": [("S", "S"), ("[", "S", "]"), ("(", "S", ")"),
                     ("a",), ("o",), ("r",), ()]},
        start="S", nonterminals={"S"},
    )
