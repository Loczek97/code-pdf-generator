import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AIService:
    @staticmethod
    def generate_description(code: str) -> str:
        api_key = os.getenv("GEMINI_API_KEY")
        
        if not api_key or "your_api_key_here" in api_key:
            return (
                "AI Description Unavailable: No API Key provided.\n"
                "Please set GEMINI_API_KEY in the .env file."
            )

        try:
            genai.configure(api_key=api_key)
            # User requested 2.5-flash which is available in this environment
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            prompt = (
                "Przeanalizuj poniższy fragment kodu i podaj krótkie, profesjonalne podsumowanie techniczne "
                "opisujące jego cel i kluczową logikę. Odpowiedz w języku polskim. Ogranicz się do 3 zdań.\n\n"
                f"Code:\n{code[:2000]}"  # Limit context window just in case
            )
            
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"AI Generation Failed: {str(e)}"
