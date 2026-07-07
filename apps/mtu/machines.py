"""Opérations comme VRAIES machines de Turing. À COMPLÉTER : tables ADD, SUB.
-> Jour 4 (E4.3)."""
from formlang.turing import TuringMachine

ADD = TuringMachine(
    transitions={
        # phase 1 : parcourir n, puis fusionner le '+' en '1'
        ("q0", "1"): ("q0", "1", "R"),
        ("q0", "+"): ("q1", "1", "R"),
        # phase 2 : parcourir m jusqu'au blanc
        ("q1", "1"): ("q1", "1", "R"),
        ("q1", "_"): ("q2", "_", "L"),
        # phase 3 : retirer UN '1' (compensation du '+' converti) puis accepter
        ("q2", "1"): ("qf", "_", "S"),
    },
    start="q0", accept={"qf"},
)

# SUB : n - m (tronqué à 0). Principe (cf. jour4_calculabilite.md) : on apparie
# un '1' de m (marqué X, gauche->droite) avec un '1' de n (barré Y,
# droite->gauche, pour garder la sortie contiguë à gauche), jusqu'à épuiser m
# (nettoyage normal, réponse = 1 restants) ou épuiser n avant m (m > n : 0).
SUB = TuringMachine(
    transitions={
        # q0 : sauter n jusqu'au '-'
        ("q0", "1"): ("q0", "1", "R"),
        ("q0", "-"): ("q1", "-", "R"),

        # q1 : chercher un '1' non marqué dans m (sauter les X déjà traités)
        ("q1", "X"): ("q1", "X", "R"),
        ("q1", "1"): ("q2", "X", "L"),
        ("q1", "_"): ("q5", "_", "L"),   # m épuisé -> nettoyage normal

        # q2 : revenir au '-' (sauter les X)
        ("q2", "X"): ("q2", "X", "L"),
        ("q2", "-"): ("q3", "-", "L"),

        # q3 : chercher le '1' non barré le plus à droite de n (sauter les Y)
        ("q3", "Y"): ("q3", "Y", "L"),
        ("q3", "1"): ("q4", "Y", "R"),
        ("q3", "_"): ("q_zero", "_", "R"),  # n épuisé avant m -> m > n -> 0

        # q4 : revenir au '-' (sauter les Y) pour reprendre la recherche dans m
        ("q4", "Y"): ("q4", "Y", "R"),
        ("q4", "-"): ("q1", "-", "R"),

        # q5/q6 : nettoyage normal — effacer X, Y, '-' ; garder les '1' restants
        ("q5", "1"): ("q5", "1", "L"),
        ("q5", "-"): ("q5", "-", "L"),
        ("q5", "X"): ("q5", "X", "L"),
        ("q5", "Y"): ("q5", "Y", "L"),
        ("q5", "_"): ("q6", "_", "R"),

        ("q6", "1"): ("q6", "1", "R"),
        ("q6", "X"): ("q6", "_", "R"),
        ("q6", "Y"): ("q6", "_", "R"),
        ("q6", "-"): ("q6", "_", "R"),
        ("q6", "_"): ("qf", "_", "S"),

        # q_zero : m > n — effacer tout le ruban, résultat 0
        ("q_zero", "1"): ("q_zero", "_", "R"),
        ("q_zero", "-"): ("q_zero", "_", "R"),
        ("q_zero", "X"): ("q_zero", "_", "R"),
        ("q_zero", "Y"): ("q_zero", "_", "R"),
        ("q_zero", "_"): ("qf", "_", "S"),
    },
    start="q0", accept={"qf"},
)
