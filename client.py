#!/usr/bin/env python3
import os
import sys
from google import genai

# === shared client initialization ===
API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    print("Error: Please set the GEMINI_API_KEY environment variable.")
    sys.exit(1)

client = genai.Client(api_key=API_KEY)
MODEL  = "gemini-2.0-flash"
