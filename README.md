# Social Media Automation with Python + Zernio API

> Automate and schedule posts on Twitter/X, Reddit, LinkedIn and more — powered by Python and the [Zernio API](https://zernio.link/kevin-meneses).

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://python.org)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-green?logo=openai)](https://openai.com)
[![Zernio](https://img.shields.io/badge/Powered%20by-Zernio-7C3AED)](https://zernio.link/kevin-meneses)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

---

## What is this?

A Python script that **automatically generates and schedules social media posts** across multiple platforms using:

- **[Zernio](https://zernio.link/kevin-meneses)** — REST API for multi-platform social media scheduling (Twitter, Reddit, LinkedIn, Instagram, Facebook)
- **OpenAI GPT-4o-mini** — dynamic content generation so every post is fresh and unique

No more manually writing and posting content every day. Set it up once, run it weekly, and let the automation handle the rest.

---

## Features

- **AI-generated content** — GPT creates unique tweets and Reddit posts on topics you define
- **Multi-platform posting** — publish to Twitter/X and Reddit in a single script run
- **Full week scheduling** — schedules 4 posts spread across 7 days automatically
- **Zernio REST API** — clean integration with Bearer auth, no third-party SDK needed
- **`.env` based config** — API keys loaded safely from environment variables

---

## Demo output

```
🔗 Connecting to Zernio...

📋 Connected accounts:
   reddit          → 6a2135f22b2567671ac3e5e4
   twitter         → 6a2136552b2567671ac3e855

🤖 Generating content with ChatGPT and scheduling posts...

  ✅ Twitter  | 2025-06-04T10:00:00 | ID: 6a2142f2d786bdfc96598f5b
     🐍 Python tip: stop writing for-loops just to build lists...

  ✅ Reddit   | 2025-06-06T10:00:00 | r/learnprogramming | ID: 6a2143aad786bdfc96598f6c
     I automated my entire social media presence with 80 lines of Python

  ✅ Twitter  | 2025-06-08T10:00:00 | ID: 6a2144bbd786bdfc96598f7d
     Consistency is the #1 growth hack — so I automated it 🚀

  ✅ Reddit   | 2025-06-10T10:00:00 | r/Python | ID: 6a2145ccd786bdfc96598f8e
     Built a Python bot that posts to 5 platforms while I sleep

🎉 Done! Check your Zernio dashboard to see the scheduled posts.
```

---

## Quick start

### 1. Clone the repo

```bash
git clone https://github.com/Kevinelectronics/social-media-automation.git
cd social-media-automation
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up your API keys

Copy `.env.example` to `.env` and fill in your keys:

```bash
cp .env.example .env
```

```env
ZERNIO_API_KEY=your_zernio_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

- **Zernio API key** → get yours free at [zernio.link/kevin-meneses](https://zernio.link/kevin-meneses)
- **OpenAI API key** → [platform.openai.com/api-keys](https://platform.openai.com/api-keys)

### 4. Connect your social accounts

Log in to [Zernio](https://zernio.link/kevin-meneses), go to **Accounts**, and connect your Twitter and Reddit profiles.

### 5. Run the script

```bash
python main.py
```

The script will generate AI content and schedule 4 posts across the coming week.

---

## How it works

```
main.py
  │
  ├── get_accounts()          # fetch connected account IDs from Zernio
  │
  ├── generate_tweet()        # ask GPT-4o-mini to write a tweet on a random topic
  ├── generate_reddit_post()  # ask GPT-4o-mini for a Reddit title + body (JSON)
  │
  └── schedule_week()         # loop through 4 slots, call Zernio POST /posts each time
```

The Zernio API endpoint used:

```
POST https://zernio.com/api/v1/posts
Authorization: Bearer YOUR_KEY
Content-Type: application/json

{
  "content": "...",
  "platforms": [{ "platform": "twitter", "accountId": "..." }],
  "publishNow": false,
  "scheduledFor": "2025-06-10T10:00:00",
  "timezone": "America/New_York"
}
```

---

## Customization

### Change topics

Edit `TOPICS` in `main.py` to generate posts about anything:

```python
TOPICS = [
    "Python automation tips",
    "productivity for developers",
    "your niche here",
]
```

### Change posting frequency

Edit the `schedule` list in `schedule_week()` to add/remove slots or change days and hours.

### Add more platforms

Zernio supports LinkedIn, Instagram and Facebook. Add a new entry to `schedule` with `"platform": "linkedin"` and the corresponding account ID.

---

## Requirements

```
requests
python-dotenv
openai
```

Python 3.10+ required.

---

## Why Zernio?

If you want to replicate this project, you'll need a [Zernio](https://zernio.link/kevin-meneses) account. It's the only multi-platform social media API I've found that:

- Supports Twitter, Reddit, LinkedIn, Instagram and Facebook in one REST API
- Has clean, well-documented endpoints
- Offers a **free tier** to get started without a credit card
- Works perfectly with Python's `requests` library — no SDK needed

**[→ Get started free on Zernio](https://zernio.link/kevin-meneses)**

---

## License

MIT — use it however you want.

---

*Built by [Kevin Meneses](https://twitter.com/meneses_kevin)*
