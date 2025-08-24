from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)
app.config["DATABASE"] = "notes.db"  # default database

# Initialize DB
def init_db():
    conn = sqlite3.connect(app.config["DATABASE"])
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS notes(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Home page - list notes
@app.route("/")
def index():
    conn = sqlite3.connect(app.config["DATABASE"])
    c = conn.cursor()
    c.execute("SELECT * FROM notes")
    notes = c.fetchall()
    conn.close()
    return render_template("index.html", notes=notes)

# Add note
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        content = request.form["content"]
        conn = sqlite3.connect(app.config["DATABASE"])
        c = conn.cursor()
        c.execute("INSERT INTO notes (content) VALUES (?)", (content,))
        conn.commit()
        conn.close()
        return redirect("/")
    return render_template("add.html")

# Delete note
@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect(app.config["DATABASE"])
    c = conn.cursor()
    c.execute("DELETE FROM notes WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
