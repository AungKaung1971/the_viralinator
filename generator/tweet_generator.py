import sqlite3
import datetime
from openai import OpenAI
from config import openAI_key, data_base_path


client = OpenAI(api_key=openAI_key)

print("OpenAI SDK version:", getattr(OpenAI, "__version__", "old SDK"))


def generate_tweets(n=5, niche="tech"):
    prompt = f"""You are a sharp, observant {niche} pundit and commentator. You cover trending topics.

Give me {n} tweets based on below.

Alternate between:

- **Tech takes:** Confident, witty, opinionated comments on trending or high-engagement tech topics (AI, startups, VC, design, product culture, Apple, Tesla, etc.). Be analytical, slightly cynical, but smart.
- **Life takes:** Dry, observational, day-to-day thoughts about people, ambition, timing, attention, or irony in modern life. Never “motivational.” Never corny. Aim for insight with a smirk.

**Tone:**

- Calm, confident, slightly detached.
- Humor should be *quietly clever*, not loud or jokey.
- Never neutral — have an opinion.
- No emojis, no hashtags, no buzzwords.
- Max 280 characters.
- If relevant, add 1 credible link for tech posts.

**Output format:**

  Type: “tech” or “life”

 Post text
"""

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[{"role": "user", "content": prompt}],
    )
    tweets = response.choices[0].message.content.split("\n")

    cleaned = [t.strip() for t in tweets if t.strip()
               and not t.strip(). startswith("Type:")]

    return cleaned


def save_tweets(tweets):
    conn = sqlite3.connect(data_base_path)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS tweets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL
        )
    """)

    cur.execute("DELETE FROM tweets")
    cur.execute("DELETE FROM sqlite_sequence WHERE name='tweets'")

    for tweet in tweets:
        cur.execute("INSERT INTO tweets (content) VALUES (?)", (tweet,))
    conn.commit()
    conn.close()


if __name__ == "__main__":
    tweets = generate_tweets()
    save_tweets(tweets)
    print(
        f"Saved {len(tweets)} tweets to database at {datetime.datetime.now()}")


# run code  = python3 -m generator.tweet_generator

# view code  = sqlite3 data/tweetinator.db "SELECT * FROM tweets;"

# clearing cache = rm -rf **/__pycache__/
