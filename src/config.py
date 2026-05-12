import os
from dotenv import load_dotenv
load_dotenv()

DB_PATH = os.getenv("DB_PATH", "data/bank_compliance.db")
DATA_PATH = os.getenv("DATA_PATH", "data/raw/transactions.csv")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = "llama-3.1-8b-instant"
RANDOM_SEED = 42
CONTAMINATION_RATE = 0.05
TEST_SIZE = 0.2
