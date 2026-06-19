# Flask Webapp Baukasten – HTL Reutte 3H

Dieses Starter-Template enthält alles was du für dein Datenbankprojekt brauchst.

## Schnellstart

```bash
# 1. Pakete installieren
pip install -r requirements.txt

# 2. Datenbank erstellen (einmalig)
python -c "from app import db_init; db_init()"

# 3. App starten
python app.py
```

Dann Browser öffnen: **http://127.0.0.1:5000**

---

## Was du anpassen musst

Suche nach `# TODO` in allen Dateien – dort steht genau was du ändern sollst.

| Datei | Was anpassen |
|-------|-------------|
| `schema.sql` | Tabellennamen, Spalten für dein Projekt |
| `app.py` | Tabellennamen in den SQL-Queries, Feldnamen |
| `templates/base.html` | Projektnamen in Navigation und Titel |
| `templates/index.html` | Willkommenstext, Karten |
| `templates/liste.html` | **komplett selbst schreiben** (Anleitung im Quelltext) |
| `templates/formular.html` | **komplett selbst schreiben** (Anleitung im Quelltext) |
| `templates/detail.html` | **komplett selbst schreiben** (Anleitung im Quelltext) |
| `static/style.css` | Farben, Layout (optional) |

---

## Dateistruktur

```
baukasten/
├── app.py              ← Flask-Hauptdatei (Routen, DB-Zugriff)
├── schema.sql          ← Datenbankstruktur (Tabellen)
├── requirements.txt    ← Python-Pakete
├── datenbank.db        ← wird automatisch erstellt
├── templates/
│   ├── base.html       ← Grundlayout (Navigation, Flash)
│   ├── index.html      ← Startseite
│   ├── liste.html      ← Alle Einträge
│   ├── formular.html   ← Neu anlegen / Bearbeiten
│   └── detail.html     ← Detailansicht
└── static/
    └── style.css       ← CSS-Stylesheet
```

---

## Pflichtfeatures für das Projekt

- [ ] Mind. 2 Tabellen in `schema.sql`
- [ ] Alle CRUD-Operationen (Create, Read, Update, Delete)
- [ ] Eingabevalidierung (leere Felder prüfen, Prepared Statements!)
- [ ] Korrigiertes Anforderungsdokument abgegeben

## Bonusfeatures (nicht bewertet, aber möglich)

- [ ] PDF-Export (ReportLab oder WeasyPrint)
- [ ] REST-API (JSON-Routen, siehe Kommentar in `app.py`)
- [ ] Login-System (Flask-Login)

---

## HTML-Seiten selbst schreiben (KI erlaubt!)

`base.html` (Layout, Navigation) und `style.css` sind fertig – die Seiten
`liste.html`, `formular.html` und `detail.html` schreibt ihr selbst.
In jeder Datei steht im Quelltext genau, was die Seite können muss und
welche Variablen ihr von app.py bekommt.

**KI-Hilfe ist dabei ausdrücklich erlaubt.** Aber Achtung:

- Die Variablennamen müssen zu eurem `render_template(...)` passen.
- Die `name`-Attribute im Formular müssen exakt den `request.form.get("...")`-Namen in app.py entsprechen – sonst kommen eure Daten nie in der Datenbank an.
- Bei der Präsentation müsst ihr erklären können, wie ein Datensatz vom Formular bis in die Datenbank kommt. „Das hat die KI gemacht" ist keine Antwort.

---

## Sicherheit – WICHTIG!

**Immer `?`-Platzhalter verwenden!**

```python
# RICHTIG ✅
con.execute("SELECT * FROM eintraege WHERE id = ?", (eintrag_id,))
con.execute("INSERT INTO eintraege (feld1) VALUES (?)", (feld1,))

# FALSCH ❌ – SQL-Injection möglich!
con.execute(f"SELECT * FROM eintraege WHERE id = {eintrag_id}")
con.execute("INSERT INTO eintraege (feld1) VALUES ('" + feld1 + "')")
```
