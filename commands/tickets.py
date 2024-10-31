import discord
from discord.ext import commands
from discord.commands import Option
from discord.commands import SlashCommandGroup
import datetime

from views.selectors.ticketSelector import TicketSelector

from utils.others.convertToEmoji import convertIntToEmojis

class Tickets(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        print(f"{self.__class__.__name__} loaded")

    ticket = SlashCommandGroup(name="ticket", description="Various ticket Commands")

    @ticket.command(
        name="setup",
        description="Sets up the ticket system"
    )
    @commands.has_permissions(administrator=True)
    async def ticket_setup(
        self,
        ctx: discord.ApplicationContext,
        panel : Option(discord.TextChannel, description="The text channel where the ticket creation will take place"), #type: ignore
        category : Option(discord.CategoryChannel, description="The category where the tickets will be created (To add roles please edit te category's permissions.)"), #type: ignore
        role: Option(discord.Role, description="The role that will be able to manage tickets ex: delete them"), #type: ignore
        general_role: Option(discord.Role, description="Role that can access General Tickets"), #type: ignore
        management_role: Option(discord.Role, description="Role that can access Management Tickets"), #type: ignore
        ownership_role: Option(discord.Role, description="Role that can access Ownership Tickets"), #type: ignore
        
    ):
        self.bot.settings.set("Tickets.Panel", panel.id)   
        self.bot.settings.set("Tickets.Category", category.id)
        self.bot.settings.set("Tickets.Role", role.id)
        self.bot.settings.set("Tickets.GeneralRole", general_role.id)
        self.bot.settings.set("Tickets.ManagementRole", management_role.id)
        self.bot.settings.set("Tickets.OwnershipRole", ownership_role.id)

        Panel = self.bot.get_channel(self.bot.settings.get("Tickets.Panel"))
        Category = self.bot.get_channel(self.bot.settings.get("Tickets.Category"))

        embed = discord.Embed(
            title="Ticket System Set Up!",
            color=discord.Color.blurple()
        )
        embed.add_field(
            name="Panel",
            value=Panel.mention
        )
        embed.add_field(
            name="Category",
            value=Category.mention
        )
        await ctx.interaction.response.send_message(embed=embed, ephemeral=True)
        
        embed = discord.Embed(
            title="Ticket Information",
            description="Do you have any questions or concerns? Do you have a player to report? Are you having any trouble within our server? If so, you can create a ticket.",
            color=discord.Color.lighter_grey()
        )
        embed.add_field(
            name="<:DE_Web:1301549835685466122> General",
            value="General Questions\nGiveaway Winning"
        )
        embed.add_field(
            name="<:DE_Star:1301550098005758063> Management",
            value="Reporting\nStaff Inquiries"
        )
        embed.add_field(
            name="<:DE_Megaphone:1301549841406496860> Ownership",
            value="Serious Issues\nServer-Wide Problem"
        )
        embed.set_image(
            url="https://r2.e-z.host/17a2b375-7193-4f28-94c4-be10a3e7c1b4/jwy79kko.png"
        )
        embed.set_footer(
            text="Designerlc Team",
            icon_url="https://r2.e-z.host/17a2b375-7193-4f28-94c4-be10a3e7c1b4/d5zm1xpi.webp"
        )
        embed2 = discord.Embed(color=discord.Color.lighter_grey()).set_image(url="https://r2.e-z.host/17a2b375-7193-4f28-94c4-be10a3e7c1b4/uddqod3k.png")
        await Panel.send(embeds=[embed2, embed], view=TicketSelector(bot=self.bot))

def setup(bot: commands.Bot):
    bot.add_cog(Tickets(bot))