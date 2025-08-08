import discord
from discord.ext import commands
from datetime import datetime
import random
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
#                    CLASSES
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

        # pet heart status initialized to 0
        pets_data[self.author_id]['hearts_status'] = 0

        # success message
        self.embed.description = f"Congratulations! You just adopted a new pet on **{date_adopted}** and decided to name it **{self.prev_petname.upper()}**!! ꉂ(˵˃ ᗜ ˂˵)!"

        # disable the buttons
        for child in self.children:
            if isinstance(child, discord.ui.Button):
                child.disabled = True
        await interaction.message.edit(embed=self.embed, view=self)
        await interaction.response.send_message(f"You successfully adopted a new pet!", ephemeral=True)

# ------------------------------------------------------------
#                    USER FUNCTIONS
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

@bot.command()
async def petabandon(ctx):
    """
    Abandon pet...
    """

    author_id = ctx.author.id
    pet = pets_data.get(author_id)

    # error check if there is no pet adopted
    if not pet:
        await ctx.send("You have not adopted a pet yet!")
        return
    
    # delete the user's pet information
    del pets_data[author_id]

    await ctx.send("You have successfully abandoned the pet...")

@bot.command()
async def petstatus(ctx):
    """
    Display heart status of pet. It will increase with interactions.
    """

    author_id = ctx.author.id
    pet = pets_data.get(author_id)

    # error check if there is no pet adopted
    if not pet:
        await ctx.send("You have not adopted a pet yet!")
        return
    
    pet_name = pets_data[author_id]['pet_name']

    match pets_data[author_id]['hearts_status']:
        case x if x < 1:
            hearts_status = f"# ♡ ♡ ♡ ♡ ♡\n{pet_name} feels tense around you..."
        case x if x < 2:
            hearts_status = f"# ❤︎ ♡ ♡ ♡ ♡\n{pet_name} is starting to warm up to you but still on edge."
        case x if x < 3:
            hearts_status = f"# ❤︎ ❤︎ ♡ ♡ ♡\n{pet_name} is tolerating your existence."
        case x if x < 4:
            hearts_status = f"# ❤︎ ❤︎ ❤︎ ♡ ♡\n{pet_name} feels safe with you and trusts you'll keep it alive."
        case x if x < 5:
            hearts_status = f"# ❤︎ ❤︎ ❤︎ ❤︎ ♡\n{pet_name} likes you a lot and feels very comfortable with you."
        case x if x >= 5:
            hearts_status = f"# ❤︎ ❤︎ ❤︎ ❤︎ ❤︎\n{pet_name} LOVES YOU SOOO MUCH!!"

    embed = discord.Embed(
        title = "Pet Status\*ੈ✩‧₊˚",
        description = hearts_status,
        color = 0x94c2ff
    )
    embed.set_footer(text="*To increase the heart status, interact with your pet often!*")
    
    await ctx.send(embed=embed)

@bot.command()
async def petpet(ctx):
    """
    Interact with pet by petting.
    """

    author_id = ctx.author.id
    pet = pets_data.get(author_id)

    # error check if there is no pet adopted
    if not pet:
        await ctx.send("You have not adopted a pet yet!")
        return
    
    pet_name = pets_data[author_id]['pet_name']
    hearts_status = pets_data[author_id]['hearts_status']

    # pet_rng =  random.randint(1, 6 - int(hearts_status))
    pet_rng = random.randint(0,1)
    print(f'pet random number {pet_rng}!')

    if pet_rng == 1:
        
        if hearts_status != 5:
            pets_data[author_id]['hearts_status'] += 0.5
        await ctx.send(f"{pet_name} purrs and rolls around as you're petting.")
    else:
        await ctx.send(f"{pet_name} avoids your hand and glares at you...")

# RUN THE BOT
bot.run(keys['BOT_TOKEN'])