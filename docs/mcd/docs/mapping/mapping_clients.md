# Mapping CLIENT — AbAssurance / AssurePlus

## Sources

- Oracle : `AB_CLIENT`
- SQL Server : `AP_USERS`
- Cible : `CLIENT` et `IDENTITE_SOURCE`

## Mapping détaillé

| Attribut cible | Oracle | SQL Server | Transformation |
|---|---|---|---|
| client_id | — | — | Générer un identifiant unifié stable |
| nom | AB_NOM | AP_FULL_NAME | Nettoyer / découpage prudent |
| prenom | AB_PRENOM | AP_FULL_NAME | Nettoyer / découpage prudent |
| nom_complet | AB_NOM + AB_PRENOM | AP_FULL_NAME | Construire ou conserver le nom complet |
| date_naissance | AB_DATE_NAISSANCE | AP_BIRTH_DATE | Convertir en DATE, valider YYYY-MM-DD côté AP |
| email | AB_EMAIL | AP_MAIL_ADDRESS | Trim, normalisation de casse, validation |
| telephone | AB_TELEPHONE | AP_PHONE_NUMBER | Nettoyage, normalisation conditionnelle |
| adresse | AB_ADRESSE | AP_STREET_ADDRESS | Nettoyage, conserver la valeur source |
| code_postal | AB_CODE_POSTAL | AP_ZIP_CODE | Conserver comme texte |
| numero_fiscal | AB_NUM_FISCAL | — | Valeur absente pour AP |
| date_creation | AB_DATE_CREATION | AP_CREATED_AT | Harmoniser date/heure et fuseau si connu |
| statut_client | AB_STATUT_CLIENT | AP_CUSTOMER_STATUS | Table de correspondance à définir |
| score_fidelite | — | AP_LOYALTY_SCORE | Valeur absente pour AB |

## Conservation des identifiants historiques

- `AB_CLIENT_ID` → `IDENTITE_SOURCE` avec `systeme_source = ABASSURANCE`
- `AP_USER_ID` → `IDENTITE_SOURCE` avec `systeme_source = ASSUREPLUS`
- Unicité proposée : (`systeme_source`, `identifiant_historique`).

## Règles de fusion

1. Normaliser les données sans perdre les valeurs originales.
2. Identifier les correspondances candidates.
3. Fusionner uniquement les correspondances suffisamment fiables et justifiables.
4. Soumettre les cas ambigus à une revue.
5. Conserver toutes les identités historiques du client unifié.
6. Journaliser les décisions de rapprochement.
7. Définir des règles de priorité par attribut avant de choisir les valeurs finales.

## Contrôles qualité

- Unicité de chaque identité source.
- Absence d'identifiants historiques orphelins.
- Dates valides et cohérentes.
- Codes postaux préservant les zéros initiaux.
- Statuts conformes au référentiel harmonisé.
- Pas de perte d'identifiants lors des fusions.
- Protection des données personnelles dans les logs et jeux de test.

## Points à valider

- Critères et seuils de rapprochement des clients.
- Règles de priorité en cas de valeurs contradictoires.
- Référentiel des statuts clients.
- Pays et formats téléphoniques attendus.
- Fuseaux horaires des deux systèmes.
- Gestion des noms composés et non décomposables.
