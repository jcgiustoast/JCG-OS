"""Telegram → JCG-OS inbox listener.

Long-polls Telegram, saves each message (text or voice) into
life/raw/inbox/YYYY-MM-DD.md. Voice notes are transcribed via OpenAI Whisper
and the original .ogg is kept alongside.

Run: python bot.py
"""
from __future__ import annotations

import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
VAULT = ROOT.parent
INBOX_DIR = VAULT / "life" / "raw" / "inbox"
STATE_FILE = ROOT / "state.json"

load_dotenv(ROOT / ".env")

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
ALLOWED_USER_ID = int(os.environ["TELEGRAM_ALLOWED_USER_ID"])
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

API = f"https://api.telegram.org/bot{BOT_TOKEN}"
FILE_API = f"https://api.telegram.org/file/bot{BOT_TOKEN}"


def load_offset() -> int:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text()).get("offset", 0)
    return 0


def save_offset(offset: int) -> None:
    STATE_FILE.write_text(json.dumps({"offset": offset}))


def inbox_file_for(dt: datetime) -> Path:
    INBOX_DIR.mkdir(parents=True, exist_ok=True)
    path = INBOX_DIR / f"{dt.strftime('%Y-%m-%d')}.md"
    if not path.exists():
        path.write_text(f"# Inbox {dt.strftime('%Y-%m-%d')}\n\n")
    return path


def append_entry(dt: datetime, kind: str, body: str, extra: str = "") -> None:
    path = inbox_file_for(dt)
    header = f"## {dt.strftime('%H:%M')} — {kind}"
    if extra:
        header += f" ({extra})"
    with path.open("a", encoding="utf-8") as f:
        f.write(f"\n{header}\n\n{body.strip()}\n")


def download_file(file_id: str, dest: Path) -> None:
    r = requests.get(f"{API}/getFile", params={"file_id": file_id}, timeout=30)
    r.raise_for_status()
    file_path = r.json()["result"]["file_path"]
    audio = requests.get(f"{FILE_API}/{file_path}", timeout=60)
    audio.raise_for_status()
    dest.write_bytes(audio.content)


def transcribe(audio_path: Path) -> str:
    if not OPENAI_API_KEY:
        return "[voice note — set OPENAI_API_KEY to auto-transcribe]"
    with audio_path.open("rb") as f:
        r = requests.post(
            "https://api.openai.com/v1/audio/transcriptions",
            headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
            files={"file": (audio_path.name, f, "audio/ogg")},
            data={"model": "whisper-1"},
            timeout=120,
        )
    if r.status_code != 200:
        return f"[transcription failed: {r.status_code} {r.text[:200]}]"
    return r.json().get("text", "").strip()


def send_reply(chat_id: int, text: str) -> None:
    try:
        requests.post(f"{API}/sendMessage", json={"chat_id": chat_id, "text": text}, timeout=10)
    except Exception:
        pass


def handle_message(msg: dict) -> None:
    user_id = msg.get("from", {}).get("id")
    chat_id = msg.get("chat", {}).get("id")
    if user_id != ALLOWED_USER_ID:
        send_reply(chat_id, "Not authorized.")
        return

    ts = datetime.fromtimestamp(msg.get("date", time.time()))

    if "text" in msg:
        append_entry(ts, "text", msg["text"])
        send_reply(chat_id, "Saved.")
        return

    if "voice" in msg or "audio" in msg:
        voice = msg.get("voice") or msg["audio"]
        duration = voice.get("duration", 0)
        audio_name = f"{ts.strftime('%Y-%m-%d-%H%M%S')}.ogg"
        audio_path = INBOX_DIR / audio_name
        INBOX_DIR.mkdir(parents=True, exist_ok=True)
        download_file(voice["file_id"], audio_path)
        transcript = transcribe(audio_path)
        body = f"{transcript}\n\n_Audio: `{audio_name}`_"
        append_entry(ts, "voice", body, extra=f"{duration}s")
        send_reply(chat_id, f"Saved voice ({duration}s).")
        return

    if "photo" in msg:
        caption = msg.get("caption", "")
        photo = msg["photo"][-1]
        img_name = f"{ts.strftime('%Y-%m-%d-%H%M%S')}.jpg"
        img_path = INBOX_DIR / img_name
        download_file(photo["file_id"], img_path)
        body = f"![photo]({img_name})"
        if caption:
            body += f"\n\n{caption}"
        append_entry(ts, "photo", body)
        send_reply(chat_id, "Saved photo.")
        return

    send_reply(chat_id, "Unsupported message type (text/voice/photo only).")


def main() -> None:
    offset = load_offset()
    print(f"[bot] listening (offset={offset}) writing to {INBOX_DIR}", flush=True)
    while True:
        try:
            r = requests.get(
                f"{API}/getUpdates",
                params={"offset": offset, "timeout": 30},
                timeout=40,
            )
            r.raise_for_status()
            for update in r.json().get("result", []):
                offset = update["update_id"] + 1
                if "message" in update:
                    try:
                        handle_message(update["message"])
                    except Exception as e:
                        print(f"[bot] handler error: {e}", file=sys.stderr, flush=True)
                save_offset(offset)
        except requests.exceptions.ReadTimeout:
            continue
        except KeyboardInterrupt:
            print("[bot] stopping")
            return
        except Exception as e:
            print(f"[bot] poll error: {e}", file=sys.stderr, flush=True)
            time.sleep(5)


if __name__ == "__main__":
    main()
