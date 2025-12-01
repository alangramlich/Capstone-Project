import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

print("--- API Key Test Script ---")

try:
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key or api_key == "YOUR_API_KEY_HERE":
        print("❌ ERROR: GOOGLE_API_KEY not found or not set in the .env file.")
        print("Please make sure your .env file contains your actual API key.")
    else:
        print("✅ API Key found in environment.")
        genai.configure(api_key=api_key)
        
        print("⏳ Listing available Gemini models...")
        available_models = []
        for m in genai.list_models():
            if "generateContent" in m.supported_generation_methods:
                available_models.append(m.name)
                print(f"   - Found available model: {m.name}")

        if not available_models:
            print("❌ ERROR: No models found that support 'generateContent' with this API key.")
        else:
            # Try to use the first available model that supports generateContent
            model_to_use = available_models[0]
            print(f"✅ Using the first available model: {model_to_use}")

            print(f"⏳ Attempting to create model '{model_to_use}'...")
            model = genai.GenerativeModel(model_to_use)
            
            print("⏳ Generating content with the API...")
            response = model.generate_content("Tell me a short, one-sentence joke.")
            
            print("\n✅ SUCCESS! The API key is working and a model is accessible.")
            print("Response from Gemini:", response.text)

except Exception as e:
    print(f"\n❌ ERROR: An error occurred while testing the API key.")
    print("-------------------------------------------------")
    print(e)
    print("-------------------------------------------------")
    print("This likely means the key is invalid or the API is not enabled correctly in your Google Cloud project.")

