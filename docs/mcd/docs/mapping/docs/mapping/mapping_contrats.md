# Mapping CONTRAT — AbAssurance / AssurePlus

## 1. Objectif

Unifier les contrats d'assurance issus d'Oracle (`AB_CONTRAT`) et de SQL Server (`AP_CONTRACTS`) dans l'entité cible `CONTRAT`.

Les références historiques sont conservées afin d'assurer la traçabilité des contrats.

## 2. Mapping des attributs

| Attribut cible | Oracle | SQL Server | Transformation |
|---|---|---|---|
| contrat_id | — | — | Générer un identifiant unifié stable |
| reference_contrat | AB_POLICY_NUMBER | AP_CONTRACT_REF | Conserver la référence source |
| client_id | AB_CLIENT_ID | AP_USER_ID | Résoudre vers CLIENT unifié via IDENTITE_SOURCE |
| type_assurance | AB_TYPE_ASSURANCE | AP_PRODUCT_CODE | Harmoniser avec un référentiel produits |
| date_debut | AB_DATE_DEBUT | AP_START_DATE | Normaliser en DATE |
| date_fin | AB_DATE_FIN | AP_END_DATE | Normaliser en DATE |
| prime_annuelle | AB_PRIME_ANNUELLE | AP_MONTHLY_PREMIUM | Oracle : conserver ; AssurePlus : multiplier par 12 sous réserve de validation |
| statut_contrat | AB_STATUT_CONTRAT | AP_CONTRACT_STATE | Harmoniser avec un référentiel des statuts |
| intermediaire_id | AB_AGENCE_ID | AP_BROKER_CODE | Résoudre vers INTERMEDIAIRE unifié |

## 3. Identifiants historiques

L'identité d'un contrat source est définie par :

- `systeme_source` : `ABASSURANCE` ou `ASSUREPLUS`
- `reference_contrat_source` : `AB_POLICY_NUMBER` ou `AP_CONTRACT_REF`

La combinaison `(systeme_source, reference_contrat_source)` doit être unique dans les données intégrées, sous réserve de vérification des contraintes réelles des bases sources.

## 4. Règles de transformation

### 4.1 Primes

- AbAssurance : conserver `AB_PRIME_ANNUELLE`.
- AssurePlus : calculer `AP_MONTHLY_PREMIUM × 12`, après validation de la règle métier.
- Utiliser un type décimal précis pour les calculs financiers.
- Conserver la prime d'origine et sa périodicité pour l'audit.
- Ne pas convertir automatiquement les devises sans référentiel validé.

### 4.2 Dates

- Normaliser les dates de début et de fin.
- Vérifier que la date de fin n'est pas antérieure à la date de début.
- Préserver les valeurs nulles lorsque le contrat est sans échéance connue.
- Signaler les incohérences dans les contrôles qualité.

### 4.3 Statuts

Créer une table de correspondance entre les statuts Oracle, SQL Server et les statuts unifiés.

Aucune correspondance métier ne doit être inventée sans examen des valeurs réelles.

### 4.4 Types d'assurance

Harmoniser `AB_TYPE_ASSURANCE` et `AP_PRODUCT_CODE` avec un référentiel produit commun.

### 4.5 Clients et intermédiaires

- Résoudre `AB_CLIENT_ID` et `AP_USER_ID` vers le client unifié.
- Résoudre `AB_AGENCE_ID` vers un intermédiaire de type `AGENCE`.
- Résoudre `AP_BROKER_CODE` vers un intermédiaire de type `COURTIER`.
- Signaler les références non résolues, sans créer de correspondance fictive.

## 5. Contrôles qualité

- Unicité des références par système source.
- Présence d'une référence de contrat.
- Cohérence des dates.
- Montants numériques valides.
- Traçabilité des conversions de primes.
- Correspondance avec un client unifié.
- Correspondance avec un intermédiaire, lorsqu'il est renseigné.
- Statuts et produits conformes aux référentiels.

## 6. Points à valider

- Formule exacte d'annualisation des primes AssurePlus.
- Devise des primes dans chaque système.
- Correspondance des codes produits.
- Correspondance des statuts.
- Contraintes d'unicité des références.
- Gestion des contrats sans intermédiaire.
- Règles de rapprochement éventuel des contrats entre les deux systèmes.
