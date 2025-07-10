"""
this script loads the openrouter api key from the environment
and prints 'success' if the key is found, or 'failed' if not
"""

import os
from dotenv import load_dotenv

load_dotenv() 
api_key = os.getenv("OPENROUTER_API_KEY")

if api_key:
    print("success")
else:
    print("failed")
