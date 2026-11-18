# Mapping SINISTRE — AbAssurance / AssurePlus

## 1. Objectif

Unifier les sinistres issus d'Oracle (`AB_SINISTRE`) et de SQL Server (`AP_CLAIMS`) dans l'entité cible `SINISTRE`, en préservant les identifiants historiques et la traçabilité.

## 2. Mapping des attributs

| Attribut cible | Oracle | SQL Server | Transformation |
|---|---|---|---|
| sinistre_id | — | — | Générer un identifiant unifié stable |
| reference_sinistre | AB_CLAIM_ID | AP_SINISTRE_NUM | Conserver la référence historique |
| contrat_id | AB_POLICY_NUMBER | Référence de contrat source à confirmer | Résoudre vers CONTRAT unifié |
| date_sinistre | AB_DATE_SINISTRE | AP_INCIDENT_DATE | Harmoniser en date/heure |
| montant_estime | AB_MONTANT_ESTIME | AP_ESTIMATED_AMOUNT | Convertir en décimal précis |
| statut_sinistre | AB_STATUT_SINISTRE | AP_CLAIM_STATUS | Appliquer le référentiel des statuts |
| description | AB_DESCRIPTION | AP_CLAIM_COMMENT | Nettoyer sans perdre l'information métier |
| score_fraude | — | AP_FRAUD_SCORE | Conserver la valeur source ; NULL pour AbAssurance |

## 3. Conservation des identifiants historiques

Chaque sinistre conserve :

- Son système source : `ABASSURANCE` ou `ASSUREPLUS`.
- Sa référence source : `AB_CLAIM_ID` ou `AP_SINISTRE_NUM`.
- Son identifiant unifié : `sinistre_id`.

La combinaison `(systeme_source, reference_sinistre_source)` est proposée comme clé unique de correspondance.

## 4. Règles de transformation

### Dates

- Harmoniser les types date et date/heure.
- Conserver l'heure lorsqu'elle est présente.
- Contrôler les dates impossibles.
- Ne pas inventer de fuseau horaire.

### Montants

- Utiliser un type décimal adapté aux données financières.
- Préserver la précision des montants d'origine.
- Vérifier la devise avant toute conversion.

### Statuts

- Définir un référentiel commun des statuts.
- Conserver les statuts historiques.
- Signaler les statuts inconnus.

### Descriptions

- Conserver les commentaires utiles à l'analyse métier.
- Nettoyer les caractères techniques indésirables.
- Protéger les données personnelles potentiellement présentes dans les descriptions.

### Score de fraude

- Conserver le score AssurePlus sans le modifier.
- Utiliser `NULL` pour les sinistres AbAssurance.
- Vérifier l'échelle et la méthode de calcul du score avant son utilisation dans un modèle prédictif.

## 5. Contrôles qualité

- Unicité des références par système source.
- Présence d'une référence de sinistre.
- Correspondance avec un contrat unifié.
- Validité des dates.
- Cohérence des montants.
- Conformité des statuts au référentiel.
- Conservation des valeurs originales pour audit.

## 6. Points à valider

- Nom exact de la colonne de liaison vers le contrat dans `AP_CLAIMS`.
- Contraintes d'unicité des références de sinistres.
- Devise et règles d'arrondi des montants.
- Référentiel commun des statuts.
- Échelle du score de fraude AssurePlus.
- Gestion des sinistres sans contrat résolu.
