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


#welcomes member upon joining
@bot.event
async def on_member_join(member):
    
    #change to welcome channel ID
    channel = bot.get_channel(keys['CHANNEL_ID'])
    
    
    #embedS
    embed = discord.Embed(
        title ="Welcome to the yuan's starspace!",
        description=f"Hello {member.mention}, glad to have you here!",
        color=0x00ff00
        
    )
    
    embed.set_thumbnail(url="https://pbs.twimg.com/media/FsKbjMSaYAMAuuh.jpg")
    embed.add_field(name="Rules", value="Please check #rules!", inline=False)
    embed.set_footer(text=f"Member #{len(member.guild.members)}")
    
    #sending embed to channel
    await channel.send(embed=embed)
    









bot.run(keys['BOT_TOKEN'])
