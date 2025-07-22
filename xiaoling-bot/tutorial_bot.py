import discord
from discord.ext import commands

# prefix to run a command for Xiaoling bot.
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

# empty dictionary for the important stuff
keys = {}

# read the key textfile to get bot token and channel ID
with open('keys.txt', 'r') as file:
    for line in file:
        if '=' in line:
            key, value = line.strip().split('=',1)
            if value.isdigit():
                keys[key] = int(value)
            else:
                keys[key] = value

# ------------- BUTTONS -----------------
class myModal(discord.ui.Modal):
    def __init__(self, title:str, parent_view, message:discord.Message):
        super().__init__(title=title)

        self.parent_view = parent_view
        self.message = message

        # input title and description prompts
        self.input_title = discord.ui.TextInput(label="Title", style=discord.TextStyle.short)
        self.input_description = discord.ui.TextInput(label="Description", style=discord.TextStyle.paragraph)

        # add to the popup
        self.add_item(self.input_title)
        self.add_item(self.input_description)

    async def on_submit(self, interaction: discord.Interaction):

        # the input values from the user
        title = self.input_title.value
        description = self.input_description.value

        # store as the instance variables
        if self.title == "Main Message":
            self.parent_view.embed.title=title
            self.parent_view.embed.description=description
        elif self.title == "Secondary Message":
            if len(self.parent_view.embed.fields) == 1:
                self.parent_view.embed.set_field_at(0, name=title, value=description, inline=False)
            else:
                self.parent_view.embed.add_field(name=title, value=description)
        await self.message.edit(embed=self.parent_view.embed)

        # embed = self.parent_view.create_embed(
        #     self.parent_view.embed.title_1,
        #     self.parent_view.embed.description_1,
        #     self.parent_view.embed.title_2,
        #     self.parent_view.embed.description_2
        # )
        
        await interaction.response.send_message("Embed Updated", ephemeral=True)

class myMenu(discord.ui.View):
    def __init__(self, embed):
        super().__init__()
        self.embed = embed
        self.value = None
        self.title_1 = None
        self.description_1 = None
        self.title_2 = None
        self.description_2 = None

    # button to enter main message
    @discord.ui.button(label="Main Message", style=discord.ButtonStyle.grey)
    async def main(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = myModal(title="Main Message", parent_view=self, message=interaction.message)
        await interaction.response.send_modal(modal)

    # button to enter secondary message
    @discord.ui.button(label="Secondary Message", style=discord.ButtonStyle.grey)
    async def secondary(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = myModal(title="Secondary Message", parent_view=self, message=interaction.message)
        await interaction.response.send_modal(modal)

# ------------- EVENTS ------------------
# after starting up, bot says something in specified channel
@bot.event
async def on_ready():
    print(f'Logged on as {bot.user}!')
    channel = bot.get_channel(keys['CHANNEL_ID'])
    await channel.send("Hello, I am at your service!")

# command to say hello
@bot.command()
async def hello(ctx):
    await ctx.send("Hello! :)")

@bot.command()
async def embed(ctx):
    embed = discord.Embed(
            title=" ",
            description=" ",
            color=0xffabdc
        )
    view = myMenu(embed)
    await ctx.reply(view=view)

@bot.command()
# async def embed(ctx):
#     embed=discord.Embed(title="Embed Title", description="this is the embed title description", color=0xffabdc)
#     # embed.set_thumbnail(url="https://i.imgur.com/axLm3p6.jpeg")
#     embed.add_field(name="embed field 1", value="description")
#     embed.add_field(name="embed field 2", value="description", inline=True)
#     embed.add_field(name="embed field 3", value="description", inline=True)
#     embed.set_footer(text="This is the footer. It contains text at the bottom of the embed")
#     await ctx.send(embed=embed)

async def embed2(ctx, *args):
    """
    displays messages in embed. mainly for setting up rules and other important things.
    usage: !embed <title> <description> <field1_name> <field1_value> <field2_name> <field2_value> ...
    example: !embed `rules` `here are the rules` `rule #1`... 
    """

    if not args:
        await ctx.send("Please enter the correct format: !embed `rules` `here are the rules` `rule #1`... ")
        return

    if len(args) >= 2:
        title = args[0]
        description = args[1]
    else:
        await ctx.send("At least put a title and description. :(")
        return

    embed=discord.Embed(
        title=title,
        description=description,
        color=0xffabdc
    )

    for i in range(2, len(args), 2):
        if i+1 < len(args):
            field_name = args[i]
            field_value = args[i+1]
            embed.add_field(
                name=field_name,
                value=field_value,
                inline=False
                )

    # embed=discord.Embed(title="Embed Title", description="this is the embed title description", color=0xffabdc)
    # # embed.set_thumbnail(url="https://i.imgur.com/axLm3p6.jpeg")
    # embed.add_field(name="embed field 1", value="description")
    # embed.add_field(name="embed field 2", value="description", inline=True)
    # embed.add_field(name="embed field 3", value="description", inline=True)
    # embed.set_footer(text="This is the footer. It contains text at the bottom of the embed")
    await ctx.send(embed=embed)
    

# RUN THE BOT
bot.run(keys['BOT_TOKEN'])