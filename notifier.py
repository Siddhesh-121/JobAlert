"""
TELEGRAM NOTIFIER
━━━━━━━━━━━━━━━━
Sends job alerts to your Telegram chat via Bot API.

Setup (one-time, 5 minutes):
  1. Open Telegram → search @BotFather → /newbot → follow prompts
     → copy the token (looks like 7123456789:AAF...)
  2. Start a chat with your new bot (send /start)
  3. Visit: https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates
     → find "chat":{"id": XXXXXXXXX} — that's your CHAT_ID
  4. Add both as GitHub Secrets:
       TELEGRAM_BOT_TOKEN
       TELEGRAM_CHAT_ID

Reads from env vars set by GitHub Actions (or a local .env file).
"""

import os
import requests

TELEGRAM_API = "https://api.telegram.org/bot{token}/sendMessage"

# Max jobs per Telegram message batch (Telegram limit: 4096 chars/message)
BATCH_SIZE = 5


def _credentials() -> tuple[str, str]:
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    chat  = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
    return token, chat


def send_alert(jobs: list[dict]) -> None:
    """Send new job alerts. Batches if many jobs found."""
    if not jobs:
        return

    token, chat = _credentials()
    if not token or not chat:
        print("[Telegram] ⚠️  TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set — skipping send.")
        return

    header = f"🤖 *{len(jobs)} new SDE job{'s' if len(jobs) > 1 else ''}* found!\n\n"

    # Split into batches to avoid message length limits
    for i in range(0, len(jobs), BATCH_SIZE):
        batch = jobs[i : i + BATCH_SIZE]
        body  = "\n\n".join(_format_job(j, idx + i + 1) for idx, j in enumerate(batch))
        text  = (header if i == 0 else "") + body
        _send(text)


def send_summary(total_scraped: int, total_new: int) -> None:
    """Optional: send a quiet summary when no new jobs found."""
    if total_new > 0:
        return   # already sent detailed alerts
    token, chat = _credentials()
    if not token or not chat:
        print("[Telegram] ⚠️  TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set — skipping send.")
        return
    text = f"✅ Job scan complete — {total_scraped} jobs checked, none new."
    _send(text)


def _format_job(job: dict, n: int) -> str:
    return (
        f"*{n}. {_esc(job['title'])}*\n"
        f"🏢 {_esc(job['company'])}\n"
        f"📍 {_esc(job['location'])}\n"
        f"🔗 [View job]({job['url']})\n"
        f"📌 _{job['source']}_"
    )


def _send(text: str) -> None:
    token, chat = _credentials()
    url  = TELEGRAM_API.format(token=token)
    data = {
        "chat_id":    chat,
        "text":       text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True,
    }
    try:
        resp = requests.post(url, json=data, timeout=10)
        resp.raise_for_status()
        print(f"[Telegram] ✅ Message sent ({len(text)} chars)")
    except requests.RequestException as e:
        print(f"[Telegram] ❌ Failed to send: {e}")


def _esc(text: str) -> str:
    """Escape Markdown special chars in job data."""
    for ch in ["*", "_", "`", "["]:
        text = text.replace(ch, f"\\{ch}")
    return text
