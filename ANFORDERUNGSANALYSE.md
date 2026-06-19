# Anforderungsanalyse – BudgetBuddy
**Projekt BudgetBuddy | HTL Reutte 3H | 2025/26**

Dieses Dokument beschreibt verbindlich, was die App leisten MUSS. Es ist die Grundlage für Entwicklung, Test und Abnahme. Alle Änderungen an diesem Dokument werden versioniert.

---

## 1 Zielbeschreibung 💡

Die App "BudgetBuddy" ermöglicht es Jugendlichen, die ihr Geld auf etwas Besonderes sparen wollen, einen Überblick über ihre Finanzen übersichtlich zu verschaffen. Der Benutzer kann Budgetlimits für bestimmte Tätigkeiten wie zum Beispiel Freizeit und Kleidung festlegen. Das Ziel ist es, Jugendlichen einen bewussten Umgang mit Geld zu fördern. Der Administrator kann jederzeit Konten verwalten und bei Bedarf sperren/löschen.

---

## 2 Akteure 💡

| Kürzel | Akteur | Beschreibung & Rechte |
|--------|--------|----------------------|
| A1 | Schüler/in | Kann sich registrieren und einloggen. Kann Einnahmen und Ausgaben erfassen, bearbeiten und löschen. Kann Budgetlimits festlegen. Sieht nur die eigenen Daten. |
| A2 | Administrator | Kann alle Benutzerkonten sehen, sperren und löschen. Kann jederzeit Updates und Änderungen durchführen. |
| A3 | Datenbank (System) | Speichert alle Benutzer-, Transaktions- und Kategoriendaten dauerhaft. Wird vom Backend über Prepared Statements angesprochen. |

---

## 3 Use Cases 💡

| UC-ID | Name | Akteur | Beschreibung | Vorbedingung | Ergebnis |
|-------|------|--------|-------------|--------------|---------|
| UC01 | Registrierung | A1 | Benutzer gibt Benutzername, E-Mail und Passwort ein und erstellt ein Konto. | App geöffnet, noch kein Konto vorhanden | Konto wurde erstellt, Benutzer ist eingeloggt |
| UC02 | Login | A1, A2 | Benutzer gibt Benutzernamen und Passwort ein. | App geöffnet, Konto vorhanden | Benutzer ist authentifiziert und sieht das Dashboard |
| UC03 | Ausgabe erfassen | A1 | Benutzer gibt Betrag und optionale Notiz ein. | Eingeloggt | Transaktion gespeichert, Dashboard aktualisiert |
| UC04 | Einnahme erfassen | A1 | Benutzer erfasst eine Einnahme mit Betrag | Eingeloggt | Einnahme gespeichert |
| UC05 | Budgetlimit setzen | A1 | Benutzer legt für eine bestimmte Kategorie ein monatliches Limit fest. | Eingeloggt, Kategorie vorhanden | Limit gespeichert |
| UC06 | Monatsübersicht anzeigen | A1 | Benutzer sieht alle Transaktionen des aktuellen Monats | Eingeloggt, mind. 1 Transaktion vorhanden | Übersicht mit Kreisdiagramm wird angezeigt |
| UC07 | Transaktion löschen | A1 | Benutzer wählt eine Transaktion aus und bestätigt das Löschen. | Eingeloggt, Transaktion vorhanden | Transaktion gelöscht, Saldo aktualisiert |
| UC08 | Benutzer verwalten (Admin) | A2 | Admin sieht alle registrierten Benutzer und kann Konten sperren. | Als Admin eingeloggt | Benutzerliste angezeigt, Aktionen möglich |

---

## 4 Funktionale Anforderungen (FA) 💡

| FA-Nr. | Beschreibung | Priorität | Akteur |
|--------|-------------|-----------|--------|
| FA01 | Benutzer können sich mit Benutzername und Passwort registrieren und einloggen/ausloggen. | Hoch | A1, A2 |
| FA02 | Benutzer können eine Transaktion (Ausgabe oder Einnahme) mit Betrag, Kategorie, Datum und optionaler Notiz erfassen. | Hoch | A1 |
| FA03 | Benutzer können Transaktionen bearbeiten oder löschen. | Hoch | A1 |
| FA04 | Das System berechnet automatisch den aktuellen Kontostand (Einnahmen minus Ausgaben). | Hoch | System |
| FA05 | Benutzer können pro Kategorie ein monatliches Budgetlimit festlegen. Das System warnt, wenn 80 % und 100 % des Limits erreicht sind. | Mittel | A1 |
| FA06 | Benutzer sehen eine Monatsübersicht mit Kreisdiagramm der Ausgaben nach Kategorien. | Mittel | A1 |
| FA07 | Benutzer können Transaktionen nach Kategorie, Datum oder Betrag filtern und sortieren. | Mittel | A1 |
| FA08 | Administratoren können Benutzerkonten einsehen und sperren/entsperren. | Niedrig | A2 |
| FA09 | Benutzer können ihr Passwort ändern. | Niedrig | A1 |

---

## 5 Nicht-funktionale Anforderungen (NFA) 💡

| NFA-Nr. | Kategorie | Beschreibung |
|---------|-----------|-------------|
| NFA01 | Sicherheit | Passwörter werden gehasht gespeichert (bcrypt, min. 10 Rounds) – niemals im Klartext. |
| NFA02 | Sicherheit | Alle DB-Abfragen verwenden Prepared Statements (kein SQL-Injection-Risiko). |
| NFA03 | Sicherheit | Sessions werden nach 30 Minuten Inaktivität automatisch beendet. Session-Token sind zufällig und nicht erratbar. |
| NFA04 | Sicherheit | Eingabefelder werden serverseitig validiert und bereinigt (XSS-Schutz). |
| NFA05 | Bedienbarkeit | Fehlermeldungen sind auf Deutsch, verständlich und geben Hinweise zur Behebung. |
| NFA06 | Performance | Die App lädt Transaktionslisten unter 1 Sekunde (max. 100 Transaktionen pro Monat). |

---

## 6 Datenbankschema

### 6.1 Tabellenübersicht

| Tabellenname | Spaltenname | Datentyp | PK / FK | Bemerkung |
|--------------|------------|----------|---------|-----------|
| benutzer | id | INTEGER | PK | Auto-Increment |
| benutzer | username | VARCHAR(255) | | NOT NULL, UNIQUE |
| benutzer | email | VARCHAR(255) | | NOT NULL, UNIQUE |
| benutzer | passwort | VARCHAR(255) | | NOT NULL |
| benutzer | gesperrt | INTEGER | | DEFAULT 0 (0=aktiv, 1=gesperrt) |
| benutzer | erstellt_am | VARCHAR(255) | | DEFAULT now() |
| kategorie | id | INTEGER | PK | Auto-Increment |
| kategorie | name | VARCHAR(255) | | z. B. Essen, Freizeit |
| kategorie | benutzer_id | INTEGER | FK → benutzer.id | NULL = Systemkategorie |
| transaktion | id | INTEGER | PK | Auto-Increment |
| transaktion | benutzer_id | INTEGER | FK → benutzer.id | NOT NULL |
| transaktion | kategorie_id | INTEGER | FK → kategorie.id | NOT NULL |
| transaktion | betrag | INTEGER | | NOT NULL, **in Cent** (Positiv = Einnahme, Negativ = Ausgabe) |
| transaktion | notiz | VARCHAR(255) | | Optional |
| transaktion | datum | VARCHAR(10) | | NOT NULL, Format: YYYY-MM-DD |
| transaktion | erstellt_am | VARCHAR(255) | | DEFAULT now() |
| budget_limit | id | INTEGER | PK | Auto-Increment |
| budget_limit | benutzer_id | INTEGER | FK → benutzer.id | NOT NULL |
| budget_limit | kategorie_id | INTEGER | FK → kategorie.id | NOT NULL |
| budget_limit | monat | VARCHAR(7) | | Format: YYYY-MM |
| budget_limit | limit_betrag | INTEGER | | NOT NULL, **in Cent** |

### 6.2 Beziehungen (ER-Diagramm)

```
┌─────────────┐
│   benutzer  │
│ (id, ...)   │
└──────┬──────┘
       │
    1:N├─────────────┬────────────────┬─────────────┐
       │             │                │             │
       │         1:N │            1:N │         1:N │
    ┌──▼────────┐ ┌──▼──────────┐ ┌──▼────────┐ ┌──▼─────────┐
    │ kategorie │ │ transaktion │ │ kategorie │ │budget_limit│
    │(id, name) │ │ (id, ...)   │ │(User-Kat) │ │(id, ...)   │
    └───────────┘ └─────────────┘ └───────────┘ └────────────┘
         ▲              ▲              ▲              ▲
         │              │              │              │
         └──────────────┴──────────────┴──────────────┘
         (1:N Beziehung zu benutzer)
```

---

## 7 Projektumfang – MVP (Minimal Viable Product)

### 🎯 Muss bis zum Ende fertig sein (4h im Unterricht + Heimarbeit):
- ✅ **FA01**: Registrierung und Login
- ✅ **FA02, FA03**: Transaktion erfassen, bearbeiten, löschen
- ✅ **FA04**: Automatischer Kontostand
- ✅ **FA06** (ohne Diagramm): Monatsübersicht als Liste

### ⏱️ Wenn noch Zeit bleibt (Stretch Goals):
- **FA06** mit Kreisdiagramm
- **FA05** Budgetlimit mit 80 %-/100 %-Warnung
- **FA07** Filtern und Sortieren

### 🚫 Nicht im Projektumfang:
- FA08: Admin-Funktionen
- FA09: Passwort ändern
- KI-Spar-Tipps (gestrichen per Lehrer-Feedback)

---

## 8 Entwicklungsreihenfolge

### Sprint 1: Datenbank + Auth (Nächste Stunde)
1. [ ] DB-Schema mit allen 4 Tabellen anlegen
2. [ ] Register-/Login-Route testen
3. [ ] Session-Management überprüfen

### Sprint 2: Transaktionen (CRUD)
1. [ ] Transaktion erfassen (Create)
2. [ ] Transaktion anzeigen (Read)
3. [ ] Transaktion bearbeiten (Update)
4. [ ] Transaktion löschen (Delete)
5. [ ] Kontostand berechnen (FA04)

### Sprint 3: Monatsübersicht
1. [ ] Transaktionen nach Monat filtern
2. [ ] Tabelle mit Transaktionsübersicht anzeigen
3. [ ] Kategorien anzeigen

### Sprint 4+: Diagramme & Limits (Optional)
1. [ ] Kreisdiagramm mit Chart.js
2. [ ] Budgetlimit-Verwaltung
3. [ ] Warnungen bei 80 % und 100 %

---

## 9 Korrektionen vom Lehrer ✅

| Problem | Lösung |
|---------|--------|
| KI-Tipps in Ziel, aber nicht in FA | **Gestrichen** (nicht im MVP) |
| NFA-Nummerierung springt | **Korrigiert**: NFA04 → NFA05 → NFA06 |
| Geldbeträge als FLOAT | **Korrigiert**: INTEGER in Cent |
| Datum sagt 2025 | **Korrigiert**: 2025/26 |

