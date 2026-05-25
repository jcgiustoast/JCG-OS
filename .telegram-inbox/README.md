# Telegram Inbox

Long-polls Telegram and writes messages into `life/raw/inbox/YYYY-MM-DD.md`.
Run `/process-inbox` in Claude later to file them into the wiki.

## One-time setup

1. **Create the bot**
   - Telegram → message `@BotFather` → `/newbot` → pick a name. Copy the token.

2. **Find your user ID**
   - Message `@userinfobot` → it replies with your numeric ID.

3. **Configure**
   ```
   cp .env.example .env
   # fill TELEGRAM_BOT_TOKEN, TELEGRAM_ALLOWED_USER_ID, OPENAI_API_KEY
   ```

4. **Install deps**
   ```
   pip install -r requirements.txt
   ```

## Run

```
python bot.py
```

Leave it running. Minimize the window. Add to Windows startup:
- `Win+R` → `shell:startup` → drop a shortcut to `run.bat` in that folder.

## What gets saved

- **Text** → appended under `## HH:MM — text`
- **Voice** → transcribed via Whisper, `.ogg` kept in same folder
- **Photo** → saved as `.jpg`, rendered inline in the daily file

The bot replies "Saved." so you know it worked.
