import asyncio
import discord
from discord.interactions import Interaction
from discord.ui import Button, View

class uSure(discord.ui.View):
    def __init__(self, bot) -> None:
        super().__init__(timeout=None)
        self.bot = bot
    
    @discord.ui.button(label="Yes", style=discord.ButtonStyle.danger, custom_id="yes_delete_ticket")
    async def delyes_ticket_callback(
        self,
        button, 
        interaction: discord.Interaction
    ):
        if "closed-" in interaction.channel.name:
            embed = discord.Embed(
                title="Ticket is being deleted",
                description="This ticket is being deleted.",
                color=discord.Color.red()
            )
            embed.set_footer(
                text=f"requested by {interaction.user.display_name}",
                icon_url=interaction.user.avatar.url
            )
            await interaction.channel.send(embed=embed)
            await asyncio.sleep(1)
            await interaction.channel.delete()