# AI Voice Input — Sales Call Bot

A Telegram bot for salespeople: send a voice message after a call, get structured data saved to a database automatically.

## How it works

```
Salesperson sends voice message on Telegram
    │
    ▼
Bot downloads .ogg file
    │
    ▼
faster-whisper transcribes audio → Vietnamese text (runs locally, free)
    │
    ▼
Claude AI extracts structured fields from transcript
    { date, customer_id, customer_phone, status, note }
    │
    ▼
SQLite saves the record → Bot replies with confirmation
```

## Sample interaction

```
Salesperson: 🎤 "Gọi cho khách Nguyễn Văn A, số không 9,09,12,34,56,
                  họ từ chối và nói đừng gọi lại"

Bot replies:
  ✅ Đã lưu cuộc gọi:
  📅 Date: 2026-06-24
  👤 Customer: Nguyễn Văn A
  📞 Phone: 0909123456
  📊 Status: rejected
  📝 Note: do not call back
```

## Prerequisites

- Python 3.9+
- `ffmpeg` installed and on PATH
- Telegram bot token (create via [@BotFather](https://t.me/BotFather))
- Anthropic API key

## Setup

```bash
# 1. Clone and create virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt
pip install faster-whisper   # not in requirements.txt yet

# 3. Create .env file
cp .env.example .env
# Fill in TELEGRAM_TOKEN and ANTHROPIC_API_KEY

# 4. Run
python bot.py
```

## Environment variables

Create a `.env` file in the project root:

```
TELEGRAM_TOKEN=your_telegram_bot_token
ANTHROPIC_API_KEY=your_anthropic_api_key
```

## Project structure

```
ai-voice-input/
├── bot.py            # Telegram bot entry point, message handlers
├── transcriber.py    # faster-whisper speech-to-text (Vietnamese)
├── extractor.py      # Claude AI structured data extraction
├── database.py       # SQLite init and save operations
├── requirements.txt
└── .env              # secrets (not committed)
```

## Database schema

```sql
CREATE TABLE phone_call (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    date            TEXT,   -- "2026-06-24"
    customer_id     TEXT,   -- customer name or ID
    customer_phone  TEXT,   -- 10-digit Vietnamese phone number
    status          TEXT,   -- "interested" | "rejected" | "no_callback"
    note            TEXT,
    created_at      TEXT    -- ISO timestamp
);
```

## Tech stack

| Component | Library |
|-----------|---------|
| Telegram bot | `python-telegram-bot` 20.x |
| Speech-to-text | `faster-whisper` (local, offline) |
| AI extraction | `anthropic` SDK — Claude Haiku |
| Database | SQLite via `sqlite3` (built-in) |
| Audio conversion | `ffmpeg` (OGG → WAV) |
