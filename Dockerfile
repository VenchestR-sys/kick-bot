FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    sqlite3 tzdata \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/data/backup /app/logs

RUN useradd -m -u 1000 kickbot && chown -R kickbot:kickbot /app
USER kickbot

CMD ["python", "main.py"]
