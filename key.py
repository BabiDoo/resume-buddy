#validating model key

import os
from dotenv import load_dotenv

def get_api_key():
    load_dotenv()  
    key = os.getenv("LANGEXTRACT_API_KEY")
    if not key:
        key = os.getenv("GOOGLE_API_KEY")
    if not key:
        raise RuntimeError(
            "Define LANGEXTRACT_API_KEY @ .env (or GOOGLE_API_KEY on envirollment)."
        )
    return key


