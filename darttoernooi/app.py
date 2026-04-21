from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "123"  # kies zelf iets

# Database maken
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS deelnemers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            naam TEXT NOT NULL,
            bijnaam TEXT,
            lied TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Home (formulier)
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        naam = request.form["naam"]
        bijnaam = request.form["bijnaam"]
        lied = request.form["lied"]

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("INSERT INTO deelnemers (naam, bijnaam, lied) VALUES (?, ?, ?)",
                  (naam, bijnaam, lied))
        conn.commit()
        conn.close()

        return redirect("/deelnemers")

    return render_template("index.html")

# Overzicht
@app.route("/deelnemers")
def deelnemers():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM deelnemers")
    data = c.fetchall()
    conn.close()

    return render_template("deelnemers.html", deelnemers=data)

@app.route("/delete/<int:id>")
def delete(id):
    import sqlite3
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("DELETE FROM deelnemers WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/deelnemers")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        wachtwoord = request.form["wachtwoord"]

        if wachtwoord == "admin123":  # kies je eigen wachtwoord!
            session["admin"] = True
            return redirect("/deelnemers")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect("/")




if __name__ == "__main__":
    app.run(debug=True)