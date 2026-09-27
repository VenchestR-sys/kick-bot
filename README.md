# KICK Bot

Telegram bot for goal tracking with gamification.

## Stack

- Python 3.12
- aiogram 3
- SQLAlchemy 2 (async)
- SQLite (WAL)

## Deploy

` ` `bash
git clone <repo> /opt/kick
cd /opt/kick
cp .env.example .env
nano .env
docker compose up -d --build
` ` `

## Backup

Cron:
` ` `
0 4 * * * /opt/kick/backup.sh
` ` `
