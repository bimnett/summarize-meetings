from dotenv import load_dotenv
import os
from google import genai
from utils import *
from datetime import datetime as dt

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Generates a summary from an audio file.
async def generate_summary(audio_file_path: str, duration_minutes: str, start_time: dt, end_time: dt) -> str:
    summary = await _run_gemini(audio_file_path, duration_minutes, start_time, end_time)
    if not summary:
        return "There was an error generating a summary."
    return summary
    

# Sends audio file to the Google Gemini API. Returns a summary of the audio file
async def _run_gemini(audio_file_path: str, duration_minutes: str, start_time: dt, end_time: dt) -> str:

    try:
        # Initialize Gemini client
        gemini = genai.Client(api_key=GEMINI_API_KEY)

        # Define gemini model to use
        gemini_model = "gemini-2.0-flash"

        # Upload audio file to Gemini file API
        audio_file = gemini.files.upload(file=audio_file_path)

        # Define system/user prompt
        prompt = f"""Summarize the provided meeting audio. Only include relevant, non-discriminatory notes. 
            The current date is {get_formatted_date(dt.now())}, and the meeting duration is {duration_minutes}. 
            The meeting started at {start_time.strftime("%H:%M")}, and ended at {end_time.strftime("%H:%M")} ({get_utc_timezone(start_time)}).
            Use this markdown format, and fill in the date, duration, start and end time, and the summary:
            # Meeting Summary
            ### Topic: <topic>
            ### Date: <date>
            ### Duration: ≈ <duration>
            ### Start/end time: <start_time> - <end_time> (<timezone>)
            ### Summary:
            <summary>

            Your response must only contain the summary, enclosed in a multi-line code block.
            """

        # Send request
        summary = gemini.models.generate_content(
            model=gemini_model,
            contents=[prompt, audio_file]
        )

        # Delete audio file locally and Google's file API after it has been processed
        if os.path.exists(audio_file_path):
            os.remove(audio_file_path)
        gemini.files.delete(name=audio_file.name)

        formatted_response = format_gemini_response(summary.text)
        return formatted_response
    
    except Exception as e:
        print(f"Error in _run_gemini: {e}")
        return None
    