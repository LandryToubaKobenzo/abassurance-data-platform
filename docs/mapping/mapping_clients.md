# Mapping des clients — AbAssurance / AssurePlus

## 1. Objectif

Définir les règles de correspondance et de transformation entre les données clients des deux compagnies d'assurance et le modèle unifié PostgreSQL.

**Sources :**
- Oracle AbAssurance : `AB_CLIENT`
- SQL Server AssurePlus : `AP_USERS`

**Cibles :**
- `assurance.client`
- `assurance.identite_source`

## 2. Correspondance des attributs

| Oracle — AB_CLIENT | SQL Server — AP_USERS | Attribut cible | Transformation |
|---|---|---|---|
| AB_CLIENT_ID | AP_USER_ID | identite_source.identifiant_source | Convertir en texte, conserver le système d'origine |
| AB_NOM | AP_FULL_NAME | client.nom | Direct pour Oracle ; extraction à définir pour AssurePlus |
| AB_PRENOM | AP_FULL_NAME | client.prenom | Direct pour Oracle ; extraction à définir pour AssurePlus |
| — | AP_FULL_NAME | client.nom_complet | Conserver le nom complet d'origine |
| AB_DATE_NAISSANCE | AP_BIRTH_DATE | client.date_naissance | Convertir en DATE |
| AB_EMAIL | AP_MAIL_ADDRESS | client.email | Nettoyer les espaces, normaliser la casse |
| AB_TELEPHONE | AP_PHONE_NUMBER | client.telephone | Harmoniser le format |
| AB_ADRESSE | AP_STREET_ADDRESS | client.adresse | Nettoyer les espaces |
| AB_CODE_POSTAL | AP_ZIP_CODE | client.code_postal | Conserver en texte |
| AB_NUM_FISCAL | — | client.numero_fiscal | NULL si absent |
| AB_DATE_CREATION | AP_CREATED_AT | client.date_creation | Harmoniser les dates et heures |
| AB_STATUT_CLIENT | AP_CUSTOMER_STATUS | client.statut_client | Appliquer une table de correspondance métier |
| — | AP_LOYALTY_SCORE | client.score_fidelite | Conserver si présent, sinon NULL |

Les noms d'attributs cibles correspondent au modèle unifié prévu. Leur existence et leurs types exacts doivent être vérifiés dans le schéma PostgreSQL avant l'implémentation.

## 3. Règles de transformation

### R01 — Identifiants historiques

Chaque enregistrement source conserve son identifiant d'origine dans `assurance.identite_source`.

Le couple `(systeme_source, identifiant_source)` doit identifier une référence source unique.

Valeurs de `systeme_source` :
- `ABASSURANCE`
- `ASSUREPLUS`

### R02 — Rapprochement des clients

Un même client peut être présent dans les deux systèmes.

Le rapprochement doit utiliser des critères de correspondance définis et vérifiés.

**Important :** deux clients ayant le même nom ne doivent pas être fusionnés automatiquement.

Les règles de rapprochement restent à valider avant toute fusion réelle.

### R03 — Nom complet

Oracle fournit séparément le nom et le prénom.

AssurePlus fournit `AP_FULL_NAME`.

La séparation automatique d'un nom complet peut être ambiguë. Le nom complet d'origine doit être conservé, et les règles d'extraction doivent être définies avant l'intégration.

### R04 — Dates

Les dates Oracle sont déjà typées.

`AP_BIRTH_DATE` est une chaîne au format `YYYY-MM-DD`.

La transformation doit vérifier la validité de chaque date et isoler les valeurs incorrectes.

### R05 — Email

Supprimer les espaces superflus et normaliser la casse pour les comparaisons.

Ne pas utiliser l'email comme identifiant unique sans validation métier.

### R06 — Téléphone

Harmoniser les numéros selon une convention à définir, sans supprimer les informations nécessaires à leur interprétation.

### R07 — Statuts clients

Créer une correspondance explicite entre les valeurs des deux systèmes.

Les valeurs inconnues doivent être signalées et non transformées arbitrairement.

### R08 — Score de fidélité

`AP_LOYALTY_SCORE` est disponible uniquement dans AssurePlus.

Pour les clients provenant uniquement d'AbAssurance, la valeur sera `NULL`.

## 4. Contrôles de qualité attendus

- Présence de l'identifiant historique.
- Unicité du couple système / identifiant source.
- Validité des dates.
- Vérification du format des emails lorsqu'ils sont renseignés.
- Cohérence des statuts clients.
- Absence de fusion non justifiée.
- Traçabilité de chaque client intégré.
- Détection et journalisation des enregistrements rejetés.

## 5. Points à confirmer

1. Colonnes et types exacts des tables PostgreSQL cibles.
2. Règles de séparation des noms AssurePlus.
3. Critères de rapprochement des identités.
4. Correspondance des statuts métier.
5. Format de normalisation des téléphones.
6. Politique de gestion des doublons et des données invalides.

## 6. Statut

**Mapping initial documenté — validation métier et technique en attente.**

Ce document constitue la base des futurs traitements d'extraction, transformation et chargement (ETL).
