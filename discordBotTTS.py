import discord
from discord.ext import commands
from gtts import gTTS
from dotenv import find_dotenv,load_dotenv
import os

#bot setup
intents = discord.Intents.default()
intents.message_content = True #Enable message content intent
bot = commands.Bot(command_prefix="!",intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as TextToSpeech")

@bot.command()
async def join(ctx):
    "Bot joins the voice channel."
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send("Joined the voice channel!")
    else:
        await ctx.send("You need to be in a voice channel first")

@bot.command()
async def leave(ctx):
    """Bot leaves the voice channel."""
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Left the voice channel!")
    else:
        await ctx.send("I'm not in a voice channel!")

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
Token = os.getenv("Token")

@bot.command()
async def speak(ctx, *, text):
    """Bot converts text to speech and plays it in the voice channel."""
    if ctx.voice_client:
        # Generate TTS audio
        tts = gTTS(text, lang="en")
        audio_file = "speech.mp3"
        tts.save(audio_file)

        # Play audio
        ctx.voice_client.stop()
        source = discord.FFmpegPCMAudio(audio_file)
        ctx.voice_client.play(source, after=lambda e: os.remove(audio_file))
        await ctx.send(f"Saying: {text}")
    else:
        await ctx.send("I'm not in a voice channel. Use `!join` to bring me to a channel.")

bot.run(Token)