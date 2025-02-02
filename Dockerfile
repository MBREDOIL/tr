FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1

# Install Chrome & Dependencies
RUN apt-get update && apt-get install -y \
    wget curl gnupg unzip \
    && wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

CMD gunicorn bot:TrackBot --bind 0.0.0.0:8000 --worker-class aiohttp.GunicornWebWorker & python3 bot.py
