# ============================================================
# Phase 2 — DATABASE DEVELOPER's File
# Branch: database
# File: database.py
# Handles: Schema creation, all SQL queries (insert/select/delete/search)
# ============================================================

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")


# ── Connection helper ──────────────────────────────────────
def get_connection():
    """Return a Row-factory connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row   # rows behave like dicts
    return conn


# ── Schema setup ──────────────────────────────────────────
def init_db():
    """
    Create the contacts table if it does not exist.
    Called once at app startup (from app.py).

    Schema:
        id      INTEGER  PRIMARY KEY AUTOINCREMENT
        name    TEXT     NOT NULL
        phone   TEXT     NOT NULL
        email   TEXT
        address TEXT
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            name    TEXT    NOT NULL,
            phone   TEXT    NOT NULL,
            email   TEXT    DEFAULT '',
            address TEXT    DEFAULT ''
        )
    """)

    conn.commit()
    conn.close()
    print("[DB] Table 'contacts' ready.")


# ── INSERT ─────────────────────────────────────────────────
def insert_contact(name, phone, email="", address=""):
    """
    Insert a new contact row.
    Returns the new row's id.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO contacts (name, phone, email, address) VALUES (?, ?, ?, ?)",
        (name.strip(), phone.strip(), email.strip(), address.strip())
    )

    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return new_id


# ── SELECT ALL ─────────────────────────────────────────────
def get_all_contacts():
    """
    Return all contacts ordered alphabetically by name.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM contacts ORDER BY name ASC")
    rows = cursor.fetchall()

    conn.close()
    return rows


# ── SELECT ONE ─────────────────────────────────────────────
def get_contact_by_id(contact_id):
    """
    Return a single contact by primary key.
    Returns None if not found.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM contacts WHERE id = ?", (contact_id,))
    row = cursor.fetchone()

    conn.close()
    return row


# ── COUNT ─────────────────────────────────────────────────
def count_contacts():
    """Return total number of contacts stored."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM contacts")
    total = cursor.fetchone()[0]

    conn.close()
    return total


# ── SEARCH ────────────────────────────────────────────────
def search_contacts(query):
    """
    Search contacts where name OR phone contains the query string.
    Case-insensitive via SQLite LIKE.
    Returns a list of matching rows.
    """
    conn = get_connection()
    cursor = conn.cursor()

    like_query = f"%{query.strip()}%"
    cursor.execute(
        """
        SELECT * FROM contacts
        WHERE name  LIKE ?
           OR phone LIKE ?
        ORDER BY name ASC
        """,
        (like_query, like_query)
    )
    rows = cursor.fetchall()

    conn.close()
    return rows


# ── DELETE ────────────────────────────────────────────────
def delete_contact(contact_id):
    """
    Delete a contact by id.
    Returns True if a row was deleted, False if id not found.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
    deleted = cursor.rowcount > 0

    conn.commit()
    conn.close()
    return deleted


# ── Quick self-test (run: python database.py) ─────────────
if __name__ == "__main__":
    init_db()
    print("[TEST] Inserting sample contacts...")
    insert_contact("Alice Johnson", "9876543210", "alice@email.com", "123 Main St")
    insert_contact("Bob Smith",    "8765432109", "bob@email.com",   "456 Oak Ave")
    insert_contact("Carol Davis",  "7654321098", "carol@email.com", "789 Pine Rd")

    print(f"[TEST] Total contacts: {count_contacts()}")

    print("[TEST] All contacts:")
    for c in get_all_contacts():
        print(f"  {c['id']}. {c['name']} — {c['phone']}")

    print("[TEST] Search 'alice':", [c['name'] for c in search_contacts("alice")])

    print("[TEST] Delete id=1:", delete_contact(1))
    print(f"[TEST] Total after delete: {count_contacts()}")
