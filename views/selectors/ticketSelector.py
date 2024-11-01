import discord
from utils.others.calcTicketNum import calcTicketNum

from views.modals.ticketReason import TicketModal

class TicketSelector(discord.ui.View):
    def __init__(self, bot: discord.Bot) -> None:
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.select(
        custom_id="ticket_selector",
        placeholder = "Ticket Category",
        min_values = 1,
        max_values = 1,
        options = [
            discord.SelectOption(
                label="General",
                emoji="<:DE_Web:1301549835685466122>",
                description="General Questions, Giveaway Winning"
            ),
            discord.SelectOption(
                label="Management",
                emoji="<:DE_Star:1301550098005758063>",
                description="Reporting, Staff Inquiries"
            ),
            discord.SelectOption(
                label="Ownership",
                emoji="<:DE_Megaphone:1301549841406496860>",
                description="Serious Issues, Server-Wide Problem"
            )
        ]
    )


    async def select_callback(self, select, interaction: discord.Interaction):
        if select.values[0] == "General":
            await interaction.response.send_modal(TicketModal(bot=self.bot))
            self.bot.settings.set(f'Tickets.Type.{interaction.user.name}', "General")

        if select.values[0] == "Management":
            await interaction.response.send_modal(TicketModal(bot=self.bot))
            self.bot.settings.set(f'Tickets.Type.{interaction.user.name}', "Management")

        if select.values[0] == "Ownership":
            await interaction.response.send_modal(TicketModal(bot=self.bot))
            self.bot.settings.set(f'Tickets.Type.{interaction.user.name}', "Ownership")