import os
from dotenv import load_dotenv

load_dotenv()

openAI_key = os.getenv("OPENAI_API_KEY")
data_base_path = "data/viralinator.db"
