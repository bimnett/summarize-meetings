from dotenv import load_dotenv
import os
from google import genai
from utils import get_formatted_date

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Generates a summary from an audio file.
async def generate_summary(audio_file_path: str, duration_minutes: int | str) -> str:
    summary = await _run_gemini(audio_file_path, duration_minutes)
    return summary
    

# Sends audio file to Google Gemini's API. Returns a summary of the audio file
async def _run_gemini(audio_file_path: str, duration_minutes: int | str) -> str:

    try:
        # Initialize Gemini client
        gemini = genai.Client(api_key=GEMINI_API_KEY)

        # Define gemini model to use
        gemini_model = "gemini-2.0-flash"

        # Upload audio file to Gemini file API
        audio_file = gemini.files.upload(file=audio_file_path)

        # Define system/user prompt
        prompt = f"""Summarize the provided meeting audio. Only include relevant, non-discriminatory notes. 
            The current date is {get_formatted_date()}, and the meeting duration is {duration_minutes} minutes. 
            Use this markdown format, and fill in the date and duration, but prepend the format with 2 new lines:
            # Meeting Summary
            ### Topic: <topic>
            ### Date: <date>
            ### Duration: <duration> minutes
            ### Summary:
            <summary>
            Your response can not have anything else in it but the summary.
            """

        # Send request
        summary = gemini.models.generate_content(
            model=gemini_model,
            contents=[prompt, audio_file]
        )

        # Print total token count used for prompt
        print(f"Total token count: {summary.usage_metadata.total_token_count}")

        # Delete audio file locally and Google's file API after it has been processed
        if os.path.exists(audio_file_path):
            os.remove(audio_file_path)
        gemini.files.delete(name=audio_file.name)

        return summary.text
    
    except Exception as e:
        print(f"Error in _run_gemini: {e}")
        return f"Error processing audio with Gemini: {e}"
    