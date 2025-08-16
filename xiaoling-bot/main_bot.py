import discord
from discord.ext import commands
import data.id_files as idfiles
import io

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
    """
    Modal popup that prompts for title and description depending if it is the main message or secondary message.
    """
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
        """
        Clicking submit (of the modal) will save the values of this session.
        """

        # the input values from the user
        title = self.input_title.value
        description = self.input_description.value

        # edit the main message
        if self.title == "Main Message":
            
            self.parent_view.embed.title = title
            self.parent_view.embed.description = description
            self.parent_view.stored_main_title = title
            self.parent_view.stored_main_description = description
            await self.message.edit(embed=self.parent_view.embed)

        # edit the secondary message
        elif self.title == "Secondary Message":
            # save the inputs and store and previous inputs
            self.parent_view.stored_secondary_title = title
            self.parent_view.stored_secondary_description = description

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

        # # submit to the target channel
        # elif self.title == "Submit Message":
        #     await self.parent_view.target_channel.send(embed=self.parent_view.embed)
        #     await interaction.response.send_message("Embed sent to specified channel! :D", ephemeral=False)

        await interaction.response.send_message("Embed is updated! :D", ephemeral=True)

class stickerModal(discord.ui.Modal):
    """
    Modal popup that prompts for sticker id.
    """
    def __init__(self, title:str, parent_view, message:discord.Message, stored_ids=""):
        super().__init__(title=title)

        self.parent_view = parent_view
        self.message = message

        # input title and description prompts
        self.input_stickers = discord.ui.TextInput(label="Sticker IDs", style=discord.TextStyle.paragraph, default=stored_ids, required=False)
        self.add_item(self.input_stickers)

    async def on_submit(self, interaction: discord.Interaction):
        stickers = self.input_stickers.value
        self.parent_view.stored_stickers = stickers

        # if stickers are inputted or not inputted, display.
        if stickers != "":
            await interaction.response.send_message("Added stickers! :D", ephemeral=True)
        else:
            await interaction.response.send_message("No stickers added!", ephemeral=True)

class myMenu(discord.ui.View):
    def __init__(self, embed, channel):
        super().__init__()
        self.embed = embed
        self.channel = channel
        self.stored_main_title = ""
        self.stored_main_description = ""
        self.stored_secondary_title = ""
        self.stored_secondary_description = ""
        self.stored_image = None
        self.stored_stickers = ""

    # button to enter main message
    @discord.ui.button(label="Main Message", style=discord.ButtonStyle.grey)
    async def main(self, interaction: discord.Interaction, button: discord.ui.Button):
        """
        User inputs main message of the embed.
        """
        modal = myModal(
            title="Main Message",
            parent_view=self,
            message=interaction.message,
            prev_title=self.stored_main_title,
            prev_description=self.stored_main_description
            )
        await interaction.response.send_modal(modal)

    # button to enter secondary message
    @discord.ui.button(label="Secondary Message", style=discord.ButtonStyle.grey)
    async def secondary(self, interaction: discord.Interaction, button: discord.ui.Button):
        """
        User inputs secondary message of the embed.
        """
        modal = myModal(
            title="Secondary Message",
            parent_view=self,
            message=interaction.message,
            prev_title=self.stored_secondary_title,
            prev_description=self.stored_secondary_description
            )
        await interaction.response.send_modal(modal)

    @discord.ui.button(label="Stickers", style=discord.ButtonStyle.grey)
    async def sticker(self, interaction: discord.Interaction, button: discord.ui.button):
        """
        User uploads a sticker (optional).
        """
        modal = stickerModal(
            title="Upload Stickers (max 3 limit)",
            parent_view=self,
            message=interaction.message,
            stored_ids=self.stored_stickers
            )
        await interaction.response.send_modal(modal)


    @discord.ui.button(label="Image", style=discord.ButtonStyle.grey)
    async def image(self, interaction: discord.Interaction, button: discord.ui.button):
        """
        User uploads an image (optional).
        """

        await interaction.response.send_message("Please upload an image below.", ephemeral=True)

        def check(msg: discord.Message):
            return (
                msg.author == interaction.user
                and msg.attachments
                and msg.attachments[0].filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".webp"))
            )
        try:
            msg = await bot.wait_for("message", check=check, timeout=30)
            attachment = msg.attachments[0]
            img = await attachment.read()
            self.stored_image = discord.File(io.BytesIO(img), filename=attachment.filename)
            await interaction.followup.send("Image saved!", ephemeral=True)

        except TimeoutError:
            await interaction.followup.send("You didn’t upload an image in time. Try uploading again.", ephemeral=True)

    # submit to send the embed to the correct channel
    @discord.ui.button(label="Submit", style=discord.ButtonStyle.red)
    async def submit(self, interaction: discord.Interaction, button: discord.ui.Button):
        # try:
        target_channel = self.channel
        embed = self.embed
        error = False

        if self.stored_main_description == "":
            error = True
            await interaction.response.send_message("Main description needed!", ephemeral=True)

        # if image exists, put it in the embed.
        if self.stored_image:
            embed.set_image(url=f"attachment://{self.stored_image.filename}")
            await target_channel.send(embed=embed, file=self.stored_image)
        else:
            await target_channel.send(embed=embed)

        # upload the stickers if valid
        # if the stickers are inputted, split it by new line.
        if self.stored_stickers != "":
            sticker_ids = []
            sticker_objs = []
            invalid_ids = []
            stickers = self.stored_stickers.splitlines() if self.stored_stickers else []

            for s in stickers:
                if s.strip() != "":
                    try:
                        sticker_ids.append(int(s))
                    except ValueError:
                        invalid_ids.append(s)
                        # error = True
            
            for sid in sticker_ids:
                try:
                    sticker = await target_channel.guild.fetch_sticker(sid)
                    sticker_objs.append(sticker)
                    # error = False
                except discord.NotFound:
                    invalid_ids.append(sid)
                    # error = True

            if sticker_objs:
                await target_channel.send(stickers=sticker_objs)
            if invalid_ids:
                await interaction.response.send_message(f"Disregarding invalid sticker IDs: {', '.join(map(str, invalid_ids))}", ephemeral=True)

        if not error:
            # close up the session and confirm send if no errors
            await interaction.message.edit(view=None)
            await interaction.response.send_message(f"Embed sent to <#{target_channel.id}>", ephemeral=False)

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