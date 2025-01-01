import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key= os.getenv("gemini_key"))

def send_request(query):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(query, generation_config=genai.types.GenerationConfig(max_output_tokens=50))
    return response.text
