import openai
import os
import json
import sqlite3
from pathlib import Path
from datetime import datetime, timezone
import logging
from typing import List, Dict, Optional
from twikit import Client
from config import auth_token, cto_token, data_base_path, openAI_key, target_users
import asyncio
from openai import OpenAI


client = OpenAI(api_key=openAI_key)


print("OpenAI SDK version:", getattr(openai, "__version__", "old SDK"))

# db code


def connect_db():
    return sqlite3.connect(data_base_path)


def create_tables():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS influencer_posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tweet_id TEXT UNIQUE,
            influencer_username TEXT,
            tweet_content TEXT,
            timestamp DATETIME
                 )
                 """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS generated_replies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            influencer_username TEXT,
            tweet_id TEXT,
            tweet_content TEXT,
            reply_text TEXT,
            timestamp DATETIME
        )
    """)
    conn.commit()
    conn.close()


def tweet_exists(tweet_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM influencer_posts WHERE tweet_id = ?", (tweet_id,))
    exists = cur.fetchone() is not None
    conn.close()
    return exists


def store_influencer_post(tweet_id, username, content):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT OR IGNORE INTO influencer_posts (tweet_id, influencer_username, tweet_content, timestamp) VALUES (?, ?, ?, ?)",
        (tweet_id, username, content, datetime.now(timezone.utc))
    )
    conn.commit()
    conn.close()

# gpt input code


def reply_generator(tweet_content, niche="tech"):

    prompt = f"""
        You are a sharp, witty commentator in the {niche} niche.
        Write a short, natural reply (under 25 words) to the following tweet:
        ---
        {tweet_content}
        ---
        The reply should sound conversational and insightful, not promotional.
        """
    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[{"role": "user", "content": prompt}],
    )

    return response.choices[0].message.content.strip()

# def reply_generator(tweet_content, niche="tech"):
#     clean_tweet = tweet_content.split("https")[0][:250]

#     prompt = f"""
#     You are a sharp, witty commentator in the {niche} niche.
#     Write a short, natural reply (under 25 words) to the following tweet:
#     ---
#     {clean_tweet}
#     ---
#     The reply should sound conversational and insightful, not promotional.
#     """

#     print("\n=== PROMPT SENT TO GPT ===")
#     print(prompt)
#     print("==========================")

#     response = client.chat.completions.create(
#         model="gpt-5-mini",
#         messages=[{"role": "user", "content": prompt}],
#     )

#     print("\n=== RAW GPT RESPONSE ===")
#     print(response)
#     print("========================\n")

#     try:
#         reply = response.choices[0].message.content
#         print("Extracted reply:", repr(reply))
#         if not reply or not reply.strip():
#             print("⚠️ GPT returned empty content or only whitespace.")
#             reply = "[Empty GPT reply]"
#     except Exception as e:
#         print("❌ Exception extracting reply:", e)
#         reply = "[Error parsing GPT reply]"

#     return reply.strip()


# scraper code


async def main():
    create_tables()
    twitter_client = Client('en-US')
    twitter_client.set_cookies({
        'auth_token': auth_token,
        'ct0': cto_token
    })

    influencers = target_users

    for username in influencers:
        user = await twitter_client.get_user_by_screen_name(username)
        tweets = await twitter_client.get_user_tweets(user.id, 'Tweets')

        for t in tweets[:3]:
            if not tweet_exists(t.id):
                print(f"New tweet from {username}: {t.text[:80]}...")
                store_influencer_post(t.id, username, t.text)

                reply = reply_generator(t.text)
                print(f"Generated Reply >> {reply}")

                conn = connect_db()
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO generated_replies (influencer_username, tweet_id, tweet_content, reply_text, timestamp)
                    VALUES (?, ?, ?, ?, ?)
                """, (username, t.id, t.text, reply, datetime.now(timezone.utc)))
                conn.commit()
                conn.close()
            else:
                print(f"Already seen tweet from {username}")


if __name__ == "__main__":
    asyncio.run(main())


# rm -rf **/__pycache__/
# python -m monitor.influencer_monitor

# sqlite3 data/tweetinator.db "SELECT * FROM influencer_posts;"


# data base code paste above after
