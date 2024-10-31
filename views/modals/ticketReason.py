import discord
import traceback
from discord.interactions import Interaction
import discord.ui
from discord.ui import View, Button

class SuggestionModal(discord.ui.Modal):
    def __init__(self, bot, title="Why do you want to create this ticket ?", *args, **kwargs):
        self.bot = bot
        super().__init__(
            discord.ui.InputText(
                label="Type",
                placeholder="I've got issues/questions with...",
                max_length=2000,
                style=discord.InputTextStyle.long
            ),
            title=title,
            *args,
            **kwargs
        )

    async def callback(self, interaction: discord.Interaction):
            embed = discord.Embed(
                title="Welcome!",
                description=f"Do you have any questions or concerns? Do you have a player to report? Are you having any trouble within our server? If so, you can create a ticket.",
                color=discord.Color.yellow()
            )
            embed.add_field(
                name="<:DE_Arrow:1301549811467817040> Type:",
                value="General"
            )
            embed.add_field(
                name="<:DE_Arrow:1301549811467817040> Reason:",
                value={self.children[0].value}
            )
            embed.set_image(
                url="https://r2.e-z.host/17a2b375-7193-4f28-94c4-be10a3e7c1b4/jwy79kko.png"
            )
            embed.set_footer(
                text="General Ticket",
                icon_url="https://r2.e-z.host/17a2b375-7193-4f28-94c4-be10a3e7c1b4/upq43ww9.png"
            )