# Rapport de validation SQL — Modèle unifié AbAssurance / AssurePlus

## 1. Objectif

Valider le fonctionnement du modèle de données unifié dans PostgreSQL (Supabase), avant l'intégration des données provenant d'Oracle AbAssurance et de SQL Server AssurePlus.

## 2. Environnement de test

- Plateforme : Supabase
- SGBD : PostgreSQL
- Schéma : `assurance`
- Nature des données : entièrement fictives
- Script de référence : `sql/tests/01_test_modele_unifie.sql`
- Méthode : transaction SQL avec `BEGIN` et `ROLLBACK`

## 3. Tables concernées

Le test couvre les six tables du modèle :

1. `client`
2. `intermediaire`
3. `identite_source`
4. `contrat`
5. `sinistre`
6. `paiement`

## 4. Scénarios de validation

### Test 01 — Insertion des clients

Insertion de deux clients fictifs dans le modèle unifié.

**Résultat :** insertion réussie.

### Test 02 — Traçabilité des identités

Insertion de trois références d'identité source, permettant notamment d'associer deux identifiants historiques à un même client unifié.

**Résultat :** insertion réussie.

### Test 03 — Gestion des intermédiaires

Insertion d'une agence AbAssurance et d'un courtier AssurePlus.

**Résultat :** insertion réussie.

### Test 04 — Relations entre les entités

Insertion de deux contrats associés aux clients et aux intermédiaires, puis de deux sinistres et de deux paiements.

**Résultat :** insertion réussie.

### Test 05 — Contrôle des volumes

| Table | Nombre de lignes insérées |
|---|---:|
| client | 2 |
| intermediaire | 2 |
| identite_source | 3 |
| contrat | 2 |
| sinistre | 2 |
| paiement | 2 |
| **Total** | **13** |

**Résultat :** les six tables ont retourné les volumes attendus pendant le test.

### Test 06 — Annulation transactionnelle

Exécution de `ROLLBACK` après les insertions et les contrôles.

Une nouvelle requête SQL a ensuite vérifié l'absence des identifiants de test dans les six tables.

**Résultat :** les six tables ont retourné `0` enregistrement pour les identifiants testés.

## 5. Conclusion

**Statut : VALIDÉ**

Le scénario d'insertion du modèle unifié a été exécuté avec succès. Les relations nécessaires aux données fictives testées ont fonctionné et le mécanisme transactionnel a permis d'annuler les insertions.

Cette validation ne couvre pas encore l'ensemble des cas métier, les performances, la sécurité applicative ou les flux réels d'ingestion Oracle et SQL Server.

## 6. Prochaines étapes

- Préparer les règles de transformation et de normalisation des données sources.
- Mettre en place les premiers flux d'ingestion.
- Ajouter des tests automatisés de qualité des données.
- Vérifier les règles de rapprochement des clients avant toute fusion réelle.
