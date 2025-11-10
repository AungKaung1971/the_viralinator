import os
import json
import sqlite3
from pathlib import Path
from datetime import datetime, timezone
import logging
from typing import List, Dict, Optional
import snscrape.modules.twitter as sntwitter


def get_usernames():
    print("Enter Target Usernames: ")

    usernames = []
    while True:
        username = input("> ").strip()
        if username == "done":
            break
        elif username:
            usernames.append(username)

    return usernames


if __name__ == "__main__":
    target_usernames = get_usernames()
    print("Usernames chosen:", target_usernames)

sntwitter.TwitterSearchScraper('from:')
