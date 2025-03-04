from datetime import datetime as dt
import contextlib
import wave

# Gets current date in the format "29 of January, 2025"
def get_formatted_date():
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