# Madalyon Sitesi (Flask)

Small Flask website with several templates and a simple SQLite database for users and an admin account.

Quick start (macOS, zsh):

1. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app

```bash
python app.py
```

4. Open http://127.0.0.1:5000 in your browser. Default admin: `admin` / `sifre123`.

Notes:
- The app uses `database.db` in the project root; the DB and default admin are created automatically when you first run the app.
- For deployment to Heroku/Railway, include a `Procfile` and set `FLASK_ENV`/`SECRET_KEY` in environment variables instead of hardcoding.
