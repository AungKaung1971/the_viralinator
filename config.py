from pathlib import Path
from dotenv import load_dotenv
import os
print("config.py has been loaded succssfully")


load_dotenv()

env_path = Path(__file__).resolve().parent / ".env"

# if not env_path.exists():
#     env_path = Path(__file__).resolve().parent.parent / ".env"

print("Looking for .env at:", env_path)


openAI_key = os.getenv("OPENAI_API_KEY")
data_base_path = "data/tweetinator.db"

auth_token = os.getenv("AUTH_TOKEN")
cto_token = os.getenv("CTO_TOKEN")

target_users = ["elonmusk", "sama",
                "realDonaldTrump", "joerogan", "TuckerCarlson", "BillGates"]
