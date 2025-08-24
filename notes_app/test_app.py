import os
import sqlite3
import pytest
from app import app, init_db

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["DATABASE"] = "notes_test.db"

    # Remove test DB if exists
    if os.path.exists(app.config["DATABASE"]):
        os.remove(app.config["DATABASE"])
    init_db()  # create fresh test DB

    with app.test_client() as client:
        yield client

    # Cleanup test DB
    if os.path.exists(app.config["DATABASE"]):
        os.remove(app.config["DATABASE"])

# Test homepage
def test_homepage_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    # adjust according to your template
    assert b"My Notes" in response.data or b"notes" in response.data

# Test adding note
def test_add_note(client):
    response = client.post("/add", data={"content": "Test Note"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Test Note" in response.data

# Test delete note
def test_delete_note(client):
    # Add note to delete
    client.post("/add", data={"content": "Delete Me"}, follow_redirects=True)

    conn = sqlite3.connect("notes_test.db")
    c = conn.cursor()
    c.execute("SELECT id FROM notes WHERE content=?", ("Delete Me",))
    note_id = c.fetchone()[0]
    conn.close()

    response = client.get(f"/delete/{note_id}", follow_redirects=True)
    assert response.status_code == 200
    assert b"Delete Me" not in response.data
