"""Calculatrice unaire. À COMPLÉTER.  -> Jour 4 (E4.3)."""
from .machines import ADD, SUB


def _ones(s: str) -> int:
    return s.count("1")


class Calculatrice:
    def addition(self, n: int, m: int) -> int:
        w = "1" * n + "+" + "1" * m
        return ADD.run(w).tape.count("1")

    def soustraction(self, n: int, m: int) -> int:   # tronquée à 0
        if m > n:
            return 0
        w = "1" * n + "-" + "1" * m
        return SUB.run(w).tape.count("1")

    def multiplication(self, n: int, m: int) -> int:
        # par composition : m additions de n (aucune nouvelle boucle de MT)
        total = 0
        for _ in range(m):
            total = self.addition(total, n)
        return total

    def division(self, n: int, m: int):              # -> (quotient, reste)
        if m == 0:
            raise ZeroDivisionError("division par zéro")
        q, r = 0, n
        while r >= m:
            r = self.soustraction(r, m)
            q += 1
        return (q, r)

    def chainer(self, v0: int, ops: list) -> int:
        v = v0
        for op, operand in ops:
            if op == "+":
                v = self.addition(v, operand)
            elif op == "-":
                v = self.soustraction(v, operand)
            elif op == "*":
                v = self.multiplication(v, operand)
            elif op == "/":
                v, _ = self.division(v, operand)
            else:
                raise ValueError(f"opérateur inconnu : {op!r}")
        return v
