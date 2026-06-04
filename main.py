"""
Automate Social Media Posting with Python + Zernio API
Content generated dynamically via OpenAI ChatGPT
Platforms: Twitter/X and Reddit
"""

import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)

# ── Config ─────────────────────────────────────────────────────────────────────

API_KEY  = os.environ["ZERNIO_API_KEY"]
BASE_URL = "https://zernio.com/api/v1"
HEADERS  = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

openai_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# ── Step 1: Get your connected account IDs ─────────────────────────────────────

def get_accounts() -> list[dict]:
    response = requests.get(f"{BASE_URL}/accounts", headers=HEADERS)
    response.raise_for_status()
    return response.json()["accounts"]


def find_account_id(accounts: list[dict], platform: str) -> str:
    for account in accounts:
        if account["platform"] == platform:
            return account["_id"]
    raise ValueError(f"No connected account found for: {platform}")


# ── Step 2: Post to Twitter ─────────────────────────────────────────────────────

def post_to_twitter(account_id: str, content: str, scheduled_for: str | None = None) -> dict:
    payload = {
        "content": content,
        "platforms": [{"platform": "twitter", "accountId": account_id}],
        "publishNow": scheduled_for is None,
    }
    if scheduled_for:
        payload["scheduledFor"] = scheduled_for
        payload["timezone"] = "America/New_York"

    response = requests.post(f"{BASE_URL}/posts", headers=HEADERS, json=payload)
    response.raise_for_status()
    return response.json()


# ── Step 3: Post to Reddit ──────────────────────────────────────────────────────

def post_to_reddit(
    account_id: str,
    title: str,
    body: str,
    subreddit: str,
    scheduled_for: str | None = None,
) -> dict:
    payload = {
        "content": f"{title}\n\n{body}",
        "platforms": [
            {
                "platform": "reddit",
                "accountId": account_id,
                "platformSpecificData": {
                    "subreddit": subreddit,
                    "title": title,
                },
            }
        ],
        "publishNow": scheduled_for is None,
    }
    if scheduled_for:
        payload["scheduledFor"] = scheduled_for
        payload["timezone"] = "America/New_York"

    response = requests.post(f"{BASE_URL}/posts", headers=HEADERS, json=payload)
    response.raise_for_status()
    return response.json()


# ── Step 4: Dynamic content generation via ChatGPT ─────────────────────────────

TOPICS = [
    "Python automation tips",
    "productivity for developers",
    "clean code practices",
    "useful Python libraries",
    "building side projects",
]

SUBREDDITS = ["learnprogramming", "Python", "programming", "devops", "MachineLearning"]


def generate_tweet() -> str:
    import random
    topic = random.choice(TOPICS)
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a developer content creator. Write engaging, concise tweets "
                    "for a technical audience. Always include 2-3 relevant hashtags. "
                    "Keep it under 260 characters. No quotes around the tweet."
                ),
            },
            {
                "role": "user",
                "content": f"Write a tweet about: {topic}",
            },
        ],
        max_tokens=100,
        temperature=0.9,
    )
    return response.choices[0].message.content.strip()[:280]


def generate_reddit_post() -> dict:
    import random
    topic = random.choice(TOPICS)
    subreddit = random.choice(SUBREDDITS)
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a developer sharing knowledge on Reddit. "
                    "Respond with a JSON object with exactly two keys: "
                    '"title" (concise Reddit post title, max 100 chars) and '
                    '"body" (3-5 sentences, conversational, no markdown headers). '
                    "Output only the JSON, no extra text."
                ),
            },
            {
                "role": "user",
                "content": f"Write a Reddit post about: {topic}",
            },
        ],
        max_tokens=300,
        temperature=0.85,
        response_format={"type": "json_object"},
    )
    import json
    data = json.loads(response.choices[0].message.content)
    return {
        "title": data["title"],
        "body": data["body"],
        "subreddit": subreddit,
    }


# ── Step 5: Schedule a full week of posts ──────────────────────────────────────

def schedule_week(twitter_id: str, reddit_id: str) -> None:
    now = datetime.now()

    schedule = [
        # Day 1 – Twitter
        {
            "platform": "twitter",
            "content": generate_tweet(),
            "when": now + timedelta(days=0, hours=10),
        },
        # Day 3 – Reddit
        {
            "platform": "reddit",
            **generate_reddit_post(),
            "when": now + timedelta(days=2, hours=10),
        },
        # Day 5 – Twitter
        {
            "platform": "twitter",
            "content": generate_tweet(),
            "when": now + timedelta(days=4, hours=10),
        },
        # Day 7 – Reddit
        {
            "platform": "reddit",
            **generate_reddit_post(),
            "when": now + timedelta(days=6, hours=10),
        },
    ]

    print("\n🤖 Generating content with ChatGPT and scheduling posts...\n")

    for post in schedule:
        scheduled_str = post["when"].strftime("%Y-%m-%dT%H:%M:%S")

        if post["platform"] == "twitter":
            result = post_to_twitter(twitter_id, post["content"], scheduled_for=scheduled_str)
            print(f"  ✅ Twitter  | {scheduled_str} | ID: {result['post']['_id']}")
            print(f"     {post['content'][:60]}...\n")

        elif post["platform"] == "reddit":
            result = post_to_reddit(
                reddit_id,
                post["title"],
                post["body"],
                post["subreddit"],
                scheduled_for=scheduled_str,
            )
            print(f"  ✅ Reddit   | {scheduled_str} | r/{post['subreddit']} | ID: {result['post']['_id']}")
            print(f"     {post['title']}\n")


# ── Main ────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("🔗 Connecting to Zernio...\n")

    accounts = get_accounts()

    print("📋 Connected accounts:")
    for acc in accounts:
        print(f"   {acc['platform']:15} → {acc['_id']}")

    twitter_id = find_account_id(accounts, "twitter")
    reddit_id  = find_account_id(accounts, "reddit")

    schedule_week(twitter_id, reddit_id)

    print("🎉 Done! Check your Zernio dashboard to see the scheduled posts.")
