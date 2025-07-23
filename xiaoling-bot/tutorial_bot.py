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
            
            self.parent_view.prev_secondary_title = title
            self.parent_view.prev_secondary_description = description

            if not title and not description:
                if len(self.parent_view.embed.fields) == 1:
                    self.parent_view.embed.remove_field(0)
                    await self.message.edit(embed=self.parent_view.embed)
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

    target_channel = channel or ctx.channel

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

    embed_result = discord.Embed(
            title=" ",
            description=" ",
            color=0xffabdc
        )
    view = myMenu(embed_result, target_channel)
    await ctx.send(embed=embed_info,view=view)

@bot.command()
async def rolesid(ctx):
    embed = discord.Embed(
        title="✧˚ · .Important Roles & Pings ID ༊\*·˚",
        description=(
            "⋇⊶⊰❣⊱⊷⋇\n"
            "__**role pings**__\n"
            "star overseer: <@&1367682907472134145> 1367682907472134145\n"
            "star gazer: <@&1384385366907293737> 1384385366907293737\n"
            "shooting stars: <@&1387267272074068161> 1387267272074068161\n"
            "constellations: <@&1372276066185383936> 1372276066185383936\n"
            "asterisms: <@&1375331835294253096> 1375331835294253096\n"
            "booster: <@&1386293381663297727> 1386293381663297727\n"
            "asteroids: <@&1373069041383510138> 1373069041383510138\n"
            "white stars: <@&1367690008701440091> 1367690008701440091\n"
            "strike 1: <@&1373141630407671900> 1373141630407671900\n"
            "strike 2: <@&1377866263568846978> 1377866263568846978\n"
            "strike 3: <@&1377866334792187925> 1377866334792187925\n"
            "level 10: <@&1373063974798622800> 1373063974798622800\n"
            "level 5: <@&1373063914018963587> 1373063914018963587\n"
            "level 1: <@&1373063865918685275> 1373063865918685275\n"
            "❀\n"

            "\n__**pings**__\n"
            "announcements: <@&1367692659799359489> 1367692659799359489\n"
            "yuanie uploads: <@&1367692693228097646> 1367692693228097646\n"
            "vid requests: <@&1367692796915355840> 1367692796915355840\n"
            "polls: <@&1367693118174007358> 1367693118174007358\n"
            "movie night: <@&1396094749877731378> 1396094749877731378\n"
            "game night: <@&1396094809420075019> 1396094809420075019\n"
            "karaoke night: <@&1396094832182821005> 1396094832182821005\n"
            "art event: <@&1396094868723601479> 1396094868723601479\n"
            "❀\n"

            "\n__**channels**__\n"
            "intro: <#1367685212158296114> 1367685212158296114\n"
            "verify: <#&1367688296653652079> 1367688296653652079\n"
            "rules: <#1367685195154591864> 1367685195154591864\n"
            "roles: <#1367686827833688215> 1367686827833688215\n"
            "❀\n"

            "\n__**age**__\n"
            "13-15: <@&1386228061027962890> 1386228061027962890\n"
            "16-17: <@&1386228212765294612> 1386228212765294612\n"
            "18-20: <@&1386228256369414154> 1386228256369414154\n"
            "20+: <@&1386228292851470386> 1386228292851470386\n"
            "❀\n"

            "\n__**pronouns**__\n"
            "she/her: <@&1367694769840717845> 1367694769840717845\n"
            "he/him: <@&1372269262403801128> 1372269262403801128\n"
            "they/them: <@&1372269357224431626> 1372269357224431626\n"
            "other/ask: <@&1372269384973811773> 1372269384973811773\n"
            "❀\n"

            "\n__**regions**__\n"
            "North America: <@&1390372038425837728> 1390372038425837728\n"
            "South America: <@&1390372092477837482> 1390372092477837482\n"
            "Asia: <@&1390372128502714388> 1390372128502714388\n"
            "Europe: <@&1390372143044235475> 1390372143044235475\n"
            "Africa: <@&1390372159695884318> 1390372159695884318\n"
            "Oceania: <@&1390372173826494716> 1390372173826494716\n"
            "❀\n"

            "\n__**colors**__\n"
            "❣ BOOSTERS/lv10\n"
            "gold: <@&1373068248521773286> 1373068248521773286\n"
            "terra: <@&1387225033637625907> 1387225033637625907\n"
            "❣ BOOSTERS/lv5\n"
            "peach pink: <@&1373068336170008616> 1373068336170008616\n"
            "pink: <@&1373068263130665142> 1373068263130665142\n"
            "❣ DEFAULT\n"
            "jade green: <@&1373070146800713768> 1373070146800713768\n"
            "sky blue: <@&1373070305412780152> 1373070305412780152\n"
            "pale blue: <@&1373070403710222446> 1373070403710222446\n"
            "white: <@&1373070562859024465> 1373070562859024465\n"
            "cream: <@&1373070497322897589> 1373070497322897589\n"
            "❀\n"

            "\nTo use a roleID, put the ID in <@&...>\nsuch as \<\@\&12345678\>\n"
            "\nTo use a channelID, put the ID in <#...>\nsuch as \<\#12345678\>\n"
        ),
        color=0xffabdc
    )

    await ctx.send(embed=embed)


# RUN THE BOT
bot.run(keys['BOT_TOKEN'])