import discord
from discord.ext import commands
import data.id_files as idfiles

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
    def __init__(self, title:str, parent_view, message:discord.Message, prev_title="", prev_description=""):
        super().__init__(title=title)

        self.parent_view = parent_view
        self.message = message

        is_secondary = self.title == "Secondary Message"

        # input title and description prompts
        self.input_title = discord.ui.TextInput(label="Title", style=discord.TextStyle.short, default=prev_title, required=False)
        self.input_description = discord.ui.TextInput(label="Description", style=discord.TextStyle.paragraph, default=prev_description, required=not is_secondary)

        # add to the popup
        self.add_item(self.input_title)
        self.add_item(self.input_description)

    # submit for each modal (not the submit button)
    async def on_submit(self, interaction: discord.Interaction):

        # the input values from the user
        title = self.input_title.value
        description = self.input_description.value

        # edit the main message
        if self.title == "Main Message":
            
            self.parent_view.embed.title = title
            self.parent_view.embed.description = description
            self.parent_view.prev_main_title = title
            self.parent_view.prev_main_description = description
            await self.message.edit(embed=self.parent_view.embed)

        # edit the secondary message
        elif self.title == "Secondary Message":
            # save the inputs and store and previous inputs
            self.parent_view.prev_secondary_title = title
            self.parent_view.prev_secondary_description = description

            # remove the second field if no input
            if not title and not description:
                if len(self.parent_view.embed.fields) == 1:
                    self.parent_view.embed.remove_field(0)
                    await self.message.edit(embed=self.parent_view.embed)
            # else, edit the second field
            else:
                if len(self.parent_view.embed.fields) == 1:
                    self.parent_view.embed.set_field_at(0, name=title, value=description, inline=False)
                else:
                    self.parent_view.embed.add_field(name=title, value=description)
                await self.message.edit(embed=self.parent_view.embed)

        # submit to the target channel
        elif self.title == "Submit Message":
            await self.parent_view.target_channel.send(embed=self.parent_view.embed)
            await interaction.response.send_message("Embed sent to specified channel! :D", ephemeral=False)

        await interaction.response.send_message("Embed is updated! :D", ephemeral=True)

class myMenu(discord.ui.View):
    def __init__(self, embed, channel):
        super().__init__()
        self.embed = embed
        self.channel = channel
        self.value = None
        self.prev_main_title = ""
        self.prev_main_description = ""
        self.prev_secondary_title = ""
        self.prev_secondary_description = ""

    # button to enter main message
    @discord.ui.button(label="Main Message", style=discord.ButtonStyle.grey)
    async def main(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = myModal(
            title="Main Message",
            parent_view=self,
            message=interaction.message,
            prev_title=self.prev_main_title,
            prev_description=self.prev_main_description
            )
        await interaction.response.send_modal(modal)

    # button to enter secondary message
    @discord.ui.button(label="Secondary Message", style=discord.ButtonStyle.grey)
    async def secondary(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = myModal(
            title="Secondary Message",
            parent_view=self,
            message=interaction.message,
            prev_title=self.prev_secondary_title,
            prev_description=self.prev_secondary_description
            )
        await interaction.response.send_modal(modal)

    # submit to send the embed to the correct channel
    @discord.ui.button(label="Submit", style=discord.ButtonStyle.red)
    async def submit(self, interaction: discord.Interaction, button: discord.ui.Button):
        target_channel = self.channel
        await target_channel.send(embed=self.embed)
        await interaction.message.edit(view=None)
        await interaction.response.send_message("Embed sent to the specified channel!", ephemeral=False)

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
async def embed(ctx, channel:discord.TextChannel=None):
    """
    Creates an embed with menu buttons to edit the embed.
    Takes an optional argument to send the embed to another channel.
    """

    # optional
    target_channel = channel or ctx.channel

    # embed message that displays how to use this command
    embed_info = discord.Embed(
        title = "Let's create a cute embed \*ੈ✩‧₊˚",
        description = (
            "✧･ﾟ: *✧･ﾟ:\*\n"
            "*So you want to create something cute, right?\n"
            "To use this command, it's pretty simple~*\n\n"

            "__Directions:˚ ༘♡ ⋆｡˚__\n"
            "The **main message** contains a title and description. ༉‧₊˚.\n"
            "- Input whatever you want for both of them.\n"
            "- This is used for main focus or info at the start of the embed.\n"
            "   - i.e. The rules and overall info for the rules.\n\n"

            "The **secondary message** also contains a title and decription. ༉‧₊˚.\n"
            "- Input whatever but it is *optional*.\n"
            "- This is used if you want to add extra information such as:\n"
            "   - i.e. a list of rules as subheaders and each rule information.\n\n"
            

            "When you are done, click **submit** and it will send over to the specified channel.\n"
            "✧･ﾟ: \*✧･ﾟ:\*✧･ﾟ: \*✧･ﾟ:\*✧･ﾟ: \*✧･ﾟ:\* \n"
        ),
        color = 0xffabdc
    )

    embed_info.set_footer(text="If you didn't set a channel after !embed, it will send to this channel after clicking submit.")

    # empty embed message that stores user input
    embed_result = discord.Embed(
            title=" ",
            description=" ",
            color=0xffabdc
        )
    view = myMenu(embed_result, target_channel)
    await ctx.send(embed=embed_info,view=view)

# display role ids
@bot.command()
async def roleid(ctx):
    embed = discord.Embed(
        title=idfiles.title,
        description=idfiles.roleid,
        color=0xffabdc
    )
    embed.set_footer(text=idfiles.footer)
    await ctx.send(embed=embed)

# display ping ids
@bot.command()
async def pingid(ctx):
    embed = discord.Embed(
        title=idfiles.title,
        description=idfiles.pingid,
        color=0xffabdc
    )
    embed.set_footer(text=idfiles.footer)
    await ctx.send(embed=embed)

# display channel ids
@bot.command()
async def channelid(ctx):
    embed = discord.Embed(
        title=idfiles.title,
        description=idfiles.channelid,
        color=0xffabdc
    )
    embed.set_footer(text=idfiles.footer)
    await ctx.send(embed=embed)

# display age ids
@bot.command()
async def ageid(ctx):
    embed = discord.Embed(
        title=idfiles.title,
        description=idfiles.ageid,
        color=0xffabdc
    )
    embed.set_footer(text=idfiles.footer)
    await ctx.send(embed=embed)

# display pronoun ids
@bot.command()
async def pronounid(ctx):
    embed = discord.Embed(
        title=idfiles.title,
        description=idfiles.pronounid,
        color=0xffabdc
    )
    embed.set_footer(text=idfiles.footer)
    await ctx.send(embed=embed)

# display region ids
@bot.command()
async def regionid(ctx):
    embed = discord.Embed(
        title=idfiles.title,
        description=idfiles.regionid,
        color=0xffabdc
    )
    embed.set_footer(text=idfiles.footer)
    await ctx.send(embed=embed)

# display color ids
@bot.command()
async def colorid(ctx):
    embed = discord.Embed(
        title=idfiles.title,
        description=idfiles.colorid,
        color=0xffabdc
    )
    embed.set_footer(text=idfiles.footer)
    await ctx.send(embed=embed)


# RUN THE BOT
bot.run(keys['BOT_TOKEN'])