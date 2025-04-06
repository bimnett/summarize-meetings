from datetime import datetime as dt
import pytz

# Gets current date in the format "29 of January, 2025"
def get_formatted_date(date: dt) -> str:
    day = date.day
    month = date.strftime("%B")  # Full month name
    year = date.year

    # Add ordinal suffix to the day
    if 10 <= day % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')

    formatted_date = f"{day}{suffix} of {month}, {year}"
    return formatted_date

# Calculates meeting duration based on a given start time
def get_meeting_duration_minutes(meeting_start_time: dt, meeting_end_time: dt) -> str:
    try:
        total_duration = meeting_end_time - meeting_start_time
        duration_minutes = int(total_duration.total_seconds() / 60)

        # Calculate hours if longer than 60 minutes
        hours = 0
        while duration_minutes >= 60:
            hours += 1
            duration_minutes -= 60
        
        if hours and duration_minutes % 10 != 1:
            return f"{hours} hours and {duration_minutes} minutes." if hours > 1 else f"{hours} hour and {duration_minutes} minutes."
        elif hours and duration_minutes % 10 == 1:
            return f"{hours} hours and {duration_minutes} minute." if hours > 1 else f"{hours} hour and {duration_minutes} minute."

        return f"{duration_minutes} minutes" if duration_minutes != 1 else f"{duration_minutes} minute"
    except TypeError:
        return f"Unknown"
    except Exception as e:
        print(f"Unexpected error: {e}")
        return "Unknown"
    
# Parses and formats Gemini response for a meeting summary
def format_gemini_response(summary: str) -> str:
    if not summary.startswith('#') or summary[-1] != '.':
        counter_front = 1
        counter_back = len(summary)
        # Count redundant characters from the start
        while summary[counter_front - 1] != '\n':
            counter_front += 1
        
        # Count redundant characters from the back
        while summary[counter_back - 1] != '.':
            counter_back -= 1
    
        # Remove redundant characters from both ends of the summary
        summary = summary[counter_front:counter_back]

    return summary

def get_utc_timezone(time: dt) -> str:
    utc_offset = time.strftime("%z")
    offset_sign = utc_offset[0]
    offset_hours = utc_offset[1:3]
    utc_string = f"UTC{offset_sign}{int(offset_hours)}"
    return utc_string