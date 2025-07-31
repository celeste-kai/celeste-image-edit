import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
STABILITYAI_API_KEY = os.getenv("STABILITYAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
LUMA_API_KEY = os.getenv("LUMA_API_KEY")
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")