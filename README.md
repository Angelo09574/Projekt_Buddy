# 🏦 BudgetBuddy – Schnelleinstieg

**Dein Finanz-Tracker für Jugendliche** | HTL Reutte 3H

---

## 🚀 In 3 Minuten starten

### 1️⃣ Abhängigkeiten installieren
```bash
cd /path/to/projekt
pip install -r requirements.txt
```

### 2️⃣ Datenbank initialisieren (einmalig)
```bash
python -c "from app import db_init; db_init()"
```

**Was passiert hier?**
- Erstellt `budgetbuddy.db`
- Legt die 4 Tabellen an: `benutzer`, `kategorie`, `transaktion`, `budget_limit`
- Fügt Standard-Kategorien ein: Essen, Freizeit, Kleidung, Transport, Sonstiges

### 3️⃣ App starten
```bash
python app.py
```

**Output:**
```
WARNING in app.run_simple: This is a development server. Do not use it in production deployments. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
```

### 4️⃣ Browser öffnen
Gehe zu: **http://127.0.0.1:5000**

---

## 📖 Erste Schritte

1. **Registrieren** (Homepage → "Registrieren")
   - Benutzername: beliebig (z.B. `max123`)
   - Email: beliebig (z.B. `max@example.com`)
   - Passwort: mind. 8 Zeichen
   - → Konto wird sofort erstellt

2. **Transaktion erfassen** ("Neu erfassen")
   - **Typ**: Einnahme oder Ausgabe
   - **Betrag**: z.B. `15,50`
   - **Kategorie**: z.B. "Freizeit"
   - **Datum**: heute oder in der Vergangenheit
   - **Notiz**: optional
   - → "Speichern"

3. **Transaktionen ansehen** ("Transaktionen")
   - Alle deine Einnahmen & Ausgaben in einer Liste
   - Bearbeiten oder Löschen möglich
   - Kontostand wird automatisch oben angezeigt

4. **Dashboard** (Home-Link)
   - Dein aktueller Kontostand
   - Links zu den wichtigsten Funktionen

---

## 📁 Projektstruktur

```
baukasten/
├── app.py                    ← Flask-Hauptdatei (alle Routen & DB-Zugriffe)
├── requirements.txt          ← Python-Abhängigkeiten
├── schema.sql               ← Datenbankstruktur
├── budgetbuddy.db           ← Datenbank (wird automatisch erstellt)
│
├── templates/               ← HTML-Seiten
│   ├── base.html           ← Layout-Template (Navigation, Flash)
│   ├── index.html          ← Dashboard / Startseite
│   ├── liste.html          ← Alle Transaktionen
│   ├── formular.html       ← Neue/Bearbeite Transaktion
│   └── detail.html         ← Detail-Ansicht einer Transaktion
│
└── static/
    └── style.css           ← Styling
```

---

## 🔐 Sicherheit

✅ **Was ist bereits implementiert:**
- Passwörter werden mit `bcrypt` gehasht (nicht im Klartext!)
- Alle SQL-Abfragen nutzen `?`-Platzhalter → kein SQL-Injection-Risiko
- Session-Timeout nach 30 Minuten
- Validierung auf Server-Seite
- Benutzer sehen nur ihre eigenen Daten

---

## 🛠️ Troubleshooting

### ❌ ModuleNotFoundError: No module named 'flask'
```bash
pip install -r requirements.txt
```

### ❌ "Unable to open database file"
```bash
# Datenbank noch nicht initialisiert:
python -c "from app import db_init; db_init()"
```

### ❌ Port 5000 wird bereits verwendet
```bash
# Entweder alte App beenden (Ctrl+C im Terminal)
# Oder in app.py die Zeile ändern:
# app.run(debug=True, port=5001)
```

### ❌ "Transaktion wurde nicht gespeichert"
- Überprüfe: War die Eingabe vollständig?
- Überprüfe: Gibt es eine Fehlermeldung? (Rot auf der Seite)
- Debug: Öffne `budgetbuddy.db` mit DB-Browser und schau, ob die Daten dort sind

---

## 📊 Datenbankschema

### benutzer
```sql
id | username | email | passwort (gehasht) | gesperrt | erstellt_am
```

### kategorie
```sql
id | name | benutzer_id (NULL = Systemkategorie)
```

### transaktion
```sql
id | benutzer_id | kategorie_id | betrag (in Cent!) | notiz | datum | erstellt_am
```

### budget_limit
```sql
id | benutzer_id | kategorie_id | monat (YYYY-MM) | limit_betrag
```

**Wichtig**: Beträge sind in **CENT** gespeichert!
- 15,50 € = 1550 (Cent)
- Bei der Anzeige wird durch 100 dividiert

---

## 🎯 MVP-Features (müssen funktionieren)

- ✅ Registrierung & Login
- ✅ Transaktion erfassen (Einnahme/Ausgabe)
- ✅ Transaktionen bearbeiten & löschen
- ✅ Kontostand berechnet sich automatisch
- ✅ Monatsübersicht (als Liste)

---

## 🚀 Stretch-Features (optional)

- Kreisdiagramm mit Chart.js
- Budgetlimit mit Warnungen
- Filtern und Sortieren
- Admin-Panel

---

## 📞 Hilfe & Ressourcen

- **Flask-Dokumentation**: https://flask.palletsprojects.com/
- **SQLite-Dokumentation**: https://www.sqlite.org/docs.html
- **Bcrypt (Passwort-Hashing)**: https://github.com/pyca/bcrypt
- **Jinja2-Templates**: https://jinja.palletsprojects.com/

---

## ✅ Vor der Abgabe

- [ ] Alle Spalten des Schemas testen
- [ ] Mit mehreren Benutzern testen
- [ ] Mit ungültigen Eingaben testen (leere Felder, negative Beträge, etc.)
- [ ] Dokumentation lesen (ANFORDERUNGSANALYSE.md)
- [ ] Git: `git push origin main`

---

**Viel Erfolg! 🎉**

Bei Fragen: Lehrer fragen oder in der Anforderungsanalyse nachlesen.

