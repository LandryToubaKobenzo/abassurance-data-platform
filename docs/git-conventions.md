
# Convention de nommage Git

## Branches principales

- main : versions stables et validées
- develop : intégration des développements

## Branches temporaires

Format : type/description-courte

- feature/ : nouvelle fonctionnalité
- fix/ : correction de bug
- docs/ : documentation
- test/ : tests
- refactor/ : amélioration du code
- hotfix/ : correction urgente
- release/ : préparation de version

## Exemples

feature/data-cleaning
feature/kafka-ingestion
feature/spark-transformation
feature/ml-prediction
fix/client-duplicates
docs/unified-mcd

## Règles

1. Utiliser des noms en minuscules.
2. Séparer les mots avec des tirets.
3. Créer les branches feature depuis develop.
4. Utiliser les Pull Requests pour intégrer le code.
5. Valider les tests avant fusion.
6. Ne jamais publier de secrets ni de données clients.

## Convention des commits

feat: add data cleaning
fix: correct duplicate handling
test: add mapping tests
docs: update architecture
ci: add quality workflow
