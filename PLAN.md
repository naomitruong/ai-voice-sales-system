# Voice Sales Bot — Demo Plan

## Overview

A Telegram bot that receives voice messages from salespeople, transcribes them, extracts structured call data using AI, and inserts the result into a database.

## Architecture

```
Salesperson
    │ sends voice message
    ▼
Telegram Bot
    │ receives .ogg audio file
    ▼
Python Backend
    ├─ Step 1: Download voice file from Telegram
    ├─ Step 2: Transcribe with OpenAI Whisper (local, free)
    ├─ Step 3: Send transcript to Claude → extract structured data
    │          {date, customer_id, status, note}
    └─ Step 4: INSERT INTO phone_call (SQLite)
    │
    └─ Step 5: Reply to salesperson with confirmation summary
```

## Database Schema

```sql
CREATE TABLE phone_call (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    date        TEXT,         -- e.g. "2026-06-23"
    customer_id TEXT,         -- e.g. "A", "Nguyen Van B"
    status      TEXT,         -- "rejected", "interested", "no_callback"
    note        TEXT,         -- e.g. "do not call back"
    created_at  TEXT          -- timestamp of insert
);
```

## Build Phases

| Phase | What | Details |
|-------|------|---------|
| 1 | **Setup** | Create Telegram bot via @BotFather, get token |
| 2 | **Bot skeleton** | Python script using `python-telegram-bot` library |
| 3 | **Voice → Text** | Download OGG from Telegram, run Whisper locally |
| 4 | **Text → Struct** | Call Claude API to extract JSON fields |
| 5 | **DB insert** | SQLite write, return confirmation message to user |
| 6 | **Deploy** | Run locally in polling mode — no server needed for demo |

## Tech Stack

| Tool | Purpose |
|------|---------|
| `python-telegram-bot` | Telegram bot framework |
| `openai-whisper` | Local speech-to-text (free, offline) |
| `anthropic` SDK | Claude for NLP extraction |
| `sqlite3` | Built-in Python, zero setup |
| `ffmpeg` | Audio conversion (OGG → WAV for Whisper) |

## Sample Bot Interaction

```
Salesperson sends: 🎤 [voice message]
  "Gọi cho khách A, họ từ chối và nói đừng gọi lại"

Bot replies:
  ✅ Đã lưu cuộc gọi:
  📅 Date: 2026-06-23
  👤 Customer: A
  📊 Status: rejected
  📝 Note: do not call back
```

## Prerequisites

1. Telegram account → create bot via `@BotFather` → get bot token
2. Anthropic API key
3. `ffmpeg` installed on machine
4. Python 3.9+

## Project Structure (target)

```
ai-voice-input/
├── PLAN.md
├── requirements.txt
├── .env                  # TELEGRAM_TOKEN, ANTHROPIC_API_KEY
├── bot.py                # main entry point
├── transcriber.py        # Whisper voice-to-text
├── extractor.py          # Claude NLP extraction
└── database.py           # SQLite operations
```
