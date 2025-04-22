import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key from environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Ensure API key is set correctly
if not api_key:
    print("❌ ERROR: API key not found! Set GOOGLE_API_KEY in your .env file.")
    exit()

# Configure the API key
genai.configure(api_key=api_key)

# Initialize the Google Generative AI model
model = genai.GenerativeModel("gemini-2.0-flash")

def generate_detailed_itinerary(days, budget, climate, landscape, transport, interests):
    """
    AI selects ONE travel destination based on user preferences and generates a full itinerary.
    """
    prompt = f"""
    **🎒 AI-Powered Travel Itinerary**  

    **📍 Step 1: AI-Suggested Travel Destination**  

    Based on the following user preferences:  
    - **Budget:** _{budget}_  
    - **Climate Preference:** _{climate}_  
    - **Landscape Type:** _{landscape}_  
    - **Preferred Transport:** _{transport}_  
    - **Interests:** _{interests}_  

    🏆 **AI selects the most ideal travel destination!**  

    **📌 Step 2: Full {days}-Day Travel Itinerary for the Suggested Destination**  

    ---  

    **🗓️ Day-by-Day Plan**  

    **🌅 Morning:**  
    - Must-visit **landmarks**, sightseeing, and nature spots.  

    **🏛️ Afternoon:**  
    - Museums, cultural experiences, and adventure activities.  

    **🌆 Evening:**  
    - Local **cuisine**, nightlife, and entertainment options.  

    ---  

    **🍽️ Must-Try Foods**  

    - List **famous dishes** and where to find them!  

    ---  

    **🏨 Top Hotels**  

    - Recommend **budget/mid-range/luxury stays**, including prices & unique features.  

    ---  

    **🎒 Packing Essentials**  

    - **Weather-based clothing & travel necessities** to ensure comfort.  

    ---  

    **📅 Best Time to Visit**  

    - **Ideal months** based on climate, seasonal festivals, and affordability.  

    ---  

    📝 **Ensure the itinerary is structured, engaging, and personalized for travelers!**  
    """

    try:
        response = model.generate_content(prompt)
        if response and hasattr(response, "text"):
            return response.text.strip()
        else:
            return "❌ ERROR: AI response is empty."
    except Exception as e:
        return f"❌ ERROR: Unable to generate itinerary. Reason: {str(e)}"
