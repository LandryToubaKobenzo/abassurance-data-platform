
"""Prédiction pédagogique du risque de sinistre à partir d'un modèle sauvegardé."""

from functools import lru_cache
from pathlib import Path

import joblib

RACINE_PROJET = Path(__file__).resolve().parents[2]
CHEMIN_MODELE = RACINE_PROJET / "models" / "modele_risque.joblib"


@lru_cache(maxsize=1)
def charger_modele():
    """Charge une seule fois le modèle entraîné et sauvegardé."""
    if not CHEMIN_MODELE.is_file():
        raise FileNotFoundError(
            "Modèle introuvable. Exécutez d'abord le script "
            "d'entraînement pour créer models/modele_risque.joblib."
        )

    return joblib.load(CHEMIN_MODELE)


def predire_risque(age, sinistres_precedents, anciennete_contrat):
    """Prédit le risque sans réentraîner le modèle."""

    if not 18 <= age <= 100:
        raise ValueError("L'âge doit être compris entre 18 et 100.")
    if not 0 <= sinistres_precedents <= 20:
        raise ValueError("Le nombre de sinistres doit être compris entre 0 et 20.")
    if not 0 <= anciennete_contrat <= 80:
        raise ValueError("L'ancienneté doit être comprise entre 0 et 80.")

    modele = charger_modele()
    prediction = modele.predict(
        [[age, sinistres_precedents, anciennete_contrat]]
    )[0]

    return "Élevé" if int(prediction) == 1 else "Faible"


if __name__ == "__main__":
    resultat = predire_risque(45, 2, 4)
    print(f"Risque de sinistre prédit : {resultat}")
