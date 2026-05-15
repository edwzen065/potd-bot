import discord
from discord.ext import commands,tasks
import logging
from dotenv import load_dotenv
import os
import zoneinfo
from datetime import time
import csv

# --- logging
handler = logging.FileHandler(filename='discord.log',encoding='utf-8',mode='w')

# --- load env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))

# --- start bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

# --- problems logic
i = 0
num_problems = 0
problems = []

# --- unpack csv
with open("problems.csv", "r") as f:
    csv_reader = csv.reader(f)
    for row in csv_reader:
        problems.append((row[0],row[1]))
        num_problems+=1

# --- time loop
MY_TIMEZONE = zoneinfo.ZoneInfo("America/Los_Angeles")
@tasks.loop(time=time(hour=23, minute=19, tzinfo=MY_TIMEZONE))
async def question():
    global i
    channel = bot.get_channel(CHANNEL_ID)

    # Logic to send the fancy embed
    embed = discord.Embed(
        title=f"Problem {i+1}",
        description = problems[i][0],
        color=discord.Color.green()
    )
    
    if channel:
        await channel.send(embed=embed)
    
    # Also print to your console for tracking
    print(f"Question failed successfully!!")

@tasks.loop(time=time(hour=23, minute=20, tzinfo=MY_TIMEZONE))
async def answer():
    global i
    channel = bot.get_channel(CHANNEL_ID)

    # Logic to send the fancy embed
    embed = discord.Embed(
        title=f"Answer to Problem {i+1}",
        description = problems[i][1],
        color=discord.Color.green()
    )
    
    if channel:
        await channel.send(embed=embed)
    
    # Also print to your console for tracking
    print(f"Answer failed successfully!!")

    i = (i+1) % len(problems)

# --- startup
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    # Start the loop as soon as the bot is online
    question.start()
    answer.start()

bot.run(TOKEN)