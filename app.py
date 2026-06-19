# ============================================================
#  BudgetBuddy  |  HTL Reutte – 3H – 2025/26
#  Datenbankanwendungen – Projektarbeit
# ============================================================

from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import os
import bcrypt
from datetime import date, timedelta

app = Flask(__name__)

app.secret_key = "aender_mich_bitte_vor_abgabe"
app.permanent_session_lifetime = timedelta(minutes=30)

DB_PFAD = os.path.join(os.path.dirname(__file__), "budgetbuddy.db")


def get_db():
    con = sqlite3.connect(DB_PFAD)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    return con


def db_init():
    with open(os.path.join(os.path.dirname(__file__), "schema.sql"), encoding="utf-8") as f:
        sql = f.read()
    con = get_db()
    con.executescript(sql)
    con.commit()
    con.close()
    print("Datenbank erfolgreich initialisiert.")


def eingeloggt():
    return "benutzer_id" in session


@app.route("/")
def index():
    if not eingeloggt():
        return render_template("index.html")

    con = get_db()
    row = con.execute(
        "SELECT COALESCE(SUM(betrag), 0) AS summe FROM transaktion WHERE benutzer_id = ?",
        (session["benutzer_id"],)
    ).fetchone()
    con.close()

    return render_template("index.html", kontostand=row["summe"])


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        passwort = request.form.get("passwort", "")

        if not username or not email or not passwort:
            flash("Bitte alle Felder ausfüllen.", "fehler")
            return render_template("register.html")

        if len(passwort) < 8:
            flash("Das Passwort muss mindestens 8 Zeichen lang sein.", "fehler")
            return render_template("register.html")

        con = get_db()
        existiert = con.execute(
            "SELECT id FROM benutzer WHERE username = ? OR email = ?",
            (username, email)
        ).fetchone()

        if existiert:
            con.close()
            flash("Benutzername oder E-Mail bereits vergeben.", "fehler")
            return render_template("register.html")

        passwort_hash = bcrypt.hashpw(passwort.encode("utf-8"), bcrypt.gensalt(rounds=10))

        cur = con.execute(
            "INSERT INTO benutzer (username, email, passwort) VALUES (?, ?, ?)",
            (username, email, passwort_hash.decode("utf-8"))
        )
        con.commit()
        neuer_benutzer_id = cur.lastrowid
        con.close()

        session.permanent = True
        session["benutzer_id"] = neuer_benutzer_id
        session["username"] = username

        flash("Konto erfolgreich erstellt. Willkommen bei BudgetBuddy!", "erfolg")
        return redirect(url_for("index"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        passwort = request.form.get("passwort", "")

        if not username or not passwort:
            flash("Bitte Benutzername und Passwort eingeben.", "fehler")
            return render_template("login.html")

        con = get_db()
        benutzer = con.execute(
            "SELECT * FROM benutzer WHERE username = ?", (username,)
        ).fetchone()
        con.close()

        if benutzer is None or not bcrypt.checkpw(
            passwort.encode("utf-8"), benutzer["passwort"].encode("utf-8")
        ):
            flash("Benutzername oder Passwort ist falsch.", "fehler")
            return render_template("login.html")

        if benutzer["gesperrt"]:
            flash("Dieses Konto wurde gesperrt. Bitte wende dich an einen Administrator.", "fehler")
            return render_template("login.html")

        session.permanent = True
        session["benutzer_id"] = benutzer["id"]
        session["username"] = benutzer["username"]

        flash(f"Willkommen zurück, {benutzer['username']}!", "erfolg")
        return redirect(url_for("index"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Du wurdest erfolgreich ausgeloggt.", "erfolg")
    return redirect(url_for("index"))


@app.route("/liste")
def liste():
    if not eingeloggt():
        flash("Bitte zuerst einloggen.", "fehler")
        return redirect(url_for("login"))

    con = get_db()
    transaktionen = con.execute("""
        SELECT t.id, t.betrag, t.notiz, t.datum, k.name AS kategorie_name
        FROM transaktion t
        JOIN kategorie k ON t.kategorie_id = k.id
        WHERE t.benutzer_id = ?
        ORDER BY t.datum DESC, t.id DESC
    """, (session["benutzer_id"],)).fetchall()
    con.close()

    return render_template("liste.html", transaktionen=transaktionen)


@app.route("/neu", methods=["GET", "POST"])
def neu():
    if not eingeloggt():
        flash("Bitte zuerst einloggen.", "fehler")
        return redirect(url_for("login"))

    con = get_db()
    kategorien = con.execute(
        "SELECT * FROM kategorie WHERE benutzer_id IS NULL OR benutzer_id = ? ORDER BY name",
        (session["benutzer_id"],)
    ).fetchall()

    if request.method == "POST":
        typ = request.form.get("typ", "")
        betrag_text = request.form.get("betrag", "").strip()
        kategorie_id = request.form.get("kategorie_id", "")
        datum = request.form.get("datum", "").strip()
        notiz = request.form.get("notiz", "").strip()

        fehler = None
        try:
            betrag_euro = float(betrag_text.replace(",", "."))
            if betrag_euro <= 0:
                fehler = "Der Betrag muss größer als 0 sein."
        except ValueError:
            fehler = "Bitte einen gültigen Betrag eingeben."

        if not kategorie_id:
            fehler = "Bitte eine Kategorie auswählen."
        if not datum:
            fehler = "Bitte ein Datum auswählen."
        if typ not in ("einnahme", "ausgabe"):
            fehler = "Ungültiger Typ."

        if fehler:
            con.close()
            flash(fehler, "fehler")
            return render_template("formular.html", modus="neu", eintrag=None, kategorien=kategorien)

        betrag_cent = round(betrag_euro * 100)
        if typ == "ausgabe":
            betrag_cent = -betrag_cent

        con.execute(
            "INSERT INTO transaktion (benutzer_id, kategorie_id, betrag, notiz, datum) VALUES (?, ?, ?, ?, ?)",
            (session["benutzer_id"], kategorie_id, betrag_cent, notiz or None, datum)
        )
        con.commit()
        con.close()

        flash("Transaktion erfolgreich gespeichert.", "erfolg")
        return redirect(url_for("liste"))

    con.close()
    return render_template("formular.html", modus="neu", eintrag=None, kategorien=kategorien)


@app.route("/bearbeiten/<int:eintrag_id>", methods=["GET", "POST"])
def bearbeiten(eintrag_id):
    if not eingeloggt():
        flash("Bitte zuerst einloggen.", "fehler")
        return redirect(url_for("login"))

    con = get_db()

    eintrag = con.execute(
        "SELECT * FROM transaktion WHERE id = ? AND benutzer_id = ?",
        (eintrag_id, session["benutzer_id"])
    ).fetchone()

    if eintrag is None:
        con.close()
        flash("Transaktion nicht gefunden.", "fehler")
        return redirect(url_for("liste"))

    kategorien = con.execute(
        "SELECT * FROM kategorie WHERE benutzer_id IS NULL OR benutzer_id = ? ORDER BY name",
        (session["benutzer_id"],)
    ).fetchall()

    if request.method == "POST":
        typ = request.form.get("typ", "")
        betrag_text = request.form.get("betrag", "").strip()
        kategorie_id = request.form.get("kategorie_id", "")
        datum = request.form.get("datum", "").strip()
        notiz = request.form.get("notiz", "").strip()

        fehler = None
        try:
            betrag_euro = float(betrag_text.replace(",", "."))
            if betrag_euro <= 0:
                fehler = "Der Betrag muss größer als 0 sein."
        except ValueError:
            fehler = "Bitte einen gültigen Betrag eingeben."

        if not kategorie_id:
            fehler = "Bitte eine Kategorie auswählen."
        if not datum:
            fehler = "Bitte ein Datum auswählen."

        if fehler:
            con.close()
            flash(fehler, "fehler")
            return render_template("formular.html", modus="bearbeiten", eintrag=eintrag, kategorien=kategorien)

        betrag_cent = round(betrag_euro * 100)
        if typ == "ausgabe":
            betrag_cent = -betrag_cent

        con.execute(
            "UPDATE transaktion SET kategorie_id = ?, betrag = ?, notiz = ?, datum = ? WHERE id = ? AND benutzer_id = ?",
            (kategorie_id, betrag_cent, notiz or None, datum, eintrag_id, session["benutzer_id"])
        )
        con.commit()
        con.close()

        flash("Transaktion erfolgreich aktualisiert.", "erfolg")
        return redirect(url_for("liste"))

    con.close()
    return render_template("formular.html", modus="bearbeiten", eintrag=eintrag, kategorien=kategorien)


@app.route("/loeschen/<int:eintrag_id>", methods=["POST"])
def loeschen(eintrag_id):
    if not eingeloggt():
        flash("Bitte zuerst einloggen.", "fehler")
        return redirect(url_for("login"))

    con = get_db()
    con.execute(
        "DELETE FROM transaktion WHERE id = ? AND benutzer_id = ?",
        (eintrag_id, session["benutzer_id"])
    )
    con.commit()
    con.close()

    flash("Transaktion gelöscht.", "erfolg")
    return redirect(url_for("liste"))


@app.route("/detail/<int:eintrag_id>")
def detail(eintrag_id):
    if not eingeloggt():
        flash("Bitte zuerst einloggen.", "fehler")
        return redirect(url_for("login"))

    con = get_db()
    transaktion = con.execute("""
        SELECT t.id, t.betrag, t.notiz, t.datum, t.kategorie_id, k.name AS kategorie_name
        FROM transaktion t
        JOIN kategorie k ON t.kategorie_id = k.id
        WHERE t.id = ? AND t.benutzer_id = ?
    """, (eintrag_id, session["benutzer_id"])).fetchone()
    con.close()

    if transaktion is None:
        flash("Transaktion nicht gefunden.", "fehler")
        return redirect(url_for("liste"))

    return render_template("detail.html", transaktion=transaktion)


if __name__ == "__main__":
    app.run(debug=True)