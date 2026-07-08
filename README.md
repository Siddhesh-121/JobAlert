# 🤖 Job Alert Bot — GenAI/AI Engineer Roles → Telegram

Scrapes LinkedIn for GenAI/AI Engineer jobs in Ireland and sends new listings
to your Telegram every hour via GitHub Actions. Fully free to run.

---

## Project structure

```
job-alert-bot/
├── main.py              ← orchestrator (run this)
├── filter.py            ← keyword matching
├── dedup.py             ← seen-job tracking
├── notifier.py          ← Telegram sender
├── requirements.txt
├── data/
│   └── seen_jobs.json   ← auto-updated by bot
├── scrapers/
│   ├── __init__.py
│   └── linkedin.py      ← active scraper (swap/add others here)
└── .github/
    └── workflows/
        └── job_alert.yml ← GitHub Actions schedule
```

---

## Setup (one-time, ~15 minutes)

### Step 1 — Create your Telegram Bot

1. Open Telegram → search **@BotFather** → send `/newbot`
2. Follow prompts → copy the **token** (e.g. `7123456789:AAF...`)
3. Open a chat with your new bot and send `/start`
4. Visit this URL in your browser (replace YOUR_TOKEN):
   ```
   https://api.telegram.org/botYOUR_TOKEN/getUpdates
   ```
5. Find `"chat":{"id": XXXXXXXXX}` → copy that number — it's your **CHAT_ID**

### Step 2 — Push to GitHub

```bash
git init
git add .
git commit -m "init: job alert bot"
git remote add origin https://github.com/YOUR_USERNAME/job-alert-bot.git
git push -u origin main
```

### Step 3 — Add GitHub Secrets

In your repo → **Settings → Secrets and variables → Actions → New repository secret**

| Secret name           | Value                    |
|-----------------------|--------------------------|
| `TELEGRAM_BOT_TOKEN`  | your bot token from Step 1 |
| `TELEGRAM_CHAT_ID`    | your chat ID from Step 1   |

### Step 4 — Enable Actions

Go to your repo → **Actions tab** → click **"I understand my workflows, go ahead and enable them"**

That's it. The bot runs at the top of every hour (6am–10pm UTC).

---

## Run locally (optional)

```bash
pip install -r requirements.txt

# Set env vars
export TELEGRAM_BOT_TOKEN="your_token"
export TELEGRAM_CHAT_ID="your_chat_id"

python main.py
```

---

## Adding more job sites

Each scraper lives in `scrapers/`. To add Indeed for example:

1. Create `scrapers/indeed.py` with a `scrape()` function returning the same dict shape
2. Uncomment the import in `scrapers/__init__.py`
3. Uncomment the call in `main.py`

The dict shape every scraper must return:
```python
{
    "title":    str,
    "company":  str,
    "location": str,
    "url":      str,
    "source":   str,   # e.g. "Indeed"
}
```

---

## Tuning keywords

Edit `filter.py` → `INCLUDE_KEYWORDS` / `EXCLUDE_KEYWORDS` to match the exact
roles you want. The filter checks title + company name.

---

## Telegram message preview

```
🤖 3 new GenAI/AI jobs found!

1. AI Engineer
🏢 Accenture Ireland
📍 Cork, Ireland
🔗 View job
📌 LinkedIn

2. LLM Platform Engineer
🏢 Workday
📍 Dublin, Ireland
🔗 View job
📌 LinkedIn
```
