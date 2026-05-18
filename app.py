# ============================================================
# Phase 3 — BACKEND DEVELOPER's File
# Branch: backend
# File: app.py
# Handles: Flask routes, form processing, connecting frontend ↔ database
# ============================================================

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from database import (
    init_db,
    insert_contact,
    get_all_contacts,
    get_contact_by_id,
    count_contacts,
    search_contacts,
    delete_contact,
)

app = Flask(__name__)
app.secret_key = "contactbook_secret_2024"   # needed for flash messages


# ── Initialise DB on first run ─────────────────────────────
with app.app_context():
    init_db()


# ============================================================
# ROUTE 1 — Home Page
# URL  : /
# Shows: Landing page with total contacts count
# ============================================================
@app.route("/")
def index():
    total = count_contacts()
    return render_template("index.html", total=total)


# ============================================================
# ROUTE 2 — All Contacts Page
# URL  : /contacts
# Shows: All contacts in card layout
# ============================================================
@app.route("/contacts")
def contacts():
    all_contacts = get_all_contacts()
    return render_template("contacts.html", contacts=all_contacts)


# ============================================================
# ROUTE 3 — Add Contact Page
# URL  : /add          (GET  → show form)
# URL  : /add          (POST → process form, save to DB)
# ============================================================
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        name    = request.form.get("name",    "").strip()
        phone   = request.form.get("phone",   "").strip()
        email   = request.form.get("email",   "").strip()
        address = request.form.get("address", "").strip()

        # ── Basic validation ──────────────────────────────
        errors = []
        if not name:
            errors.append("Name is required.")
        if not phone:
            errors.append("Phone number is required.")
        elif not phone.replace("+", "").replace("-", "").replace(" ", "").isdigit():
            errors.append("Phone must contain only digits (+ - spaces allowed).")

        if errors:
            for err in errors:
                flash(err, "error")
            # Re-render form with the values the user already typed
            return render_template("add.html",
                                   prefill={"name": name, "phone": phone,
                                            "email": email, "address": address})

        new_id = insert_contact(name, phone, email, address)
        flash(f"Contact '{name}' added successfully!", "success")
        return redirect(url_for("detail", contact_id=new_id))

    # GET — empty form
    return render_template("add.html", prefill={})


# ============================================================
# ROUTE 4 — Search Page
# URL  : /search                (GET  → empty search page)
# URL  : /search?q=<query>      (GET  → results)
# ============================================================
@app.route("/search")
def search():
    query   = request.args.get("q", "").strip()
    results = []
    searched = False

    if query:
        results  = search_contacts(query)
        searched = True

    return render_template("search.html",
                           query=query,
                           results=results,
                           searched=searched)


# ============================================================
# ROUTE 5 — Contact Detail Page
# URL  : /contact/<id>
# Shows: Full information for one contact
# ============================================================
@app.route("/contact/<int:contact_id>")
def detail(contact_id):
    contact = get_contact_by_id(contact_id)
    if contact is None:
        flash("Contact not found.", "error")
        return redirect(url_for("contacts"))
    return render_template("detail.html", contact=contact)


# ============================================================
# ROUTE 6 — Delete Contact
# URL  : /delete/<id>   (POST only — triggered by JS confirm)
# ============================================================
@app.route("/delete/<int:contact_id>", methods=["POST"])
def delete(contact_id):
    contact = get_contact_by_id(contact_id)
    if contact:
        name = contact["name"]
        delete_contact(contact_id)
        flash(f"Contact '{name}' has been deleted.", "success")
    else:
        flash("Contact not found.", "error")
    return redirect(url_for("contacts"))


# ============================================================
# ROUTE 7 — API: Live search (used by JS fetch in search page)
# URL  : /api/search?q=<query>
# Returns: JSON list of matching contacts
# ============================================================
@app.route("/api/search")
def api_search():
    query = request.args.get("q", "").strip()
    if not query:
        return jsonify([])
    rows = search_contacts(query)
    # sqlite3.Row → plain dict for JSON serialisation
    results = [dict(row) for row in rows]
    return jsonify(results)


# ============================================================
# Run the app
# ============================================================
if __name__ == "__main__":
    print("=" * 50)
    print("  Contact Book App — running at http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, port=5000)
 