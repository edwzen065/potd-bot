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

    with open("answerGiven.txt", "r") as f:
        answerGiven, i = [int(el) for el in f.read().strip().split(",")]

    if answerGiven == 1:
        file = discord.File(f"images/{int(problems[i][0]):04d}.png", filename=f"{int(problems[i][0]):04d}.png")
        embed = discord.Embed(title="Problem", color=discord.Color.green())
        embed.set_image(url=f"attachment://{int(problems[i][0]):04d}.png")
        await channel.send(file = file, embed=embed)
        answerGiven = 0
    else:
        embed = discord.Embed(title="Answer", description=problems[i][1], color=discord.Color.blue())
        await channel.send(embed=embed)
        answerGiven = 1

    with open("answerGiven.txt", "w") as f:
        f.write(str(answerGiven)+str(i))

    print("Task complete. Shutting down.")
    await bot.close() 

bot.run(TOKEN)
#testing