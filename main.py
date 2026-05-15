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
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

# --- Timezone logic
MY_TIMEZONE = zoneinfo.ZoneInfo("America/Los_Angeles")
current_hour = datetime.now(MY_TIMEZONE).hour

# with open("counter.txt", 'rw') as f:
#     counter = int(f.read())-1
#     f.write(counter)
counter = 1

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

    if current_hour == 5:
        # Send Question
        embed = discord.Embed(title="Problem", description=problems[counter+1][0], color=discord.Color.green())
        await channel.send(embed=embed)
    else:
        # Send Answer
        embed = discord.Embed(title="Answer", description=problems[counter+1][1], color=discord.Color.blue())
        await channel.send(embed=embed)

    # 3. THE MOST IMPORTANT PART FOR CRON
    print("Task complete. Shutting down.")
    await bot.close() 

bot.run(TOKEN)