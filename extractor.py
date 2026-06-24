import anthropic
import json
import os
from datetime import date
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def extract(transcript: str) -> dict:
    today = date.today().isoformat()
    message = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=256,
        messages=[{
            "role": "user",
            "content": f"""Extract sale data from this sales note and return ONLY valid JSON.

Today's date: {today}
Transcript: {transcript}

Return JSON with these fields:
- date: use today's date ({today}) unless a specific date is mentioned in the transcript
- customer_id: customer NAME or ID (usually after "customer" or "client" in the transcript)
- customer_phone: customer PHONE NUMBER as digits only (10-11 digits). Vietnamese phone numbers are spoken as digit groups separated by commas — concatenate them all. "không" = 0, other groups are literal digits. Examples:
  * "không 3,39,88,76,69" → 0339887669 (0 + 3 + 39 + 88 + 76 + 69)
  * "không 33976 năm không 1 2" → 0339765012
  * "không 9,09,12,34,56" → 0909123456
- status: one of "interested", "rejected", "no_callback"
- note: short summary

Example: {{"date":"2026-06-23","customer_id":"Nguyen Van A","customer_phone":"0909123456","status":"rejected","note":"do not call back"}}"""
        }]
    )
    raw = message.content[0].text.strip()
    # strip markdown code block nếu có
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]

    print("Claude raw:", json.loads(raw.strip()))
    return json.loads(raw.strip())
