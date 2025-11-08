# Multi-Dealership Web App (Flask + Pony ORM)

Web application for a multi-dealership: public site with a car configurator and a reserved area for customers; 
back-office for secretariat and employees.

**Stack:** Flask, Flask-Login, Pony ORM (SQLite), Jinja templates, ReportLab (PDF).

> **Authors / Collaborators:** Ilaria Ballerini, Elisa Biasi, Irene Greco  
> **Docs:** see `docs/` (if present).

---

## Features
- Customer area: registration/login, saved configurations, quotes (with/without trade-in), orders, messages.
- Staff area (secretariat + employees): manage brands, models, colors, engines, options, images, discounts, orders.
- Data model with **Pony ORM** entities; SQLite mapping generated at startup.

## Project structure (suggested)
```
.
├─ app.py                   # Flask app (customer routes, views)
├─ amm.py                   # Admin/staff routes
├─ database.py              # Pony ORM binding, entity imports, mapping
├─ database10/              # Entities (one .py per table: Auto, Brand, Modello, ...)
├─ templates/               # Jinja templates
├─ static/                  # CSS/JS/assets
├─ inserimenti.py           # Seed script: offices, employees, secretariat
├─ inserimento_dati.py      # Seed script: brands, colors, models, engines, options, discounts, users
├─ foto1.pdf		    # These files simulate the pictures a customer would upload when offering a used vehicle for evaluation.
├─ foto2.pdf
├─ foto3.pdf
├─ foto4.pdf
└─ Documentation            # PDF documentation (in italian)
```

## Requirements
- Python 3.10+ (recommended)
- Install packages from `requirements.txt`

## Quick start (development)
```bash
# 1) Create and activate a virtualenv
python3 -m venv env
source env/bin/activate              # Windows: env\Scripts\activate

# 2) Install deps
pip install -r requirements.txt

# 3) Initialize/seed demo data (optional)
python inserimenti.py
python inserimento_dati.py

# 4) Run
export FLASK_APP=app.py              # Windows PowerShell: $env:FLASK_APP="app.py"
flask run                            # or: python app.py (if app.py calls app.run)
```

## Configuration notes
- SQLite database file is created/bound by `database.py` (e.g., `database.db`).
- Default credentials/seeds are provided by the seed scripts above.
- For production, move secrets to environment variables and run behind a WSGI server (e.g., gunicorn).

## Acknowledgments
This project was developed as a group effort by **Ilaria Ballerini**, **Elisa Biasi**, and **Irene Greco**.
