-- ============================================================
--  Datenbankschema  |  BudgetBuddy – HTL Reutte – 3H – Projektarbeit
-- ============================================================
--
--  Einmalig ausführen mit:
--    python -c "from app import db_init; db_init()"
-- ============================================================

-- Tabelle Benutzer
CREATE TABLE IF NOT EXISTS benutzer (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    username    VARCHAR(255) NOT NULL UNIQUE,
    email       VARCHAR(255) NOT NULL UNIQUE,
    passwort    VARCHAR(255) NOT NULL,
    gesperrt    INTEGER NOT NULL DEFAULT 0,        -- 0 = aktiv, 1 = gesperrt
    erstellt_am VARCHAR(255) DEFAULT (datetime('now'))
);

-- Tabelle Kategorie
CREATE TABLE IF NOT EXISTS kategorie (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        VARCHAR(255) NOT NULL,
    benutzer_id INTEGER REFERENCES benutzer(id)    -- NULL = Systemkategorie
);

-- Tabelle Transaktion
CREATE TABLE IF NOT EXISTS transaktion (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    benutzer_id  INTEGER NOT NULL REFERENCES benutzer(id),
    kategorie_id INTEGER NOT NULL REFERENCES kategorie(id),
    betrag       INTEGER NOT NULL,                 -- in Cent
    notiz        VARCHAR(255),                     -- optional
    datum        VARCHAR(10) NOT NULL,              -- Format: YYYY-MM-DD
    erstellt_am  VARCHAR(255) DEFAULT (datetime('now'))
);

-- Tabelle budget_limit
CREATE TABLE IF NOT EXISTS budget_limit (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    benutzer_id  INTEGER NOT NULL REFERENCES benutzer(id),
    kategorie_id INTEGER NOT NULL REFERENCES kategorie(id),
    monat        VARCHAR(7) NOT NULL,
    limit_betrag INTEGER NOT NULL
);

-- Beispiel-Systemkategorien (zum Testen, NULL = für alle Benutzer sichtbar)
INSERT INTO kategorie (name, benutzer_id) VALUES ('Essen', NULL);
INSERT INTO kategorie (name, benutzer_id) VALUES ('Freizeit', NULL);
INSERT INTO kategorie (name, benutzer_id) VALUES ('Kleidung', NULL);
INSERT INTO kategorie (name, benutzer_id) VALUES ('Transport', NULL);
INSERT INTO kategorie (name, benutzer_id) VALUES ('Sonstiges', NULL);