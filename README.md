A Discord bot designed to facilitate remote meetings by joining voice channels, recording audio 
sessions, and generating meeting summaries.

## Features

* **Voice Channel Joining**: Joins specified voice channels for meetings.
* **Audio Recording**: Records audio from the joined voice channel until the meeting is ended.
* **Meeting Summary Generation**: Generates a summary of the recorded meeting in the form of written notes.

## Installation and Setup

To host this bot locally, you have two recommended installation methods:

**Option 1: Docker (Recommended)**

Using Docker simplifies setup and ensures a consistent environment.

1.  **Clone the Repository:**
    ```bash
    git clone <your-repository-url>
    cd <repository-directory>
    ```
2.  **Build the Docker Image:**
    ```bash
    docker build -t meeting-summary-bot .
    ```
3.  **Run the Docker Container:**
    ```bash
    docker run -e GEMINI_API_KEY=<your_gemini_api_key> -e TOKEN=<your_discord_bot_token> meeting-summary-bot
    ```
    * Replace `<your_gemini_api_key>` and `<your_discord_bot_token>` with your actual API key and bot token.
    * If you need to mount a local `.env` file, use the `-v` flag: `docker run -v $(pwd)/.env:/app/.env -e GEMINI_API_KEY=<your_gemini_api_key> -e TOKEN=<your_discord_bot_token> meeting-summary-bot`

**Option 2: Local Python Environment**

If you prefer a local setup:

1.  **Fork this Repository:**
    Fork this repository to create your own copy.
2.  **(Optional but recommended) Setup a [Virtual Environment](https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/)**
3.  **Install Dependencies:**
    Install the required dependencies by running `pip install --no-cache-dir -r requirements.txt`.
4.  **Configure `.env` File:**
    Configure the bot's settings in the `.env` file by modifying the `GEMINI_API_KEY` and `TOKEN` variables.
5.  **Run the Bot:**
    ```bash
    python -u bot.py

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