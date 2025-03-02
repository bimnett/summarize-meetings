A Discord bot designed to facilitate remote meetings by automatically joining voice channels, recording audio 
sessions, and generating meeting summaries.

## Features

* **Voice Channel Joining**: Automatically joins specified voice channels for meetings.
* **Audio Recording**: Records audio from the joined voice channel until the meeting is ended.
* **Meeting Summary Generation**: Generates a summary of the recorded meeting in the form of written notes.

## Installation and Setup
------------------------

To use this bot, follow these steps:

1. Fork this repository to create your own copy.
2. Install the required dependencies by running `pip install -r requirements.txt`.
3. Configure the bot's settings in the `.env` file by modifying the `TOKEN`, `CHANNELS_TO_JOIN`, and `MEETING 
SUMMARYTemplate` variables.

## Running the Bot
------------------

To run the bot, execute the following command:
```bash
python main.py
```
This will start the bot and begin listening for commands.

## Commands
---------

The bot responds to the following commands:

* `/join [channel_id]`: Joins a voice channel with the specified ID.
* `/endmeeting`: Ends the current audio recording session and generates meeting summary notes.

## API Documentation
--------------------

### Discord Bot API

Please refer to the [Discord API documentation](https://discord.com/developers/docs/resources/channel) for more 
information on how to interact with the bot.

## Contributing
------------

Contributions are welcome! Please submit a pull request with any changes, additions, or improvements you'd like 
to make.

## License
-------

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT). See `LICENSE` file for 
details.

---