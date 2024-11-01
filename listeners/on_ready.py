import os
import discord
import inspect
import importlib
from discord.ext import commands

from views.selectors.ticketSelector import TicketSelector
from views.buttons.manageTickets import manageTicket
from views.buttons.ticketDeleteCheck import uSure

class Ready(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        print(f"{self.__class__.__name__} loaded")

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} is ready")
        activity = discord.Activity(
            name="Roblox",
            details="On ER:LC",
            type=discord.ActivityType.playing,
            assets={"large_image": "roblox", "small_image": "roblox"}
        )
        await self.bot.change_presence(status=discord.Status.online, activity=activity)        
        print("Loading views...")
        self.bot.add_view(TicketSelector(bot=self.bot))
        self.bot.add_view(manageTicket(bot=self.bot))
        self.bot.add_view(uSure(bot=self.bot))
        print("Loaded views!")




def setup(bot: commands.Bot):
    bot.add_cog(Ready(bot))