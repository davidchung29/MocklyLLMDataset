import os
from dotenv import load_dotenv

load_dotenv() 
api_key = os.getenv("OPENROUTER_API_KEY")

if api_key:
    print("success")
else:
    print("failed")
