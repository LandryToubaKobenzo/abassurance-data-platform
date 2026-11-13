
"""Pipeline de normalisation des clients AbAssurance et AssurePlus."""

import json
from pathlib import Path

from abassurance.normalisation import (
    normaliser_client_ab,
    normaliser_client_ap,

from abassurance.rapprochement import detecter_correspondances
)


def unifier_clients(clients_ab, clients_ap):
    """Normalise les sources en conservant leurs identifiants historiques."""
    resultat = []

    def analyser_clients(clients_ab, clients_ap):
    """Normalise les clients et détecte les correspondances candidates."""
    clients = unifier_clients(clients_ab, clients_ap)
    correspondances = detecter_correspondances(clients)

    return {
        "clients": clients,
        "correspondances_candidates": correspondances,
    }
    
    for client in clients_ab:
        resultat.append(normaliser_client_ab(client))

    for client in clients_ap:
        resultat.append(normaliser_client_ap(client))

    return resultat


def executer_pipeline(fichier_ab, fichier_ap, fichier_sortie):
    """Lit deux fichiers JSON et écrit les clients normalisés."""
    with open(fichier_ab, encoding="utf-8") as fichier:
        clients_ab = json.load(fichier)

    with open(fichier_ap, encoding="utf-8") as fichier:
        clients_ap = json.load(fichier)

    if not isinstance(clients_ab, list) or not isinstance(clients_ap, list):
        raise TypeError("Les fichiers sources doivent contenir des listes JSON.")

    resultat = unifier_clients(clients_ab, clients_ap)

    sortie = Path(fichier_sortie)
    sortie.parent.mkdir(parents=True, exist_ok=True)

    with sortie.open("w", encoding="utf-8") as fichier:
        json.dump(resultat, fichier, ensure_ascii=False, indent=2)

    return len(resultat)
