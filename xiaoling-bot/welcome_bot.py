import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
keys = {}

#reading key txt file

with open('keys.txt', 'r') as file:
    for line in file:
        if '=' in line:
            key, value = line.strip().split('=',1)
            if value.isdigit():
                keys[key] = int(value)
            else:
                keys[key] = value
                


#events

@bot.event
async def on_member_join(member):
    
    channel = bot.get_channel(keys['CHANNEL_ID'])
    await channel.send(f"Welcome {member.mention}!")
    









bot.run(keys['BOT_TOKEN'])
