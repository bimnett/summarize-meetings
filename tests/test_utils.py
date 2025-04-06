import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import unittest
from datetime import datetime as dt
from utils import get_formatted_date, get_meeting_duration_minutes, format_gemini_response

class TestDateFunctions(unittest.TestCase):

    def test_get_formatted_date_normal(self):
        mock_datetime = dt(2025, 1, 29, 12, 0, 0)
        result = get_formatted_date(mock_datetime)
        self.assertEqual(result, "29th of January, 2025")

        mock_datetime = dt(2024, 7, 16)
        result = get_formatted_date(mock_datetime)
        self.assertEqual(result, "16th of July, 2024")


    def test_get_meeting_duration_minutes_normal(self):
        start_time = dt(2024, 1, 1, 12, 0, 0)
        end_time = dt(2024, 1, 1, 13, 5, 0)
        result = get_meeting_duration_minutes(start_time, end_time)
        self.assertEqual(result, "1 hour and 5 minutes.")

        start_time = dt(2025, 4, 11, 12, 0, 0)
        end_time = dt(2025, 4, 11, 14, 35, 0)
        result = get_meeting_duration_minutes(start_time, end_time)
        self.assertEqual(result, "2 hours and 35 minutes.")

    
    def test_get_meeting_duration_minutes_malformed_input(self):
        start_time = dt(2025, 4, 11, 12, 0, 0)
        result = get_meeting_duration_minutes(start_time, None)
        self.assertEqual(result, "Unknown")

        
    def test_format_gemini_response_normal(self):
        summary1 = "'```3Some text\nMore text. This is a summary.'''``''''"
        result1 = format_gemini_response(summary1)
        self.assertEqual(result1, "More text. This is a summary.")

        summary2 = "#This is a summary."
        result2 = format_gemini_response(summary2)
        self.assertEqual(result2, "#This is a summary.")

        summary3 = "A\nB. C."
        result3 = format_gemini_response(summary3)
        self.assertEqual(result3, "B. C.")

        summary4 = "123456789\nabcdefg. test."
        result4 = format_gemini_response(summary4)
        self.assertEqual(result4, "abcdefg. test.")

if __name__ == '__main__':
    unittest.main()