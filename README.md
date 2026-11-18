# Case Lab v2

Clean Flask + HTML/CSS/JavaScript test build. No database and no logging of case openings.

## Run locally

### Windows
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000`.

Exit the virtual environment with `deactivate`.

## Files
- `app.py`: Flask API and Python case logic.
- `templates/index.html`: page structure.
- `static/style.css`: site appearance.
- `static/case.js`: reel animation and API call.

All item names are fictional placeholders.
