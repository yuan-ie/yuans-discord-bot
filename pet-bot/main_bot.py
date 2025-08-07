import discord
from discord.ext import commands
# import data.id_files as idfiles

# prefix to run a command for Xiaoling bot.
bot = commands.Bot(command_prefix="-", intents=discord.Intents.all())

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

class adoptModal(discord.ui.Modal):
    def __init__(self, title:str, parent_view, message:discord.Message, petname=""):
        super().__init__(title=title)

        self.parent_view = parent_view # adoptMenu is the parent
        self.message = message

        # input pet name prompts
        self.input_petname = discord.ui.TextInput(label="Pet Name", style=discord.TextStyle.short, default=petname, required=True)
        self.add_item(self.input_petname)

    # submit for each modal (not the submit button)
    async def on_submit(self, interaction: discord.Interaction):

        # pet name input from the user
        usr_petname = self.input_petname.value

        # saves the input to be used again
        self.parent_view.prev_petname = usr_petname

        # the existing embed
        embed = self.parent_view.embed
        embed.description = (
            "RIFU will allow you to have your very own virtual pet!\n"
            "Let's give your pet a name! ₊˚⊹ ᰔ\n\n"
            f"You decided with **{usr_petname}**. Any last thoughts?\n"
            "*Note: You will not be able to change it later.*\n"
        )
        await self.message.edit(embed=self.parent_view.embed)

        # optional response to the modal submission
        await interaction.response.send_message("You decided a pet name!", ephemeral=True)

# button menu to adopt a pet
class adoptMenu(discord.ui.View):
    def __init__(self, embed, channel):
        super().__init__()
        self.embed = embed
        self.channel = channel
        self.prev_petname = ""

    @discord.ui.button(label="Pet Name", style=discord.ButtonStyle.grey)
    async def main(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = adoptModal(
            title="Name your pet! 𐔌՞. .՞𐦯",
            parent_view=self,
            message=interaction.message,
            petname=self.prev_petname
        )
        await interaction.response.send_modal(modal)

@bot.command()
async def hello(ctx):
    await ctx.send("Hello! :)")

@bot.command()
async def adopt(ctx):
    """
    Sends an embed to adopt a pet and name it.
    """

    embed = discord.Embed(
        title = "Let's adopt a pet~ \*ੈ✩‧₊˚",
        description = (
            "RIFU will allow you to have your very own virtual pet!\n"
            "Let's give your pet a name! ₊˚⊹ ᰔ\n"
        ),
        color = 0x94c2ff
    )

    view = adoptMenu(embed, ctx.channel)
    await ctx.send(embed=embed,view=view)

# RUN THE BOT
bot.run(keys['BOT_TOKEN'])