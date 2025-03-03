import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from summarize import generate_summary


# Setup env variables
load_dotenv()
TOKEN = os.getenv("TOKEN")


# Setup discord bot
intents = discord.Intents.default()
intents.voice_states = True
intents.message_content = True # Required for command detection
bot = commands.Bot(command_prefix="/", intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")


async def finished_recording(sink, channel: discord.VoiceChannel):
    try:
        # Store participating users. Only stores users present during the end of the meeting.
        recorded_users = [f"<@{user_id}>" for user_id, audio in sink.audio_data.items()]
        print(f"Finished recording in {channel.name}, recorded users: {', '.join(recorded_users)}")

        # Create audio file
        audio_file_path = f"recorded_audio_{channel.id}.wav"
        with open(audio_file_path, "wb") as f:
            for audio in sink.audio_data.values():
                f.write(audio.file.getbuffer())


        summary = await generate_summary(audio_file_path)
        await channel.send(summary)

        # Delete audio file after it has been processed
        if os.path.exists(audio_file_path):
            os.remove(audio_file_path)

    except FileNotFoundError:
        await channel.send("Audio file not found.")
    except discord.DiscordException as e:
        await channel.send(f"Discord error: {e}")
        print(f"Discord error: {e}")
    except Exception as e:
        await channel.send(f"An unexpected error occurred: {e}")
        print(f"Error in finished_recording: {e}")


@bot.slash_command(name="end_meeting", description="Stops recording audio in your voice channel")
async def end_meeting(ctx):
    if ctx.voice_client:
        try:
            ctx.voice_client.stop_recording()
            await ctx.send("Meeting recording ended and summary is being generated.")
        except Exception as e:
            await ctx.send(f"Error ending meeting: {e}")
    else:
        await ctx.send("Bot is not currently recording in this channel.")



@bot.slash_command(name="start_meeting", description="Start recording audio in your voice channel")
async def start_meeting(ctx):
    try:
        # Check if author is not in a voice channel
        if not ctx.author.voice:
            return await ctx.send("You are not connected to a voice channel.")
        
        # Define channel id to join
        channel = ctx.author.voice.channel

        # Check if the bot is already in the specified voice channel
        if ctx.voice_client:
            if ctx.voice_client.channel.id != channel.id:
                await ctx.voice_client.disconnect()
                voice_client = await channel.connect()
            else:
                return await ctx.send("Already in this voice channel.")

        # Join the voice channel
        voice_client = await channel.connect()
        await ctx.send(f"Joined {channel.name} and started recording the meeting.")
        
        # Start recording meeting
        voice_client.start_recording(
            discord.sinks.WaveSink(),
            finished_recording,
            channel
        )

    except Exception as e:
        await ctx.send(f"Error starting meeting: {str(e)}")
        print(f"Error in start_meeting: {e}")


if __name__ == "__main__":
    try:
        bot.run(TOKEN)
    except discord.LoginFailure:
        print("Invalid token provided.")