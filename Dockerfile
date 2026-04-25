FROM python:3.11-slim

# Install system dependencies required by Chromium
RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    libx11-6 \
    libxrandr2 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxkbcommon0 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libcairo2 \
    libasound2 \
    libatspi2.0-0 \
    libdbus-1-3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libgbm1 \
    libnspr4 \
    libnss3 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir playwright
RUN python -m playwright install --with-deps chromium

ENV PYTHONPATH=/app:$PYTHONPATH

CMD ["sh", "-c", "python manage.py migrate && gunicorn config.wsgi --log-file -"]
