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

        
    async def on_member_join(self, member):
        print("hi")
        channel = self.bot.get_channel(self.bot.settings.get('Systems.Welcoming.Channel'))
        if channel is not None:
            embed = discord.Embed(
                title=f"Welcome {member.name}!",
                description=f"Welcome to @designerlc, {member.mention}",
                color=discord.Color.blurple()
            )
            embed.set_thumbnail(url=member.avatar.url)
            embed.set_footer(text="Need help? Open a ticket!", icon_url="https://r2.e-z.host/17a2b375-7193-4f28-94c4-be10a3e7c1b4/d5zm1xpi.webp")
            await channel.send(f'Welcome {member.mention}.')
        if channel is None:
            print("Welcome Channel has NOT been set. I will not be able to welcome new members. Please set it by using /settings welcoming.")




def setup(bot: commands.Bot):
    bot.add_cog(Ready(bot))