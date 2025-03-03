from dotenv import load_dotenv
import os
from google import genai
import asyncio

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Generates a summary from an audio file.
async def generate_summary(audio_file_path):
    summary = await asyncio.to_thread(_run_gemini, audio_file_path)
    return summary
    

# Sends audio file to Google Gemini's API. Returns a summary of the audio file
def _run_gemini(audio_file_path):

    try:
        # Initialize Gemini client
        gemini = genai.Client(api_key=GEMINI_API_KEY)

        # Define gemini model to use
        gemini_model = "gemini-2.0-flash"

        # Create audio file object
        with open(audio_file_path, "rb"):
            audio_file = audio_file_path.read()

        audio_file = gemini.files.upload(file=audio_file_path)

        # Define system/user prompt
        prompt = """You are a world-class transcript summarizer that never misses a detail. 
                    You will recieve and transcribe an audio file of a meeting, and you will respond with a summary.
                    Make sure to only include notes that are relevant to the meeting."""

        # Send request
        summary = gemini.models.generate_content(
            model=gemini_model,
            contents=[prompt, audio_file]
        )

        return summary.text
    
    except Exception as e:
        print(f"Error in _run_gemini: {e}")
        return f"Error processing audio with Gemini: {e}"