import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')

if not api_key:
    print("API Key not found in .env")
else:
    genai.configure(api_key=api_key)
    try:
        models = [m.name for m in genai.list_models() if 'embedContent' in m.supported_generation_methods]
        print(f"Available embedding models: {models}")
    except Exception as e:
        print(f"Error: {e}")
