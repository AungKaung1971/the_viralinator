import os
import json
import sqlite3
from pathlib import Path
from datetime import datetime, timezone
import logging
from typing import List, Dict, Optional
from twikit import Client
from config import auth_token, cto_token
import asyncio


# def get_usernames():
#     print("Enter Target Usernames: ")

#     usernames = []
#     while True:
#         username = input("> ").strip()
#         if username == "done":
#             break
#         elif username:
#             usernames.append(username)

#     return usernames


# if __name__ == "__main__":
#     target_usernames = get_usernames()
#     print("Usernames chosen:", target_usernames)

async def main():
    client = Client('en-US')
    client.set_cookies({
        'auth_token': auth_token,
        'ct0': cto_token
    })

    user = await client.get_user_by_screen_name('elonmusk')
    tweets = await client.get_user_tweets(user.id, 'Tweets')

    for t in tweets[:2]:
        print(t.text)


if __name__ == "__main__":
    asyncio.run(main())


# rm -rf **/__pycache__/
# python -m monitor.influencer_monitor
