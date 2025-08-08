import discord
from discord.ext import commands
from datetime import datetime
# import data.id_files as idfiles

# prefix to run a command for Xiaoling bot.
bot = commands.Bot(command_prefix="+", intents=discord.Intents.all())

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

# ------------------------------------------------------------
# ------------------------------------------------------------

class adoptModal(discord.ui.Modal):
    def __init__(self, title:str, parent_view, message:discord.Message, petname="", author_id=""):
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
            f"You decided with **{usr_petname.upper()}**. Any last thoughts?\n"
            "*Note: You will not be able to change it later.*\n"
        )
        await self.message.edit(embed=self.parent_view.embed)

        # optional response to the modal submission
        await interaction.response.send_message("You decided a pet name!", ephemeral=True)

# button menu to adopt a pet
class adoptMenu(discord.ui.View):
    def __init__(self, embed, channel, author_id):
        super().__init__()
        self.embed = embed
        self.channel = channel
        self.author_id = author_id
        self.prev_petname = ""

    # button to edit pet name
    @discord.ui.button(label="Pet Name", style=discord.ButtonStyle.grey)
    async def main(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = adoptModal(
            title="Name your pet! 𐔌՞. .՞𐦯",
            parent_view=self,
            message=interaction.message,
            petname=self.prev_petname,
            author_id=self.author_id
        )
        await interaction.response.send_modal(modal)

    # button to confirm pet name
    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.red)
    async def submit(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not self.prev_petname:
            await interaction.response.send_message("You have not adopted a pet yet!", ephemeral=True)
            return
        
        # store user and pet information
        if self.author_id not in pets_data:
            pets_data[self.author_id] = {}
        pets_data[self.author_id]['pet_name'] = self.prev_petname.upper()

        # get the date and store the date in user information
        date_adopted = datetime.now().strftime("%B %d, %Y")
        pets_data[self.author_id]['date_adopted'] = date_adopted

        # success message
        self.embed.description = f"Congratulations! You just adopted a new pet on **{date_adopted}** and decided to name it **{self.prev_petname.upper()}**!! ꉂ(˵˃ ᗜ ˂˵)!"

        # disable the buttons
        for child in self.children:
            if isinstance(child, discord.ui.Button):
                child.disabled = True
        await interaction.message.edit(embed=self.embed, view=self)
        await interaction.response.send_message(f"You successfully adopted a new pet!", ephemeral=True)

# ------------------------------------------------------------
# ------------------------------------------------------------

pets_data = {}

@bot.command()
async def hello(ctx):
    await ctx.send("Hello! :)")

@bot.command()
async def petadopt(ctx):
    """
    Sends an embed to adopt a pet and name it.
    """

    author_id = ctx.author.id
    pet = pets_data.get(author_id)

    # error check if there is no pet adopted
    if pet:
        await ctx.send("You already have a pet!")
        return

    embed = discord.Embed(
        title = "Let's adopt a pet~ \*ੈ✩‧₊˚",
        description = (
            "RIFU will allow you to have your very own virtual pet!\n"
            "Let's give your pet a name! ₊˚⊹ ᰔ\n"
        ),
        color = 0x94c2ff
    )

    view = adoptMenu(embed, ctx.channel, ctx.author.id)
    await ctx.send(embed=embed,view=view)

@bot.command()
async def petinfo(ctx):
    """
    Sends an embed to view the info of the user's pet.
    """
    author_id = ctx.author.id
    pet = pets_data.get(author_id)

    # error check if there is no pet adopted
    if not pet:
        await ctx.send("You have not adopted a pet yet!")
        return
    
    # display pet info
    embed = discord.Embed(
        title = "Pet Info \*ੈ✩‧₊˚",
        description = (
            f"Name: **{pets_data[author_id]['pet_name']}** ₊˚⊹ ᰔ\n"
            f"Date Adopted: {pets_data[author_id]['date_adopted']} \n"
        ),
        color = 0x94c2ff
    )
    await ctx.send(embed=embed)

# RUN THE BOT
bot.run(keys['BOT_TOKEN'])