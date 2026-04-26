web: bash init_railway.sh
worker: celery -A config worker --loglevel=info -P solo
bot: python apps/orchestrator/telegram_bot.py
