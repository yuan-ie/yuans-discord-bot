import discord

keys = {}

with open('keys.txt', 'r') as file:
    for line in file:
        if '=' in line:
            key, value = line.strip().split('=',1)
            if value.isdigit():
                keys[key] = int(value)
            else:
                keys[key] = value

print (keys['BOT_TOKEN'])
print (keys['CHANNEL_ID'])

# class MyClient(discord.Client):
#     async def on_ready(self):
#         print(f'Logged on as {self.user}!')

#     async def on_message(self, message)
#         print(f'Message from {message.author}: {message.content}')

# intents = discord.Intents.default()
# intents.message_content = True

# client = MyClient(intents=intents)

# # ------------- EVENTS ------------------
# @client.event
# async def on_ready():
#     print(f'Logged on as {client.user}!')

# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return

#     if message.content.startswith('$hello'):
#         await message.channel.send('Hello!')

# client.run(BOT_TOKEN)