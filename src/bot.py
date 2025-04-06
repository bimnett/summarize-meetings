import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from datetime import datetime as dt
import pytz
from summarize import generate_summary
from utils import get_meeting_duration_minutes

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Ensure the /app/data directory exists
os.makedirs("/app/data", exist_ok=True)

# Setup discord bot
intents = discord.Intents.default()
intents.voice_states = True
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)


# Keep track of which channel id a meeting was called from
recording_channels: dict[int, int] = {}
# Keep track of cancelled recordings for servers.
cancel_recordings = set()
# Keep track of meeting start times
meeting_start_times: dict[int, dt] = {}


# Define standard timezone as Europe/Stockholm
swedish_timezone = "Europe/Stockholm"


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")


async def finished_recording(sink, channel: discord.VoiceChannel):
    try:

        # Check if recording should be cancelled
        if channel.guild.id in cancel_recordings:
            cancel_recordings.remove(channel.guild.id)
            return

        # Get text channel where meeting was called in
        text_channel_id = recording_channels[channel.guild.id]
        text_channel = bot.get_channel(text_channel_id)

        audio_file_path = f"/app/data/meeting_{channel.id}_{dt.now().strftime('%Y%m%d_%H%M%S')}.wav"
        
        # Get meeting duration
        start_time = meeting_start_times.get(channel.guild.id)
        end_time = dt.now(pytz.timezone(swedish_timezone))
        meeting_duration_minutes = get_meeting_duration_minutes(start_time, end_time)

        # Create audio file
        audio_file_path = f"recorded_audio_{channel.id}.wav"
        with open(audio_file_path, "wb") as f:
            for audio in sink.audio_data.values():
                f.write(audio.file.getbuffer())

        # Get meeting summary in text
        summary = await generate_summary(audio_file_path, meeting_duration_minutes, start_time, end_time)
        await text_channel.send(summary)

    except FileNotFoundError:
        await channel.send("Audio file not found.")
    except discord.DiscordException as e:
        await channel.send(f"Discord error: {e}")
        print(f"Discord error: {e}")
    except Exception as e:
        await channel.send(f"An unexpected error occurred: {e}")
        print(f"Error in finished_recording: {e}")


@bot.slash_command(name="cancel", description="Cancels the current recording in your voice channel")
async def cancel(ctx):
    await ctx.defer()
    try:     
        if ctx.voice_client:
            cancel_recordings.add(ctx.guild.id)
            await ctx.voice_client.disconnect()
            await ctx.followup.send("Recording was successfully cancelled.")
        else:
            await ctx.followup.send("App is currently not recording.")
    except Exception as e:
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.followup.send("Error cancelling the recording.")


@bot.slash_command(name="end_meeting", description="Stops recording audio in your voice channel and gets summary")
async def end_meeting(ctx):
    await ctx.defer()
    if ctx.voice_client:
        try:
            await ctx.followup.send("The recording has ended and a summary is being generated. This may take a few minutes.")
            await ctx.voice_client.disconnect()
        except Exception as e:
            await ctx.followup.send("There was an error while ending the meeting.")
            print(f"Error: {e}")
            if ctx.voice_client:
                await ctx.voice_client.disconnect()
    else:
        await ctx.followup.send("App is currently not recording.")



@bot.slash_command(name="start_meeting", description="Start recording audio in your voice channel")
async def start_meeting(ctx):
    await ctx.defer()
    try:
        # Check if author is not in a voice channel
        if not ctx.author.voice:
            return await ctx.followup.send("You are not connected to a voice channel.")
        
        # Define channel id to join
        channel = ctx.author.voice.channel

        # Check if the bot is already in the specified voice channel
        if ctx.voice_client:
            if ctx.voice_client.channel.id != channel.id:
                await ctx.voice_client.disconnect()
                voice_client = await channel.connect()
            else:
                return await ctx.followup.send("Already in this voice channel.")

        # Join the voice channel
        voice_client = await channel.connect()
        await ctx.followup.send(f"Joined {channel.name} and started recording the meeting.")
        
        # Add guild id to recording_channels dict
        recording_channels[ctx.guild.id] = ctx.channel.id
        # Add starting time for meeting
        meeting_start_times[ctx.guild.id] = dt.now(pytz.timezone(swedish_timezone))

        # Start recording meeting
        voice_client.start_recording(
            discord.sinks.WaveSink(),
            finished_recording,
            channel
        )

    except Exception as e:
        await ctx.followup.send(f"Error starting meeting: {str(e)}")
        print(f"Error in start_meeting: {e}")
        if ctx.voice_client:
            await ctx.voice_client.disconnect()

if __name__ == "__main__":
    try:
        bot.run(TOKEN)
    except discord.LoginFailure:
        print("Invalid token provided.")