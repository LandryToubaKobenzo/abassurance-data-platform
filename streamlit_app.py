
"""Interface web de démonstration AbAssurance–AssurePlus."""

import sys
from pathlib import Path

import streamlit as st

# Permet d'importer le package Python depuis le dossier src.
RACINE = Path(__file__).resolve().parent
sys.path.insert(0, str(RACINE / "src"))

from abassurance.prediction import predire_risque  # noqa: E402


st.set_page_config(
    page_title="AbAssurance – Plateforme Data & IA",
    page_icon="🛡️",
    layout="centered",
)

st.title("🛡️ AbAssurance – Plateforme Data & IA")
st.subheader("Projet de fusion AbAssurance / AssurePlus")

st.info(
    "Application pédagogique développée dans le cadre "
    "du Bachelor Concepteur Développeur & IA – Bloc 3."
)

st.markdown(
    """
    ### Présentation du projet

    L'objectif est de proposer une plateforme permettant
    d'unifier les données de deux compagnies d'assurance :

    - **AbAssurance** : système historique Oracle.
    - **AssurePlus** : système historique SQL Server.

    Le prototype comprend un pipeline Python d'unification
    des clients, une démonstration Apache Spark et
    un modèle de prédiction du risque de sinistre.
    """
)

st.divider()

st.header("🤖 Démonstration du modèle prédictif")

st.write(
    "Saisissez les caractéristiques d'un assuré fictif "
    "pour obtenir une classification indicative du risque."
)

age = st.number_input(
    "Âge de l'assuré",
    min_value=18,
    max_value=100,
    value=45,
    step=1,
)

sinistres = st.number_input(
    "Nombre de sinistres précédents",
    min_value=0,
    max_value=20,
    value=2,
    step=1,
)

anciennete = st.number_input(
    "Ancienneté du contrat (années)",
    min_value=0,
    max_value=80,
    value=4,
    step=1,
)

if st.button("Prédire le risque", type="primary"):
    resultat = predire_risque(
        int(age),
        int(sinistres),
        int(anciennete),
    )

    if resultat == "Élevé":
        st.warning(f"Risque prédit : {resultat}")
    else:
        st.success(f"Risque prédit : {resultat}")

st.divider()

st.header("⚙️ Architecture du projet")

st.markdown(
    """
    **Architecture cible :**

    Oracle / SQL Server → Talend → Kafka
    → Spark → Hadoop → Intelligence artificielle

    **Composants effectivement démontrés :**

    - Unification des clients avec Python.
    - Tests automatisés et contrôle qualité.
    - Traitement PySpark en mode local.
    - Prototype de prédiction avec scikit-learn.
    - Interface web avec Streamlit.
    """
)

st.header("📋 Limites de la démonstration")

st.markdown(
    """
    Les données utilisées sont entièrement fictives. Le modèle de classification
    est entraîné sur 300 observations synthétiques reproductibles, dont 240 pour
    l'entraînement et 60 pour le test. Une évaluation technique a été réalisée
    à l'aide des métriques accuracy, précision, rappel, F1-score et matrice
    de confusion.

    Les résultats obtenus sur ces données artificielles ne permettent pas de
    conclure à une performance équivalente sur des données réelles. Ce prototype
    ne doit pas être utilisé pour prendre des décisions concernant des assurés.

    Les composants Talend, Kafka et Hadoop relèvent de l'architecture cible
    et ne sont pas déployés dans cette démonstration.
    """
)

st.divider()

st.markdown(
    "[Consulter le code source sur GitHub]"
    "(https://github.com/LandryToubaKobenzo/abassurance-data-platform)"
)
