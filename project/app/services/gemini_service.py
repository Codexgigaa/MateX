import google.generativeai as genai
import os
from dotenv import load_dotenv
import time
#here we load dotenv
load_dotenv()

#apikey 
apiKey = os.getenv('API_key')

if not apiKey:
    print("fail to load")
    raise ValueError("GOOGLE_API_KEY not found in environment variable")
else:
    print("successfully load api")

# 2. Define Configuration
generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 2048,
}

#Initialize the specific model due to cost and speed
model = genai.GenerativeModel(
    model_name = "gemini-2.5-flash",
    generation_config = generation_config
)

def ask_Gemini(User_Prompt, retry=1):
    for i in range(retry):

        try:
            response = model.generate_content(User_Prompt)
            
            if response.candidates:
                return response.text
            else:
                return "Response blocked via safety settings"
        except Exception as e:
            if "429" in str(e) and i < retry -1:
                time.sleep(5)
                continue
            return f"{str(e)}"
# to test that API request does work?
print(ask_Gemini("Hello buddy kesse ho aap?"))

