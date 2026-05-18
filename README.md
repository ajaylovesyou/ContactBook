# 📒 Contact Book — Team Project

A full-stack web application built with **Flask + SQLite + Vanilla JS**.

---

## 🚀 Quick Start

```bash
# 1. Clone the repo
git clone <your-repo-url>
cd contact-book

# 2. Install Flask
pip install flask
# or: pip install -r requirements.txt

# 3. Run the app
python app.py

# 4. Open browser
# http://localhost:5000
```

---

## 📁 Project Structure

```
contact-book/
├── app.py            ← Backend: Flask routes (backend branch)
├── database.py       ← Database: SQLite queries  (database branch)
├── database.db       ← SQLite file (auto-created on first run)
├── requirements.txt  ← Python dependencies
├── git_setup.sh      ← One-time Git branch setup script
├── templates/
│   ├── index.html    ← Home page
│   ├── contacts.html ← All contacts (card grid)
│   ├── add.html      ← Add contact form
│   ├── search.html   ← Search page
│   └── detail.html   ← Single contact view
└── static/
    ├── css/
    │   └── style.css ← All styles (frontend branch)
    └── js/
        └── main.js   ← JS interactions (frontend branch)
```

---

## 🧑‍💻 Team Responsibilities

| Role | Branch | Files |
|---|---|---|
| Frontend Developer | `frontend` | `templates/*.html`, `static/css/style.css`, `static/js/main.js` |
| Backend Developer | `backend` | `app.py` |
| Database Developer | `database` | `database.py` |

---

## 🌿 Git Workflow

```bash
# Each member works on their own branch
git checkout frontend   # frontend dev
git checkout backend    # backend dev
git checkout database   # database dev

# Save your work
git add .
git commit -m "feat: add responsive navbar"

# Merge into main when done
git checkout main
git merge frontend
git merge backend
git merge database
```

**Commit message convention:**
- `feat:` — new feature
- `fix:` — bug fix
- `style:` — CSS/layout changes
- `db:` — database changes
- `docs:` — documentation

---

## 🗺️ Pages & Routes

| Page | URL | Method |
|---|---|---|
| Home | `/` | GET |
| All Contacts | `/contacts` | GET |
| Add Contact | `/add` | GET, POST |
| Search | `/search?q=<query>` | GET |
| Contact Detail | `/contact/<id>` | GET |
| Delete | `/delete/<id>` | POST |
| API Search | `/api/search?q=<query>` | GET (JSON) |

---

## 🗄️ Database Schema

```sql
CREATE TABLE contacts (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    name    TEXT    NOT NULL,
    phone   TEXT    NOT NULL,
    email   TEXT    DEFAULT '',
    address TEXT    DEFAULT ''
);
```

---

## ⚙️ Tech Stack

- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Backend**: Python 3, Flask
- **Database**: SQLite (built into Python — no installation needed)
- **Fonts**: Playfair Display, DM Sans (Google Fonts)

---

## ✅ Features Checklist

- [x] Home page with total contact count
- [x] All contacts in card layout
- [x] Add contact form with validation
- [x] Search by name or phone
- [x] Contact detail page
- [x] Delete with confirmation dialog
- [x] Responsive design (mobile friendly)
- [x] Flash messages (success / error)
- [x] Live client-side filter on contacts page
- [x] Animated cards
- [x] REST API endpoint `/api/search`

---

## 🐛 Phase 6 — Testing Checklist

Run through these before merging all branches:

1. **Add** — Add a contact with all fields → confirm redirect to detail page
2. **Add validation** — Submit empty form → error flash message shown
3. **All Contacts** — Visit `/contacts` → see card grid
4. **Live filter** — Type in filter box → cards hide/show without page reload
5. **Search** — Search by name → results appear; search by phone → results appear
6. **Search empty** — Search for "xyz" → "No results" message shown
7. **Detail** — Click "View" on a card → full details shown
8. **Delete** — Click "Delete" → confirm dialog appears → cancel → contact still exists
9. **Delete confirm** — Click Delete → confirm → contact removed → success flash
10. **Mobile** — Resize to 375px → hamburger menu works, layout adapts
11. **Flash dismiss** — Flash messages auto-dismiss after 4 seconds
