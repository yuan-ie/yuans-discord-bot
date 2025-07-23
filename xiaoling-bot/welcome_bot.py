import discord
from discord.ext import commands
from datetime import datetime

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
    
    #other channels
    rules_channel_id = 1367685195154591864
    intro_channel_id = 1367685212158296114
    verify_channel_id = 1367688296653652079
    
    #setting up time
    unix_time = int(datetime.utcnow().timestamp())
    
    
    
    #embeds
    embed = discord.Embed(
        title ="**welcome to『yuanie's server』 !**",
        description=(
            f"{member.mention} just joined! we hope you enjoy your time here :D\n\n"
            "─✦─ ✧ ✦─\n\n"
            f"make sure to read <#{rules_channel_id}>, make an <#{intro_channel_id}>, "
            f"and <#{verify_channel_id}> before you chat!"
        ),
        color=discord.Color.from_rgb(74, 46, 100)
        
    )
    
    
    embed.set_author(
        name=member.display_name,
        icon_url=member.avatar.url if member.avatar else member.default_avatar.url
    )
    #embed.set_thumbnail(url="https://pbs.twimg.com/media/FsKbjMSaYAMAuuh.jpg")
    embed.set_image(url="https://i.pinimg.com/originals/58/2a/8c/582a8c8f1941f193f32697a9d0dbca3c.gif")
    embed.add_field(name="Rules", value="Please check #rules!", inline=False)
    embed.set_footer(text=f"we are now at {len(member.guild.members)} members! • <t:{unix_time}:f>")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    #sending embed to channel
    await channel.send(embed=embed)
    









bot.run(keys['BOT_TOKEN'])
