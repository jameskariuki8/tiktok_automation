# TikTok Growth Assistant

AI-powered TikTok management platform built with Django, Celery, and LangChain.

## Tech Stack
- **Backend:** Django, DRF
- **Database:** PostgreSQL (currently configured with SQLite for initial setup)
- **Queue:** Celery + Redis
- **AI:** LangChain + Gemini
- **Frontend:** Tailwind CSS

## Prerequisites
- Windows OS
- [uv](https://github.com/astral-sh/uv)
- Python 3.11+
- Redis (for Celery)

## Setup
1. Clone the repository.
2. Initialize environment:
   ```powershell
   uv sync
   ```
3. Update `.env` with your API keys.
4. Run migrations:
   ```powershell
   uv run python manage.py migrate
   ```
5. Create a superuser (if not already created):
   ```powershell
   uv run python manage.py createsuperuser
   ```

## Running the app
1. Start the Django server:
   ```powershell
   uv run python manage.py runserver
   ```
2. Start Celery worker:
   ```powershell
   uv run celery -A config worker --loglevel=info -P solo
   ```
   *(Note: Use `-P solo` on Windows)*

## App URLs
- **Main Dashboard:** http://127.0.0.1:8000/
- **API Documentation:** http://127.0.0.1:8000/api/docs/
- **Admin Panel:** http://127.0.0.1:8000/admin/
