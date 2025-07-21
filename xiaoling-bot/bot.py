import discord
from discord.ext import commands

# prefix to run a command for Xiaoling bot.
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

keys = {}

with open('keys.txt', 'r') as file:
    for line in file:
        if '=' in line:
            key, value = line.strip().split('=',1)
            if value.isdigit():
                keys[key] = int(value)
            else:
                keys[key] = value

# print (keys['BOT_TOKEN'])
# print (keys['CHANNEL_ID'])

# intents = discord.Intents.default()
# intents.message_content = True

# client = MyClient(intents=intents)

# ------------- EVENTS ------------------
@bot.event
async def on_ready():
    print(f'Logged on as {bot.user}!')
    channel = bot.get_channel(keys['CHANNEL_ID'])
    await channel.send("Hello, I am at your service!")

@bot.command()
async def hello(ctx):
    await ctx.send("Hello! :)")
# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return

    # if message.content.startswith('$hello'):
    #     await message.channel.send('Hello!')

# client.run(BOT_TOKEN)

bot.run(keys['BOT_TOKEN'])