BOT_TOKEN = ''
CHANNEL_ID = 

import discord

# class MyClient(discord.Client):
#     async def on_ready(self):
#         print(f'Logged on as {self.user}!')

#     async def on_message(self, message)
#         print(f'Message from {message.author}: {message.content}')

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)

# ------------- EVENTS ------------------
@client.event
async def on_ready():
    print(f'Logged on as {client.user}!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run(BOT_TOKEN)