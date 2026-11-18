# AbAssurance / AssurePlus — Data Platform

Plateforme de démonstration pour l'unification des données de deux compagnies d'assurance fictives : AbAssurance (Oracle) et AssurePlus (SQL Server).

## 1. Objectif

Le projet vise à concevoir une architecture Data commune permettant de rapprocher les informations issues des deux systèmes historiques, d'améliorer la qualité des données et de préparer de futurs usages analytiques et IA.

Le dépôt contient un prototype pédagogique utilisant des données fictives. Il ne constitue pas une migration réelle des bases Oracle et SQL Server.

## 2. Organisation du dépôt

- `.github/workflows/` : automatisation des contrôles et démonstrations avec GitHub Actions.
- `data/` : données de démonstration et fichiers utilisés par les traitements.
- `docs/` : documentation technique, modèles de données, mapping et conventions Git.
- `models/` : artefacts liés au modèle IA de démonstration.
- `scripts/` : scripts d'exécution du pipeline, de génération de données IA, d'entraînement et de démonstration Spark.
- `sql/` : ressources SQL du projet.
- `src/abassurance/` : code Python métier, notamment normalisation, rapprochement, validation, pipeline et prédiction.
- `tests/` : tests automatisés.
- `streamlit_app.py` : interface de démonstration Streamlit.
- `requirements.txt` et `pyproject.toml` : dépendances et configuration Python.
- `sonar-project.properties` : configuration de l'analyse SonarQube.

## 3. Architecture : cible et prototype

### Architecture cible

La solution envisagée comprend des sources Oracle et SQL Server, une couche d'intégration de type Talend, des flux Kafka, un stockage Hadoop/HDFS, des traitements Apache Spark et des services analytiques ou IA.

Ces composants décrivent une architecture cible : leur présence dans la documentation ne signifie pas qu'ils sont tous déployés.

### Prototype réalisé

Le prototype comprend notamment :

- des données synthétiques et des fichiers JSON ;
- des traitements Python de normalisation et de rapprochement de clients ;
- une démonstration PySpark en mode local ;
- un modèle pédagogique de scoring du risque entraîné sur des données synthétiques ;
- la sauvegarde et le chargement du modèle pour la prédiction ;
- une API FastAPI avec documentation Swagger ;
- une interface Streamlit ;
- des workflows GitHub Actions pour les vérifications automatisées.

Les connexions réelles Oracle et SQL Server, ainsi que le déploiement d'un cluster Kafka, Hadoop ou Spark distribué, ne font pas partie du prototype.

## 4. Pipeline de données

Le pipeline Python vise à lire les données fictives, harmoniser les champs, normaliser les informations clients, rapprocher les identités et produire des données unifiées contrôlables.

Les scripts d'exécution sont regroupés dans `scripts/` et le code métier dans `src/abassurance/`.

## 5. Pipeline IA et API

Le cas d'usage IA démontré est le scoring du risque sur des observations synthétiques. Les scripts permettent de générer un jeu de données, d'entraîner et d'évaluer un modèle, puis de sauvegarder l'artefact pour son réemploi.

Le modèle est chargé pour réaliser des prédictions sans réentraînement à chaque appel. Une API FastAPI expose le service et sa documentation Swagger.

La fraude et la résiliation sont des cas d'usage envisagés, non des modèles opérationnels livrés.

## 6. Qualité, tests et intégration continue

Le dépôt utilise GitHub Actions pour automatiser, selon les workflows concernés, des contrôles de qualité Python, des tests, l'exécution du pipeline, une démonstration Spark, les étapes IA et la vérification de l'API Swagger.

Les fichiers de configuration incluent `pyproject.toml` et `sonar-project.properties`.

Les résultats et statuts sont consultables dans l'onglet **Actions** du dépôt. Les anciens échecs conservés dans l'historique ne doivent pas être confondus avec l'état des exécutions les plus récentes.

## 7. Modélisation et traçabilité

La documentation située dans `docs/mcd/mcd_unifie.md` décrit le modèle conceptuel unifié et son extension aux cas d'usage IA, notamment les entités, les relations et les features envisagées.

La provenance des données et la conservation des identifiants historiques constituent des principes de conception du projet.

## 8. Conventions Git

Le projet distingue les branches `main` et `develop`. La branche `develop` contient les évolutions du prototype et sert de référence pour la démonstration actuelle.

Les conventions de contribution sont documentées dans `docs/git-conventions.md`.

## 9. Démonstration

Interface Streamlit : https://abassurance-bachelor.streamlit.app

Dépôt GitHub : https://github.com/LandryToubaKobenzo/abassurance-data-platform

Pour examiner les réalisations techniques, sélectionner la branche `develop`, parcourir les dossiers du projet et consulter les résultats récents dans l'onglet **Actions**.

## 10. Limites

Ce projet est une preuve de concept pédagogique. Les données sont fictives et les métriques IA ne démontrent pas une performance sur des données d'assurance réelles. L'architecture Big Data complète reste une cible de conception.
