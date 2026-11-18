
-- ============================================================
-- AbAssurance + AssurePlus
-- MPD unifie - PostgreSQL
-- ============================================================

CREATE SCHEMA IF NOT EXISTS assurance;

-- 1. CLIENT
CREATE TABLE assurance.client (
    client_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nom VARCHAR(100),
    prenom VARCHAR(100),
    nom_complet VARCHAR(200),
    date_naissance DATE,
    email VARCHAR(150),
    telephone VARCHAR(25),
    adresse VARCHAR(255),
    code_postal VARCHAR(10),
    numero_fiscal VARCHAR(30),
    statut_client VARCHAR(20),
    score_fidelite INTEGER,
    date_creation TIMESTAMP,
    CONSTRAINT chk_score_fidelite
        CHECK (score_fidelite IS NULL OR score_fidelite >= 0)
);

-- 2. IDENTITE_SOURCE
-- Conservation des identifiants clients historiques.
CREATE TABLE assurance.identite_source (
    identite_source_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    client_id BIGINT NOT NULL,
    systeme_source VARCHAR(20) NOT NULL,
    identifiant_source VARCHAR(100) NOT NULL,

    CONSTRAINT fk_identite_client
        FOREIGN KEY (client_id)
        REFERENCES assurance.client(client_id),

    CONSTRAINT chk_identite_systeme
        CHECK (systeme_source IN ('ABASSURANCE', 'ASSUREPLUS')),

    CONSTRAINT uq_identite_source
        UNIQUE (systeme_source, identifiant_source)
);

-- 3. INTERMEDIAIRE
CREATE TABLE assurance.intermediaire (
    intermediaire_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    type_intermediaire VARCHAR(10) NOT NULL,
    systeme_source VARCHAR(20) NOT NULL,
    identifiant_source VARCHAR(100) NOT NULL,

    CONSTRAINT chk_type_intermediaire
        CHECK (type_intermediaire IN ('AGENCE', 'COURTIER')),

    CONSTRAINT chk_intermediaire_systeme
        CHECK (systeme_source IN ('ABASSURANCE', 'ASSUREPLUS')),

    CONSTRAINT uq_intermediaire_source
        UNIQUE (systeme_source, identifiant_source)
);

-- 4. CONTRAT
CREATE TABLE assurance.contrat (
    contrat_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    client_id BIGINT NOT NULL,
    intermediaire_id BIGINT,
    systeme_source VARCHAR(20) NOT NULL,
    reference_source VARCHAR(30) NOT NULL,
    type_assurance VARCHAR(50),
    date_debut DATE,
    date_fin DATE,
    prime_source NUMERIC(12,2),
    periodicite_prime VARCHAR(10),
    prime_annuelle_normalisee NUMERIC(12,2),
    statut_contrat VARCHAR(20),

    CONSTRAINT fk_contrat_client
        FOREIGN KEY (client_id)
        REFERENCES assurance.client(client_id),

    CONSTRAINT fk_contrat_intermediaire
        FOREIGN KEY (intermediaire_id)
        REFERENCES assurance.intermediaire(intermediaire_id),

    CONSTRAINT chk_contrat_systeme
        CHECK (systeme_source IN ('ABASSURANCE', 'ASSUREPLUS')),

    CONSTRAINT chk_periodicite
        CHECK (periodicite_prime IN ('MENSUELLE', 'ANNUELLE')),

    CONSTRAINT chk_dates_contrat
        CHECK (date_fin IS NULL OR date_debut IS NULL
               OR date_fin >= date_debut),

    CONSTRAINT chk_prime_source
        CHECK (prime_source IS NULL OR prime_source >= 0),

    CONSTRAINT chk_prime_annuelle
        CHECK (
            prime_annuelle_normalisee IS NULL
            OR prime_annuelle_normalisee >= 0
        ),

    CONSTRAINT uq_contrat_source
        UNIQUE (systeme_source, reference_source)
);

-- 5. SINISTRE
CREATE TABLE assurance.sinistre (
    sinistre_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    contrat_id BIGINT NOT NULL,
    systeme_source VARCHAR(20) NOT NULL,
    identifiant_source VARCHAR(100) NOT NULL,
    date_sinistre TIMESTAMP,
    montant_estime NUMERIC(12,2),
    statut_sinistre VARCHAR(30),
    description TEXT,
    score_fraude NUMERIC(5,2),

    CONSTRAINT fk_sinistre_contrat
        FOREIGN KEY (contrat_id)
        REFERENCES assurance.contrat(contrat_id),

    CONSTRAINT chk_sinistre_systeme
        CHECK (systeme_source IN ('ABASSURANCE', 'ASSUREPLUS')),

    CONSTRAINT chk_montant_estime
        CHECK (montant_estime IS NULL OR montant_estime >= 0),

    CONSTRAINT uq_sinistre_source
        UNIQUE (systeme_source, identifiant_source)
);

-- 6. PAIEMENT
CREATE TABLE assurance.paiement (
    paiement_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    contrat_id BIGINT NOT NULL,
    systeme_source VARCHAR(20) NOT NULL,
    identifiant_source VARCHAR(100) NOT NULL,
    date_paiement TIMESTAMP,
    montant NUMERIC(12,2),
    mode_paiement VARCHAR(30),
    statut_transaction VARCHAR(20),

    CONSTRAINT fk_paiement_contrat
        FOREIGN KEY (contrat_id)
        REFERENCES assurance.contrat(contrat_id),

    CONSTRAINT chk_paiement_systeme
        CHECK (systeme_source IN ('ABASSURANCE', 'ASSUREPLUS')),

    CONSTRAINT chk_montant_paiement
        CHECK (montant IS NULL OR montant >= 0),

    CONSTRAINT uq_paiement_source
        UNIQUE (systeme_source, identifiant_source)
);

-- ============================================================
-- Index pour les jointures et recherches courantes
-- ============================================================

CREATE INDEX idx_identite_client
    ON assurance.identite_source(client_id);

CREATE INDEX idx_contrat_client
    ON assurance.contrat(client_id);

CREATE INDEX idx_contrat_intermediaire
    ON assurance.contrat(intermediaire_id);

CREATE INDEX idx_sinistre_contrat
    ON assurance.sinistre(contrat_id);

CREATE INDEX idx_paiement_contrat
    ON assurance.paiement(contrat_id);

CREATE INDEX idx_sinistre_date
    ON assurance.sinistre(date_sinistre);

CREATE INDEX idx_paiement_date
    ON assurance.paiement(date_paiement);
