

import os
from dotenv import load_dotenv
from pathlib import Path


load_dotenv()

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

openAI_key = os.getenv("OPENAI_API_KEY")
data_base_path = "data/viralinator.db"

auth_token = os.getenv("AUTH_TOKEN")
cto_token = os.getenv("CTO_TOKEN")
