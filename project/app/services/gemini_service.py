import google.generativeai as genai
import os
from dotenv import load_dotenv
#here we load dotenv
load_dotenv()

#apikey 
apiKey = os.getenv('Google_API_Key')

if not apiKey:
    print("fail to load")
    raise ValueError("GOOGLE_API_KEY not found in environment variable")
else:
    print("successfully load api")

genai.configure(apiKey=apiKey)
