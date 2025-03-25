from datetime import datetime as dt

# Gets current date in the format "29 of January, 2025"
def get_formatted_date() -> str:
    now = dt.now()
    day = now.day
    month = now.strftime("%B")  # Full month name
    year = now.year

    # Add ordinal suffix to the day
    if 10 <= day % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')

    formatted_date = f"{day}{suffix} of {month}, {year}"
    return formatted_date

# Calculates meeting duration based on a given start time
def get_meeting_duration_minutes(meeting_start_time: dt | None) -> str:
    try:
        total_duration = dt.now() - meeting_start_time
        duration_minutes = int(total_duration.total_seconds() / 60)
        return f"{duration_minutes} minutes" if duration_minutes != 1 else f"{duration_minutes} minute"
    except TypeError:
        return f"Unknown"
    except Exception as e:
        print(f"Unexpected error: {e}")
        return "Unknown"
    
# Parses and formats Gemini response for a meeting summary
def format_gemini_response(summary: str) -> str:
    if not summary.startswith('#'):
        counter_front = 1
        counter_back = -1
        # Count redundant characters from the start
        while summary[counter_front] != '\n':
            counter_front += 1
        
        # Count redundant characters from the back
        while summary[counter_back] != '.':
            counter_back -= 1
    
        # Remove redundant characters from both ends of the summary
        summary = summary[counter_front:counter_back] + '.'

    return summary