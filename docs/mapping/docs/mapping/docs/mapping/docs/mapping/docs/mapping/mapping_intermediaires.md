# Mapping INTERMEDIAIRE — AbAssurance / AssurePlus

## 1. Objectif

Unifier les références d'agences AbAssurance et de courtiers AssurePlus dans une entité conceptuelle commune `INTERMEDIAIRE`.

Cette entité permet de rattacher chaque contrat à son intermédiaire, tout en conservant l'origine des références.

## 2. Sources

### Oracle — AbAssurance

- Table : `AB_CONTRAT`
- Colonne : `AB_AGENCE_ID`
- Type source : `NUMBER`
- Type métier : `AGENCE`

### SQL Server — AssurePlus

- Table : `AP_CONTRACTS`
- Colonne : `AP_BROKER_CODE`
- Type source : `NVARCHAR(30)`
- Type métier : `COURTIER`

Aucune table détaillée des agences ou courtiers n'a été fournie à ce stade.

## 3. Mapping des attributs

| Attribut cible | Oracle | SQL Server | Transformation |
|---|---|---|---|
| intermediaire_id | — | — | Générer un identifiant unifié stable |
| type_intermediaire | — | — | AGENCE pour Oracle, COURTIER pour SQL Server |
| reference_intermediaire | AB_AGENCE_ID | AP_BROKER_CODE | Convertir en référence textuelle canonique |
| systeme_source | ABASSURANCE | ASSUREPLUS | Conserver le système d'origine |

## 4. Règles de transformation

### 4.1 Identification

Chaque intermédiaire est identifié, dans cette première version, par :

- `systeme_source`
- `reference_intermediaire`

La combinaison de ces deux champs constitue une clé métier candidate.

Les identifiants numériques Oracle sont convertis en texte sans perte d'information. Les codes SQL Server sont nettoyés sans modifier arbitrairement leur signification.

### 4.2 Type d'intermédiaire

Les valeurs autorisées sont :

- `AGENCE`
- `COURTIER`

Les intermédiaires provenant d'AbAssurance reçoivent le type `AGENCE`.

Les intermédiaires provenant d'AssurePlus reçoivent le type `COURTIER`.

### 4.3 Déduplication

- Réutiliser le même `intermediaire_id` pour les occurrences répétées d'une même référence dans un même système.
- Ne pas fusionner automatiquement des intermédiaires de systèmes différents.
- Ne pas considérer deux références identiques comme représentant nécessairement le même intermédiaire.
- Préserver les références historiques.

### 4.4 Rattachement aux contrats

Pour AbAssurance :

`AB_CONTRAT.AB_AGENCE_ID` → `INTERMEDIAIRE.intermediaire_id`

Pour AssurePlus :

`AP_CONTRACTS.AP_BROKER_CODE` → `INTERMEDIAIRE.intermediaire_id`

La résolution doit utiliser le système source et la référence historique.

### 4.5 Valeurs manquantes

- Ne pas créer de faux intermédiaire pour remplacer une référence absente.
- Conserver un rattachement non renseigné lorsque la règle métier l'autorise.
- Signaler les références invalides ou impossibles à résoudre.

## 5. Contrôles qualité

- Unicité de `(systeme_source, reference_intermediaire)` pour les références renseignées.
- Présence d'un type autorisé : AGENCE ou COURTIER.
- Stabilité des identifiants unifiés lors des rechargements.
- Absence de doublons techniques.
- Conservation des références historiques.
- Cohérence entre la source du contrat et celle de l'intermédiaire.

## 6. Limites du modèle actuel

Les informations suivantes ne sont pas disponibles dans les schémas fournis :

- Nom de l'agence ou du courtier.
- Adresse de l'intermédiaire.
- Coordonnées de contact.
- Statut d'activité.
- Informations contractuelles détaillées.

Ces attributs ne doivent pas être inventés.

## 7. Points à valider

- Unicité réelle des références dans chaque système.
- Possibilité qu'un intermédiaire soit partagé entre plusieurs compagnies.
- Gestion des intermédiaires absents.
- Existence éventuelle de tables de référence supplémentaires.
- Cardinalité exacte de l'association INTERMEDIAIRE–CONTRAT.
