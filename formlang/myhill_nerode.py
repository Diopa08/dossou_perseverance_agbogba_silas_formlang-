"""Classes de Myhill-Nerode (approx. sur suffixes témoins). À COMPLÉTER.
-> Jour 5 (E5.3)."""
from __future__ import annotations


def nerode_classes(accepts, words, suffixes):
    classes = {}
    for w in words:
        sig = tuple(accepts(w + s) for s in suffixes)
        classes.setdefault(sig, []).append(w)
    return list(classes.values())


def equivalent(u, v, accepts, suffixes) -> bool:
    # FOURNI
    return all(accepts(u + s) == accepts(v + s) for s in suffixes)
