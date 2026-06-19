# Entwicklungsplan – BudgetBuddy MVP

**Stand**: 19.06.2026 | **Status**: Bereit für Sprint 1

---

## 📋 Projektstruktur

```
✅ Schema ist vorhanden (schema.sql)
✅ App-Grundgerüst vorhanden (app.py)
✅ Templates vorhanden (base.html, index.html, liste.html, formular.html, detail.html)
✅ CSS vorhanden (style.css)
```

---

## 🚀 Sprint 1: Initiales Setup + Login/Register (TODAY)

### Aufgaben:
- [ ] **Terminal**: `pip install -r requirements.txt`
- [ ] **Terminal**: `python -c "from app import db_init; db_init()"`
  - Initialisiert die Datenbank mit `schema.sql`
  - Erstellt alle 4 Tabellen
  - Fügt Systemkategorien ein
- [ ] **Terminal**: `python app.py`
  - App startet auf `http://127.0.0.1:5000`
- [ ] **Browser**: `http://127.0.0.1:5000` aufrufen
- [ ] **Testen**: Register-Funktion
  - Neues Konto anlegen
  - Passwort muss mind. 8 Zeichen lang sein
  - Benutzer sollte automatisch eingeloggt sein
- [ ] **Testen**: Login-Funktion
  - Mit neuen Anmeldedaten anmelden
  - Mit falschen Daten Fehler testen
- [ ] **Testen**: Logout
  - Link klicken → zurück zur Startseite

### ✅ Kriterien für "Sprint 1 DONE":
- Registrierung funktioniert
- Login/Logout funktioniert
- Kontostand wird auf Dashboard angezeigt
- Passwörter werden gehasht (check: `budgetbuddy.db` in DB-Browser)

---

## 🎯 Sprint 2: Transaktionen (CRUD)

### Aufgaben:
- [ ] **Neue Transaktion** (Formular)
  - Typ: Einnahme / Ausgabe wählen
  - Betrag eingeben (wird zu Cent konvertiert)
  - Kategorie wählen
  - Datum wählen
  - Notiz eintragen (optional)
  - → Speichern
- [ ] **Transaktionen anzeigen** (Liste)
  - Alle Transaktionen des aktuellen Benutzers
  - Sortiert nach Datum (neueste zuerst)
  - Kategorie anzeigen
  - Betrag farbig: grün (+) / rot (-)
- [ ] **Transaktion bearbeiten**
  - Auf "Detail" oder "Bearbeiten" klicken
  - Alle Felder können geändert werden
  - Speichern
- [ ] **Transaktion löschen**
  - Sicherheitsabfrage: "Wirklich löschen?"
  - Erfolgs-/Fehlermeldung zeigen
- [ ] **Kontostand berechnen** (FA04)
  - Summe aller Transaktionen (positive - negative)
  - Auf Dashboard anzeigen

### ✅ Kriterien für "Sprint 2 DONE":
- Du kannst ≥ 5 Transaktionen erfassen
- Die Transaktionen erscheinen in der Liste
- Einnahme und Ausgabe unterscheiden sich (farblich, Vorzeichen)
- Du kannst Transaktionen bearbeiten und löschen
- Kontostand aktualisiert sich automatisch

---

## 📊 Sprint 3: Monatsübersicht (MVP-Finale)

### Aufgaben:
- [ ] **Monat-Filter hinzufügen**
  - Optionale Dropdown oder Datumsbereich
  - "Aktueller Monat" als default
- [ ] **Filterung in der Liste**
  - SQL: `WHERE strftime('%Y-%m', datum) = ?`
- [ ] **Gesamtsumme pro Monat anzeigen**
  - Summe aller Ausgaben
  - Summe aller Einnahmen
  - Netto (Einnahmen - Ausgaben)

### ✅ Kriterien für "Sprint 3 DONE":
- Monatsübersicht funktioniert
- Die Liste zeigt nur Transaktionen des aktuellen Monats
- Summen werden korrekt berechnet

---

## 🌈 Sprint 4+: Stretch Goals (Optional)

### Wenn Zeit bleibt:
1. **Kreisdiagramm** (FA06)
   - Chart.js Library einbinden
   - Ausgaben nach Kategorien
   - Im Monat darstellen
   
2. **Budgetlimit** (FA05)
   - Neue Route: `/limit`
   - Limit pro Kategorie setzen
   - Warnung bei 80 % / 100 %
   
3. **Filtern & Sortieren** (FA07)
   - Nach Kategorie filtern
   - Nach Betrag sortieren
   - Nach Datum sortieren

---

## 🔧 Häufige Probleme & Lösungen

### Problem: "Datenbank nicht initialisiert"
```bash
python -c "from app import db_init; db_init()"
```

### Problem: "Module nicht gefunden" (ImportError)
```bash
pip install -r requirements.txt
```

### Problem: "Port 5000 wird bereits verwendet"
```bash
# Entweder:
# 1. App beenden (Ctrl+C)
# 2. Oder anderen Port nutzen: python app.py --port 5001
```

### Problem: "Formular wird nicht abgesendet"
- Überprüfe: `name`-Attribute im HTML
- Diese müssen mit `request.form.get("name")` im Python übereinstimmen
- Beispiel: `<input name="betrag">` → `request.form.get("betrag")`

### Problem: "Transaktionen erscheinen nicht in der Liste"
- Überprüfe: Bist du eingeloggt?
- Überprüfe: Wurde die Transaktion gespeichert? (Check: DB-Browser)
- Überprüfe: Die `kategorie_id` existiert wirklich?

---

## 📝 Checkliste für die Abgabe

### Code:
- [ ] Alle SQL-Abfragen verwenden `?`-Platzhalter
- [ ] Keine Passwörter im Klartext gespeichert
- [ ] Sessions funktionieren (30 Min Timeout)
- [ ] Eingaben werden validiert (serverseitig!)
- [ ] Fehlermeldungen auf Deutsch

### Dokumentation:
- [ ] `ANFORDERUNGSANALYSE.md` aktuell
- [ ] `README.md` mit Startanleitung
- [ ] Code kommentiert (besonders komplizierte Stellen)

### Testing:
- [ ] Register/Login funktioniert
- [ ] Transaktionen CRUD funktioniert
- [ ] Kontostand berechnet sich richtig
- [ ] Monatsübersicht funktioniert
- [ ] Mit mehreren Benutzern getestet
- [ ] Mit ungültigen Eingaben getestet

### Performance:
- [ ] App lädt schnell (< 1 Sek)
- [ ] Keine Fehler in der Browser-Konsole (F12)

---

## 💡 Tipps

**Git-Workflow:**
```bash
# Vor jeder neuen Feature:
git add .
git commit -m "Feature: Transaktionen CRUD hinzugefügt"

# Vor Abgabe:
git push origin main
```

**Debugging:**
- Nutze `print()` für Debug-Ausgaben
- Überprüfe die Server-Logs (Terminal)
- Öffne Browser Developer Tools (F12)
- Nutze einen DB-Browser um die Daten direkt zu sehen

**Code-Qualität:**
- Verwende `snake_case` für Variablen (nicht camelCase)
- Gruppiere verwandte SQL-Abfragen
- Schreibe kurze, aussagekräftige Fehlermeldungen

