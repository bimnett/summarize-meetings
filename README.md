<h1 align="center"> Meeting Summarizer </h1>

<p align="center">
    <img src="./images/readme/Icon_2000x2000.jpg" height=350 width=350/>
</p>

<p align="center">
    <a href="https://www.freepik.com/free-vector/hand-drawn-flat-paper-cartoon-illustration_156119334.htm#fromView=search&page=1&position=3&uuid=1864ad44-9394-48df-ac88-0bc376a0059b&query=Mascot+notes">Designed by Freepik</a>
</p>

&nbsp;

A Discord bot designed that facilitates remote meetings by joining voice channels, recording audio 
sessions, and generating meeting summaries.

## Features

* **Audio Recording**: Joins a voice channel and records audio until the meeting has ended.
* **Meeting Summary Generation**: Generates a summary of the recorded meeting in the form of written notes.

## Installation and Setup

To host this bot locally, there are two recommended installation methods.

Prerequisites:
* Python (3.7 or higher)
* [Setting up a bot on Discord's developer portal](./docs/SetupDiscordBot.md)
* [A Google Gemini API key](https://ai.google.dev/gemini-api/docs/api-key)
* Docker (only for docker option)

&nbsp;

**Option 1: Docker (Recommended)**

Using Docker simplifies the setup and ensures a consistent environment.

1.  **Fork and Clone the Repository:**
    ```bash
    git clone <your-repository-url>
    cd <repository-directory>
    ```
2.  **Create a `.env` file in the root directory:**
    * Copy and paste the contents of `.env.example`
    * Replace `<your_gemini_api_key>` and `<your_discord_bot_token>` with your Gemini and Discord API keys.
3.  **Run the Docker Service:**
    ```bash
    docker-compose up --build
    ```

**Option 2: Local Python Environment**

If you prefer a local setup:

1.  **Fork and clone this Repository:**
    Fork and clone this repository to create your own copy.
2.  **(Optional but recommended) Setup a [Virtual Environment](https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/)**
3.  **Install Dependencies:**
    Install the required dependencies by running
    ```bash
    cd src && pip3 install --no-cache-dir -r requirements.txt
    ```
4.  **Configure `.env` File:**
    Configure the bot's settings in the `.env` file by modifying the `GEMINI_API_KEY` and `DISCORD_BOT_TOKEN` variables.
5.  **Run the Bot:**
    ```bash
    python -u bot.py
    ```

## Commands

The bot responds to the following commands:

* `/start_meeting`: Joins the voice channel that the author is currently in, and starts an audio recording session
* `/end_meeting`: Ends the current audio recording session and generates meeting summary notes.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT). See `LICENSE` file for 
details.