
-- =====================================================
-- ABASSURANCE DATA PLATFORM
-- Test d'insertion des 6 tables du schema assurance
-- Donnees 100 % fictives
-- Aucune modification conservee : ROLLBACK final
-- =====================================================

BEGIN;

-- =====================================================
-- 1. CLIENTS
-- =====================================================

INSERT INTO assurance.client (
    client_id,
    nom,
    prenom,
    nom_complet,
    date_naissance,
    email,
    statut_client,
    score_fidelite
)
OVERRIDING SYSTEM VALUE
VALUES
(
    910001,
    'Martin',
    'Alice',
    'Alice Martin',
    DATE '1988-04-12',
    'alice.martin@example.com',
    'ACTIF',
    85
),
(
    910002,
    'Dupont',
    'Jean',
    'Jean Dupont',
    DATE '1990-09-23',
    'jean.dupont@example.com',
    'ACTIF',
    70
);

-- =====================================================
-- 2. INTERMEDIAIRES
-- =====================================================

INSERT INTO assurance.intermediaire (
    intermediaire_id,
    type_intermediaire,
    systeme_source,
    identifiant_source
)
OVERRIDING SYSTEM VALUE
VALUES
(
    920001,
    'AGENCE',
    'ABASSURANCE',
    '101'
),
(
    920002,
    'COURTIER',
    'ASSUREPLUS',
    'BRK-202'
);

-- =====================================================
-- 3. IDENTITES SOURCES
-- =====================================================

INSERT INTO assurance.identite_source (
    identite_source_id,
    client_id,
    systeme_source,
    identifiant_source
)
OVERRIDING SYSTEM VALUE
VALUES
(
    930001,
    910001,
    'ABASSURANCE',
    '1001'
),
(
    930002,
    910001,
    'ASSUREPLUS',
    '2001'
),
(
    930003,
    910002,
    'ASSUREPLUS',
    '2002'
);

-- =====================================================
-- 4. CONTRATS
-- =====================================================

INSERT INTO assurance.contrat (
    contrat_id,
    client_id,
    intermediaire_id,
    systeme_source,
    reference_source,
    type_assurance,
    date_debut,
    date_fin,
    prime_source,
    periodicite_prime,
    prime_annuelle_normalisee,
    statut_contrat
)
OVERRIDING SYSTEM VALUE
VALUES
(
    940001,
    910001,
    920001,
    'ABASSURANCE',
    'AB-POL-TEST-001',
    'AUTO',
    DATE '2025-01-01',
    DATE '2026-12-31',
    600.00,
    'ANNUELLE',
    600.00,
    'ACTIF'
),
(
    940002,
    910001,
    920002,
    'ASSUREPLUS',
    'AP-CTR-TEST-001',
    'HABITATION',
    DATE '2025-03-01',
    DATE '2026-12-31',
    45.00,
    'MENSUELLE',
    540.00,
    'ACTIF'
);

-- Hypothese de test :
-- prime annuelle AssurePlus = 45.00 x 12 = 540.00

-- =====================================================
-- 5. SINISTRES
-- =====================================================

INSERT INTO assurance.sinistre (
    sinistre_id,
    contrat_id,
    systeme_source,
    identifiant_source,
    date_sinistre,
    montant_estime,
    statut_sinistre,
    description,
    score_fraude
)
OVERRIDING SYSTEM VALUE
VALUES
(
    950001,
    940001,
    'ABASSURANCE',
    '3001',
    TIMESTAMP '2025-06-12 14:30:00',
    1200.00,
    'OUVERT',
    'Sinistre automobile fictif',
    NULL
),
(
    950002,
    940002,
    'ASSUREPLUS',
    '4001',
    TIMESTAMP '2025-08-04 11:15:00',
    350.00,
    'OUVERT',
    'Degat des eaux fictif',
    12.50
);

-- =====================================================
-- 6. PAIEMENTS
-- =====================================================

INSERT INTO assurance.paiement (
    paiement_id,
    contrat_id,
    systeme_source,
    identifiant_source,
    date_paiement,
    montant,
    mode_paiement,
    statut_transaction
)
OVERRIDING SYSTEM VALUE
VALUES
(
    960001,
    940001,
    'ABASSURANCE',
    '5001',
    TIMESTAMP '2025-01-05 09:00:00',
    600.00,
    'VIREMENT',
    NULL
),
(
    960002,
    940002,
    'ASSUREPLUS',
    '550e8400-e29b-41d4-a716-446655440000',
    TIMESTAMP '2025-03-05 09:00:00',
    45.00,
    'CARTE',
    'VALIDEE'
);

-- =====================================================
-- 7. VERIFICATION DES INSERTIONS
-- =====================================================

SELECT
    'client' AS table_name,
    COUNT(*) AS nb_lignes
FROM assurance.client
WHERE client_id BETWEEN 910001 AND 910002

UNION ALL

SELECT
    'intermediaire',
    COUNT(*)
FROM assurance.intermediaire
WHERE intermediaire_id BETWEEN 920001 AND 920002

UNION ALL

SELECT
    'identite_source',
    COUNT(*)
FROM assurance.identite_source
WHERE identite_source_id BETWEEN 930001 AND 930003

UNION ALL

SELECT
    'contrat',
    COUNT(*)
FROM assurance.contrat
WHERE contrat_id BETWEEN 940001 AND 940002

UNION ALL

SELECT
    'sinistre',
    COUNT(*)
FROM assurance.sinistre
WHERE sinistre_id BETWEEN 950001 AND 950002

UNION ALL

SELECT
    'paiement',
    COUNT(*)
FROM assurance.paiement
WHERE paiement_id BETWEEN 960001 AND 960002;

-- =====================================================
-- 8. ANNULATION DES DONNEES DE TEST
-- =====================================================

ROLLBACK;
