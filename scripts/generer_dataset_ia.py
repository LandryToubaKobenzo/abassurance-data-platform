"""Génère un dataset IA fictif et reproductible pour la démonstration."""

import csv
import random
from pathlib import Path


def generer_dataset(nombre=300, graine=42):
    """Crée des exemples synthétiques sans utiliser de données réelles."""
    generateur = random.Random(graine)
    lignes = []

    for identifiant in range(1, nombre + 1):
        age = generateur.randint(18, 85)
        sinistres = generateur.choices(
            [0, 1, 2, 3, 4, 5],
            weights=[45, 25, 15, 8, 5, 2],
        )[0]
        anciennete = generateur.randint(0, min(age - 18, 35))

        score = (
            2 * sinistres
            + (1 if age >= 60 else 0)
            + (1 if anciennete < 2 else 0)
        )

        risque_eleve = int(score >= 4)

        lignes.append(
            {
                "id_observation": identifiant,
                "age": age,
                "sinistres_precedents": sinistres,
                "anciennete_contrat": anciennete,
                "risque_eleve": risque_eleve,
            }
        )

    return lignes


def main():
    destination = (
        Path(__file__).resolve().parents[1]
        / "data"
        / "processed"
        / "risques_synthetiques.csv"
    )
    destination.parent.mkdir(parents=True, exist_ok=True)

    lignes = generer_dataset()

    with destination.open("w", newline="", encoding="utf-8") as fichier:
        redacteur = csv.DictWriter(
            fichier,
            fieldnames=[
                "id_observation",
                "age",
                "sinistres_precedents",
                "anciennete_contrat",
                "risque_eleve",
            ],
        )
        redacteur.writeheader()
        redacteur.writerows(lignes)

    print(f"Dataset généré : {len(lignes)} observations")
    print(f"Fichier : {destination}")


if __name__ == "__main__":
    main()
