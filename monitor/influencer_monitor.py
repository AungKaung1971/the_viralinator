import os
import json
import sqlite3
from pathlib import Path
from datetime import datetime, timezone
import logging
from typing import List, Dict, Optional
from twikit import Client
from config import auth_token, cto_token, data_base_path
import asyncio

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


def tweet_exits(tweet_id):
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

# scraper code


async def main():
    create_tables()
    client = Client('en-US')
    client.set_cookies({
        'auth_token': auth_token,
        'ct0': cto_token
    })

    user = await client.get_user_by_screen_name('elonmusk')
    tweets = await client.get_user_tweets(user.id, 'Tweets')

    for t in tweets[:2]:
        tweet_id = str(t.id)
        content = t.text
        username = user.screen_name

        if not tweet_exits(tweet_id):
            store_influencer_post(tweet_id, username, content)
            print(f"✅ Saved tweet: {tweet_id[:6]}... | {content[:50]}...")
        else:
            print(f"⚪ Skipped existing tweet: {tweet_id}")


if __name__ == "__main__":
    asyncio.run(main())


# rm -rf **/__pycache__/
# python -m monitor.influencer_monitor

# sqlite3 data/tweetinator.db "SELECT * FROM influencer_posts;"


# data base code paste above after
