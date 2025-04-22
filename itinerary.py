import google.generativeai as genai

def generate_itinerary(destination, budget, preferences, climate, landscape, transport):
    """Generates a 5-day travel itinerary using Generative AI."""
    prompt = f"""
    You are an expert AI travel planner.

    Create a 5-day travel itinerary for a destination: {destination}.
    Details:
    - Budget: {budget}
    - Climate: {climate}
    - Landscape: {landscape}
    - Preferred Mode of Transport: {transport}
    - Traveler Preferences: {preferences}

    Include:
    1. Suitable transport options
    2. Famous tourist spots
    3. Popular local foods
    4. Recommended hotels under budget
    5. Packing tips based on climate
    6. Ideal trip length (within budget)
    7. Extra tips and hidden gems
    """

    try:
        response = genai.GenerativeModel("gemini-2.0-flash").generate_content(prompt)
        if response and hasattr(response, "text"):
            itinerary = response.text.strip()
            print(f"DEBUG: Generated Itinerary - {itinerary}")  # ✅ Print before returning
            return itinerary
        else:
            return "❌ ERROR: AI response is empty."
    except Exception as e:
        return f"❌ ERROR: Unable to generate itinerary. Reason: {str(e)}"

# ✅ Debugging Test
if __name__ == "__main__":
    sample_itinerary = generate_itinerary("Paris", 50000, "Adventure, seafood", "Sunny", "Sea", "Flight")
    print(f"Generated Itinerary:\n{sample_itinerary}")
