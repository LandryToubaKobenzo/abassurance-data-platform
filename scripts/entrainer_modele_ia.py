
"""Entraîne et évalue un modèle IA sur des données synthétiques."""

import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

RACINE = Path(__file__).resolve().parents[1]
DATASET = RACINE / "data" / "processed" / "risques_synthetiques.csv"
MODELE = RACINE / "models" / "modele_risque.joblib"
METRIQUES = RACINE / "models" / "metriques_modele.json"

VARIABLES = [
    "age",
    "sinistres_precedents",
    "anciennete_contrat",
]
CIBLE = "risque_eleve"


def entrainer():
    """Entraîne, évalue et sauvegarde le modèle."""
    if not DATASET.is_file():
        raise FileNotFoundError(
            f"Dataset absent : {DATASET}. "
            "Exécutez d'abord le générateur de données IA."
        )

    donnees = pd.read_csv(DATASET)

    colonnes = VARIABLES + [CIBLE]
    manquantes = set(colonnes) - set(donnees.columns)
    if manquantes:
        raise ValueError(
            f"Colonnes manquantes : {sorted(manquantes)}"
        )

    if donnees[colonnes].isna().any().any():
        raise ValueError("Le dataset contient des valeurs manquantes.")

    x = donnees[VARIABLES]
    y = donnees[CIBLE]

    if not set(y.unique()).issubset({0, 1}):
        raise ValueError("La cible doit contenir uniquement 0 et 1.")

    if y.nunique() != 2 or y.value_counts().min() < 2:
        raise ValueError(
            "Chaque classe doit contenir au moins deux observations."
        )

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    modele = DecisionTreeClassifier(
        max_depth=3,
        random_state=42,
        class_weight="balanced",
    )
    modele.fit(x_train, y_train)

    predictions = modele.predict(x_test)

    resultats = {
        "observations_total": len(donnees),
        "observations_entrainement": len(x_train),
        "observations_test": len(x_test),
        "accuracy": float(accuracy_score(y_test, predictions)),
        "precision": float(
            precision_score(y_test, predictions, zero_division=0)
        ),
        "recall": float(
            recall_score(y_test, predictions, zero_division=0)
        ),
        "f1_score": float(
            f1_score(y_test, predictions, zero_division=0)
        ),
        "matrice_confusion": confusion_matrix(
            y_test, predictions, labels=[0, 1]
        ).tolist(),
    }

    MODELE.parent.mkdir(parents=True, exist_ok=True)

    joblib.dump(modele, MODELE)

    with METRIQUES.open("w", encoding="utf-8") as fichier:
        json.dump(resultats, fichier, indent=2, ensure_ascii=False)

    print("Entraînement terminé.")
    print(json.dumps(resultats, indent=2, ensure_ascii=False))
    print("\nRapport de classification :")
    print(classification_report(y_test, predictions, zero_division=0))

    return resultats


if __name__ == "__main__":
    entrainer()
