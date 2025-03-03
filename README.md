A Discord bot designed to facilitate remote meetings by joining voice channels, recording audio 
sessions, and generating meeting summaries.

## Features

* **Voice Channel Joining**: Joins specified voice channels for meetings.
* **Audio Recording**: Records audio from the joined voice channel until the meeting is ended.
* **Meeting Summary Generation**: Generates a summary of the recorded meeting in the form of written notes.

## Installation and Setup

To use this bot, follow these steps:

1. Fork this repository to create your own copy.
2. (Optional) Setup a [virtual environment](https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/)
3. Install the required dependencies by running `pip install --no-cache-dir -r requirements.txt`.
4. Configure the bot's settings in the `.env` file by modifying the `GEMINI_API_KEY` and `TOKEN` variables.

## Running the Bot

To run the bot, execute the following command:
```bash
python bot.py
```
This will start the bot and begin listening for commands.

## Commands

The bot responds to the following commands:

* `/start_meeting`: Joins the voice channel that the author is currently in, and starts an audio recording session
* `/end_meeting`: Ends the current audio recording session and generates meeting summary notes.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT). See `LICENSE` file for 
details.