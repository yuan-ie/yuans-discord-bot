import discord
from discord.ext import commands
from datetime import datetime
import random
import os
import sqlite3
from tracker_function import pet_interact, feed_interact, bath_interact
from database_function import create_database, update_database, add_data, update_data, remove_data, search_data, retrieve_data, age_data
from level_function import add_exp, display_level, species_pack
from bios import species as sp

datafolder = "../data"
datafile = "../data/database.db"

# create folder if it does not exist
if not os.path.exists(datafolder):
    os.mkdir(datafolder)

# create empty database if it does not exist
create_database(datafile=datafile)

# prefix to run a command for Xiaoling bot.
bot = commands.Bot(command_prefix="+", intents=discord.Intents.all())

# empty dictionary for the important stuff
keys = {}

# read the key textfile to get bot token and channel ID
with open('../keys.txt', 'r') as file:
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
    def __init__(self, title:str, parent_view, message:discord.Message, pet_name="", author_id=""):
        super().__init__(title=title)

        self.parent_view = parent_view # adoptMenu is the parent
        self.message = message

        # input pet name prompts
        self.input_pet_name = discord.ui.TextInput(label="Pet Name", style=discord.TextStyle.short, default=pet_name, required=True)
        self.add_item(self.input_pet_name)

    # submit for each modal (not the submit button)
    async def on_submit(self, interaction: discord.Interaction):

        # pet name input from the user
        usr_pet_name = self.input_pet_name.value

        # saves the input to be used again
        self.parent_view.prev_pet_name = usr_pet_name

        # the existing embed
        embed = self.parent_view.embed
        embed.description = (
            "RIFU will allow you to have your very own virtual pet!\n"
            "Let's give your pet a name! ₊˚⊹ ᰔ\n\n"
            f"You decided with **{usr_pet_name.upper()}**. Any last thoughts?\n"
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
        self.prev_pet_name = ""

    # button to edit pet name
    @discord.ui.button(label="Pet Name", style=discord.ButtonStyle.grey)
    async def main(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = adoptModal(
            title="Name your pet! 𐔌՞. .՞𐦯",
            parent_view=self,
            message=interaction.message,
            pet_name=self.prev_pet_name,
            author_id=self.author_id
        )
        await interaction.response.send_modal(modal)

    # button to confirm pet name
    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.red)
    async def submit(self, interaction: discord.Interaction, button: discord.ui.Button):

        # if name is left blank
        if self.prev_pet_name == "":
            await interaction.response.send_message("You haven't decided a name yet!", ephemeral=True)
        else:
            # get the date and store the date in user information
            date_adopted = datetime.now().strftime("%B %d, %Y")

            # initialize user's pet information (userid, pet name, date adopted, hearts status, and update flag(0 or 1))
            add_data(
                filename=datafile,
                userid=self.author_id,
                pet_name=self.prev_pet_name.upper(),
                date_adopted=date_adopted,
                hearts_status=0,
                pet=0,
                pet_log="",
                feed=0,
                feed_log="",
                bath=0,
                bath_log="",
                level=0,
                species="",
                gender=""
                rarity=""
                description=""
                evolved="")

            # success message
            self.embed.description = f"Congratulations! You just adopted a new pet on **{date_adopted}** and decided to name it **{self.prev_pet_name.upper()}**!! ꉂ(˵˃ ᗜ ˂˵)!"

            # disable the buttons
            for child in self.children:
                if isinstance(child, discord.ui.Button):
                    child.disabled = True
            await interaction.message.edit(embed=self.embed, view=self)
            await interaction.response.send_message(f"You successfully adopted a new pet!", ephemeral=True)
        
# ------------------------------------------------------------
#                    USER FUNCTIONS
# ------------------------------------------------------------

@bot.command()
async def hello(ctx):
    await ctx.send("Hello! :)")

@bot.command()
async def adopt(ctx):
    """
    Sends an embed to adopt a pet and name it.
    """

    author_id = ctx.author.id
    pet = search_data(datafile, author_id)

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
async def info(ctx):
    """
    Sends an embed to view the info of the user's pet.
    """
    author_id = ctx.author.id
    pet = search_data(datafile, author_id)

    # error check if there is no pet adopted
    if not pet:
        await ctx.send("You have not adopted a pet yet!")
        return
    
    pet_name = retrieve_data(datafile, author_id, "pet_name")
    date_adopted = retrieve_data(datafile, author_id, "date_adopted")
    gender = retrieve_data(datafile, author_id, "gender")
    species = retrieve_data(datafile, author_id, "species")
    level = retrieve_data(datafile, author_id, "level")
    
    # display pet info
    embed = discord.Embed(
        title = "⋆. 𐙚 ˚ Pet Info ₍^. .^₎⟆ \✧˚ ⋆｡˚",
        description = (
            f"Name: **{pet_name}** ₊˚⊹ ᰔ\n"
            f"Level: {int(level)}\n"
            f"Age: {age_data(date_adopted)} days old \n"
            f"Gender: {date_adopted} \n"
            f"Species: {species} {sp.rarity[species]}\n "
            f"Date Adopted: {date_adopted} \n"
            f"Date Adopted: {date_adopted} \n"
        ),
        color = 0x94c2ff
    )
    await ctx.send(embed=embed)

@bot.command()
async def abandon(ctx):
    """
    Abandon pet...
    """

    author_id = ctx.author.id
    pet = search_data(datafile, author_id)

    # error check if there is no pet adopted
    if not pet:
        await ctx.send("You have not adopted a pet yet!")
        return
    
    # delete the user's pet information
    remove_data(datafile, author_id)

    await ctx.send("You have successfully abandoned the pet...")

@bot.command()
async def hearts(ctx):
    """
    Display heart status of pet. It will increase with interactions.
    """

    author_id = ctx.author.id
    pet = search_data(datafile, author_id)

    # error check if there is no pet adopted
    if not pet:
        await ctx.send("You have not adopted a pet yet!")
        return
    
    hearts_status = retrieve_data(datafile, author_id, "hearts_status")
    pet_name = retrieve_data(datafile, author_id, "pet_name")

    match float(hearts_status):
        case x if x < 1:
            hearts_status = f"# ♡ ♡ ♡ ♡ ♡\n⤷ ゛{pet_name} feels tense around you...\n"
        case x if x < 2:
            hearts_status = f"# ♥︎ ♡ ♡ ♡ ♡\n⤷ ゛{pet_name} is starting to warm up to you but still on edge.\n"
        case x if x < 3:
            hearts_status = f"# ♥︎ ♥︎ ♡ ♡ ♡\n⤷ ゛{pet_name} is tolerating your existence.\n"
        case x if x < 4:
            hearts_status = f"# ♥︎ ♥︎ ♥︎ ♡ ♡\n⤷ ゛{pet_name} feels safe with you and trusts you'll keep it alive.\n"
        case x if x < 5:
            hearts_status = f"# ♥︎ ♥︎ ♥︎ ♥︎ ♡\n⤷ ゛{pet_name} likes you a lot and feels very comfortable with you.\n"
        case x if x >= 5:
            hearts_status = f"# ♥︎ ♥︎ ♥︎ ♥︎ ♥︎\n⤷ ゛{pet_name} LOVES YOU SOOO MUCH!!\n"

    embed = discord.Embed(
        title = "⋆˚✿˖° Hearts Status \*°❀⋆.ೃ࿔\*:･",
        description = (
            hearts_status + "⋆˚✿˖°\n"
            ),
        color = 0x94c2ff
    )
    embed.set_footer(text="*To increase the heart status, interact with your pet often!*")
    
    await ctx.send(embed=embed)

@bot.command()
async def pet(ctx):
    """
    Interact with pet by petting.
    """

    author_id = ctx.author.id
    pet = search_data(datafile, author_id)

    # error check if there is no pet adopted
    if not pet:
        await ctx.send("You have not adopted a pet yet!")
        return
    
    # retrieve data
    pet_name = retrieve_data(datafile, author_id, "pet_name")
    pet = retrieve_data(datafile, author_id, "pet")
    pet_log = retrieve_data(datafile, author_id, "pet_log")
    hearts_status = retrieve_data(datafile, author_id, "hearts_status")

    # update data
    new_pet_count, new_pet_log, flag = pet_interact(pet, pet_log)
    update_data(datafile, author_id, "pet", new_pet_count)
    update_data(datafile, author_id, "pet_log", new_pet_log)

    # check if reached the max number of pet interacts
    if flag is False:
        await ctx.send(f"{pet_name} doesn't want anymore pets!")
        return
    
    # add experience regardless if interact fails/success except when it reaches max
    level = retrieve_data(datafile, author_id, "level")
    levelup, new_level = add_exp(level, 0.10)
    update_data(datafile, author_id, "level", new_level)
    
    hearts_status = float(hearts_status)

    pet_rng =  random.randint(0, int((6 - int(hearts_status)) / 2))

    if pet_rng == 0:
        if hearts_status < 5:
            hearts_status += 0.25
            update_data(datafile, author_id, "hearts_status", hearts_status)
        await ctx.send(f"{pet_name} purrs and rolls around as you're petting.")
    else:
        await ctx.send(f"{pet_name} avoids your hand and glares at you...")

    if levelup is True:
        await ctx.send(f"{pet_name} has leveled up to level {int(new_level)}! ⸜(｡˃ ᵕ ˂ )⸝♡")

@bot.command()
async def feed(ctx):
    """
    Interact with pet by feeding.
    """

    author_id = ctx.author.id
    pet = search_data(datafile, author_id)

    # error check if there is no pet adopted
    if not pet:
        await ctx.send("You have not adopted a pet yet!")
        return
    
    pet_name = retrieve_data(datafile, author_id, "pet_name")
    feed = retrieve_data(datafile, author_id, "feed")
    feed_log = retrieve_data(datafile, author_id, "feed_log")
    hearts_status = retrieve_data(datafile, author_id, "hearts_status")

    new_feed_count, new_feed_log, flag = feed_interact(feed, feed_log)
    update_data(datafile, author_id, "feed", new_feed_count)
    update_data(datafile, author_id, "feed_log", new_feed_log)

    # check if reached the max number of pet interacts
    if flag is False:
        await ctx.send(f"{pet_name} can't eat another bite..")
        return
    
    # add experience regardless if interact fails/success except when it reaches max
    level = retrieve_data(datafile, author_id, "level")
    levelup, new_level = add_exp(level, 0.30)
    update_data(datafile, author_id, "level", new_level)

    hearts_status = float(hearts_status)

    if hearts_status < 5:
        hearts_status += 0.4
        update_data(datafile, author_id, "hearts_status", hearts_status)

    response_rng = random.randint(1,3)
    match response_rng:
        case 1: await ctx.send(f"{pet_name} gobbles up the food like this is its last meal.")
        case 2: await ctx.send(f"{pet_name} jumps in joy before tearing up the food in your hands.")
        case 3: await ctx.send(f"{pet_name} nibbles on the food till the very last crumb.")

    if levelup is True:
        await ctx.send(f"{pet_name} has leveled up to level {int(new_level)}! ⸜(｡˃ ᵕ ˂ )⸝♡")

@bot.command()
async def bath(ctx):
    """
    Interact with pet by bathing.
    """

    author_id = ctx.author.id
    pet = search_data(datafile, author_id)

    # error check if there is no pet adopted
    if not pet:
        await ctx.send("You have not adopted a pet yet!")
        return
    
    pet_name = retrieve_data(datafile, author_id, "pet_name")
    bath = retrieve_data(datafile, author_id, "bath")
    bath_log = retrieve_data(datafile, author_id, "bath_log")
    hearts_status = retrieve_data(datafile, author_id, "hearts_status")

    new_bath_count, new_bath_log, flag = bath_interact(bath, bath_log)
    update_data(datafile, author_id, "bath", new_bath_count)
    update_data(datafile, author_id, "bath_log", new_bath_log)

    # check if reached the max number of pet interacts
    if flag is False:
        await ctx.send(f"{pet_name} had already taken a bath!")
        return
    
    # add experience regardless if interact fails/success except when it reaches max
    level = retrieve_data(datafile, author_id, "level")
    levelup, new_level = add_exp(level, 0.30)
    update_data(datafile, author_id, "level", new_level)

    hearts_status = float(hearts_status)

    if hearts_status < 5:
        hearts_status += 0.4
        update_data(datafile, author_id, "hearts_status", hearts_status)
    
    await ctx.send(f"{pet_name} feels super clean now~")

    if levelup is True:
        await ctx.send(f"{pet_name} has leveled up to level {int(new_level)}! ⸜(｡˃ ᵕ ˂ )⸝♡")

@bot.command()
async def interacts(ctx):
    """
    Display the interacts usage.
    """

    author_id = ctx.author.id
    pet = search_data(datafile, author_id)

    # error check if there is no pet adopted
    if not pet:
        await ctx.send("You have not adopted a pet yet!")
        return
    
    pet = retrieve_data(datafile, author_id, "pet")
    feed = retrieve_data(datafile, author_id, "feed")
    bath = retrieve_data(datafile, author_id, "bath")

    embed = discord.Embed(
        title = "୨ৎ Interacts Status ≽^• ˕ • ྀི≼",
        description = (
            "°❀⋆.ೃ࿔\*:･°❀⋆.ೃ࿔\*:･\n\n"
            f"𖦹 ⭑ Pet: **{pet}**/3\n"
            "-# *for every 24 hours*\n\n"
            f"𖦹 ⭑ Feed: **{feed}**/1\n"
            "-# *for every 12 hours*\n\n"
            f"𖦹 ⭑ Bath: **{bath}**/1\n"
            "-# *for every 24 hours*\n\n"
            "°❀⋆.ೃ࿔\*:･°❀⋆.ೃ࿔\*:･"
        ),
        color = 0x94c2ff
    )
    
    await ctx.send(embed=embed)

@bot.command()
async def pethelp(ctx):
    embed = discord.Embed(
        title = "╰┈➤ Help ₍ᐢ. .ᐢ₎ ♬⋆.˚",
        description = (
            "The command always starts with '+', such as `+pethelp`!\n"
            "Here are the list of commands:\n\n"

            "˚ ༘ ೀ⋆｡˚\n"
            "✦ `+adopt` : adopt a pet and name it!\n"
            "✦ `+info` : display your pet's info!\n"
            "✦ `+hearts` : display your pet's heart status!\n"
            "✦ `+interacts` : displays the number of pet interacts!\n"
            "✦ `+pet` : pet your pet! max 3 pets per 24 hours.\n"
            "✦ `+feed` : feed your pet! max 1 feed per 12 hours\n"
            "✦ `+bath` : bathe your pet! max 1 bath per 24 hours\n"
            "✦ `+abandon` : abandon your pet if you're heartless and soulless.. :(\n"
        ),
        color = 0x94c2ff
    )
    
    await ctx.send(embed=embed)

@bot.command()
async def level(ctx):
    """
    Display level of the user's pet.
    """

    author_id = ctx.author.id
    pet = search_data(datafile, author_id)

    # error check if there is no pet adopted
    if not pet:
        await ctx.send("You have not adopted a pet yet!")
        return
    
    level = retrieve_data(datafile, author_id, "level")
    
    whole, fraction = display_level(level)
    
    embed = discord.Embed(
        title = "╰┈➤ Level Status ₍ᐢ. .ᐢ₎ ♬⋆.˚",
        description = (
            f"Level: {whole}\n"
            f"Exp: {int(fraction*100)}/100\n"            
        ),
        color = 0x94c2ff
    )
    
    await ctx.send(embed=embed)

@bot.command()
async def petpack(ctx):
    """
    Gives petpack (species, level, and gender) to users who do not have it.
    """

    author_id = ctx.author.id
    pet = search_data(datafile, author_id)

    # error check if there is no pet adopted
    if not pet:
        await ctx.send("You have not adopted a pet yet!")
        return
    
    species = retrieve_data(datafile, author_id, "species")
    level = retrieve_data(datafile, author_id, "level")
    gender = retrieve_data(datafile, author_id, "gender")

    if species is None and level is None and gender is None:
        species, level, gender = species_pack()
        update_data(datafile, author_id, "species", species)
        update_data(datafile, author_id, "level", level)
        update_data(datafile, author_id, "gender", gender)
        
        await ctx.send(f"Petpack given! <{species}, level {level}, {gender}>")

    else:
        await ctx.send(f"You already have the petpack! <{species}, level {level}, {gender}>")

@bot.command()
async def admin(ctx):
    """
    Admin adjust something.
    """

    author_id = ctx.author.id
    pet = search_data(datafile, author_id)

    # error check if there is no pet adopted
    if not pet:
        await ctx.send("You have not adopted a pet yet!")
        return
    
    level = update_data(datafile, author_id, "level", 4.5)
    update_data(datafile, author_id, "level", level)        
    await ctx.send(f"level changed to {level}")

# RUN THE BOT
bot.run(keys['BOT_TOKEN'])