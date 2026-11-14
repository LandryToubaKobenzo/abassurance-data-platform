
"""Prototype pédagogique de prédiction du risque de sinistre."""

from sklearn.tree import DecisionTreeClassifier


def entrainer_modele():
    """Entraîne un modèle sur des exemples synthétiques."""

    # [âge, nombre de sinistres précédents, ancienneté du contrat]
    caracteristiques = [
        [25, 0, 2],
        [42, 0, 10],
        [35, 1, 5],
        [55, 3, 8],
        [29, 2, 1],
        [48, 0, 15],
        [62, 4, 3],
        [31, 0, 6],
        [45, 2, 4],
        [38, 1, 9],
    ]

    # 0 = risque faible ; 1 = risque élevé
    etiquettes = [0, 0, 0, 1, 1, 0, 1, 0, 1, 0]

    modele = DecisionTreeClassifier(max_depth=3, random_state=42)
    modele.fit(caracteristiques, etiquettes)
    return modele


def predire_risque(age, sinistres_precedents, anciennete_contrat):
    """Prédit une catégorie de risque à partir de trois variables."""

    modele = entrainer_modele()
    prediction = modele.predict(
        [[age, sinistres_precedents, anciennete_contrat]]
    )[0]

    return "Élevé" if prediction == 1 else "Faible"


if __name__ == "__main__":
    resultat = predire_risque(45, 2, 4)
    print(f"Risque de sinistre prédit : {resultat}")
