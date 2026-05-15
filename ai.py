import os
import discord
import logging
from discord.ext import commands, tasks
from dotenv import load_dotenv
from datetime import time
import zoneinfo

# --- 1. SETUP LOGGING ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('discord')

# --- 2. LOAD ENVIRONMENT VARIABLES ---
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))

# --- 3. INITIALIZE BOT ---
# Standard intents (No message_content needed for scheduled tasks)
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# --- 4. THE TIME LOOP ---
# This runs at exactly 2:30 PM (14:30) every day
MY_TIMEZONE = zoneinfo.ZoneInfo("America/Los_Angeles")

@tasks.loop(time=time(hour=22, minute=10, tzinfo=MY_TIMEZONE))
async def daily_print():
    channel = bot.get_channel(CHANNEL_ID)
    
    # Logic to send the fancy embed
    embed = discord.Embed(
        title="⏰ Scheduled Alert",
        description="The daily timer has been triggered!",
        color=discord.Color.green()
    )
    
    if channel:
        await channel.send(embed=embed)
    
    # Also print to your console for tracking
    print(f"Task executed successfully at 14:30")

# --- 5. STARTUP ---
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    # Start the loop as soon as the bot is online
    if not daily_print.is_running():
        daily_print.start()

bot.run(TOKEN)