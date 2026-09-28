# FitBuddy – AI Fitness Plan Generator

Complete FastAPI + Jinja2 + SQLAlchemy/SQLite + Gemini implementation based on the supplied project documentation.

## Features
- Personalized 7-day workout generation
- Gemini-powered nutrition/recovery tip
- Feedback-based AI plan regeneration
- SQLite persistence with SQLAlchemy
- Admin/coach user and plan view
- JSON API endpoints
- Swagger/OpenAPI at `/docs`
- Local fallback generation when no Gemini key is configured
- Automated tests

## VS Code / Windows

```powershell
cd FitBuddy
py -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000

Swagger: http://127.0.0.1:8000/docs

Admin view: http://127.0.0.1:8000/view-all-users

## Gemini setup
Edit `.env`:

```env
GOOGLE_API_KEY=your_real_gemini_api_key
GEMINI_PRO_MODEL=gemini-2.5-pro
GEMINI_FLASH_MODEL=gemini-2.5-flash
```

The model names are configurable because Gemini model availability can change by account/API version. If the key is blank or a call fails, the app uses its built-in fallback so the UI/database workflow remains testable.

## Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

## Test

```bash
python -m pytest -q
```

If pytest is not installed, add it with `pip install pytest`.

## Routes
- `GET /` – input page
- `POST /generate-workout` – generate and save plan
- `POST /submit-feedback` – update an existing plan
- `GET /view-all-users` – admin view
- `GET /api/users` – JSON list
- `GET /api/users/{user_id}` – JSON user + plan
- `DELETE /api/users/{user_id}` – delete user and plan

## Safety
This is a general wellness software project, not a medical diagnostic or treatment application. It avoids medical diagnosis and unsafe training recommendations and advises professional guidance for injuries, pain, or medical conditions.
