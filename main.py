import discord
from discord.ext import commands
import os
import csv
from datetime import datetime
import zoneinfo

# --- load env
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))

# --- Start bot
bot = discord.Client(intents=discord.Intents.default())

# --- Timezone logic
MY_TIMEZONE = zoneinfo.ZoneInfo("America/Los_Angeles")
current_hour = datetime.now(MY_TIMEZONE).hour

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    channel = bot.get_channel(CHANNEL_ID)
    
    if not channel:
        print("Channel not found!")
        await bot.close()
        return

    with open("problems.csv", "r") as f:
        problems = list(csv.reader(f))

    start_date = datetime(2024, 1, 1, tzinfo=MY_TIMEZONE)
    now = datetime.now(MY_TIMEZONE)
    i = (now - start_date).days % len(problems)

    if current_hour == 5:
        embed = discord.Embed(title="Problem", description=problems[i][0], color=discord.Color.green())
        await channel.send(embed=embed)
    elif current_hour == 0:
        embed = discord.Embed(title="Answer", description=problems[(i-1) % len(problems)][1], color=discord.Color.blue())
        await channel.send(embed=embed)
    else:
        await channel.send("click")

    print("Task complete. Shutting down.")
    await bot.close() 

bot.run(TOKEN)