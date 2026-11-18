# Mapping PAIEMENT — AbAssurance / AssurePlus

## 1. Objectif

Unifier les paiements issus d'Oracle (`AB_PAIEMENT`) et de SQL Server (`AP_PAYMENTS`) dans l'entité cible `PAIEMENT`.

Le modèle doit préserver les références historiques, les montants, les dates et les informations propres à chaque système.

## 2. Mapping des attributs

| Attribut cible | Oracle | SQL Server | Transformation |
|---|---|---|---|
| paiement_id | — | — | Générer un identifiant unifié stable |
| reference_paiement | AB_PAYMENT_ID | AP_PAYMENT_REF | Convertir en représentation textuelle canonique |
| contrat_id | AB_POLICY_NUMBER | AP_CONTRACT_REF | Résoudre vers CONTRAT unifié |
| date_paiement | AB_DATE_PAIEMENT | AP_PAYMENT_DATETIME | Harmoniser en date/heure |
| montant | AB_MONTANT | AP_AMOUNT_PAID | Conserver la précision décimale |
| mode_paiement | AB_MODE_PAIEMENT | AP_PAYMENT_CHANNEL | Appliquer un référentiel commun |
| statut_transaction | — | AP_TRANSACTION_STATUS | Conserver le statut AP ; NULL pour AB |

## 3. Conservation des références historiques

Pour chaque paiement, conserver :

- `systeme_source` : `ABASSURANCE` ou `ASSUREPLUS`.
- `reference_paiement_source` : identifiant historique du paiement.
- `paiement_id` : identifiant unifié.

La combinaison `(systeme_source, reference_paiement_source)` est proposée comme clé unique de correspondance, sous réserve de vérification des contraintes réelles des sources.

## 4. Règles de transformation

### 4.1 Identifiants

- Convertir `AB_PAYMENT_ID` en texte sans modifier sa valeur.
- Convertir `AP_PAYMENT_REF` (UUID) dans un format canonique.
- Conserver le système d'origine pour distinguer les références.
- Garantir la stabilité de `paiement_id` lors des rechargements.

### 4.2 Dates

- Préserver la date et l'heure disponibles.
- Contrôler les valeurs invalides.
- Ne pas attribuer de fuseau horaire sans information fiable.
- Conserver les valeurs sources pour l'audit.

### 4.3 Montants

- Utiliser une représentation décimale exacte.
- Vérifier la devise et les conventions de signe.
- Ne pas convertir automatiquement les devises.
- Signaler les montants anormaux selon des règles métier à définir.

### 4.4 Modes de paiement

- Harmoniser `AB_MODE_PAIEMENT` et `AP_PAYMENT_CHANNEL`.
- Définir une table de correspondance.
- Conserver la valeur historique en complément de la valeur harmonisée.

### 4.5 Statuts de transaction

- Conserver `AP_TRANSACTION_STATUS`.
- Utiliser `NULL` pour les paiements Oracle si le statut est inconnu.
- Ne pas assimiler automatiquement l'existence d'un paiement à une transaction réussie.

### 4.6 Rattachement au contrat

- Rechercher le contrat par `(systeme_source, reference_contrat_source)`.
- Résoudre cette référence vers `contrat_id`.
- Signaler les références de contrat non résolues.
- Éviter de rattacher un paiement à un contrat uniquement sur une référence non qualifiée par sa source.

## 5. Contrôles qualité

- Unicité des références de paiement par système source.
- Présence d'une référence historique valide.
- Correspondance avec un contrat unifié.
- Validité des dates.
- Conservation de la précision des montants.
- Conformité des modes de paiement au référentiel.
- Conservation des statuts disponibles.
- Absence de doublons créés lors des rechargements.

## 6. Points à valider

- Contraintes exactes de clés primaires et étrangères.
- Devise et conventions de signe des montants.
- Référentiel des modes de paiement.
- Signification des statuts de transaction.
- Gestion des remboursements, annulations et rejets.
- Traitement des paiements sans contrat résolu.
- Règles de détection des doublons de paiement.
