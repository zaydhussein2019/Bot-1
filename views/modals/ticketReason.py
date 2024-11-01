import discord
import traceback
from discord.interactions import Interaction
import discord.ui
from discord.ui import View, Button

from utils.others.calcTicketNum import calcTicketNum

from views.buttons.manageTickets import manageTicket


class TicketModal(discord.ui.Modal):
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
                title="Creating your ticket...",
                description="Please be patient as we are working to create your ticket.",
                color=discord.Color.yellow()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

            if self.bot.settings.get(f'Tickets.Type.{interaction.user.name}') == "General":
                role = self.bot.settings.get('Tickets.GeneralRole')
            if self.bot.settings.get(f'Tickets.Type.{interaction.user.name}') == "Management":
                role = self.bot.settings.get('Tickets.ManagementRole')
            if self.bot.settings.get(f'Tickets.Type.{interaction.user.name}') == "Ownership":
                role = self.bot.settings.get('Tickets.OwnershipRole')
            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                interaction.guild.me: discord.PermissionOverwrite(view_channel=True),
                interaction.user: discord.PermissionOverwrite(view_channel=True), 
                interaction.guild.get_role(role): discord.PermissionOverwrite(view_channel=True)
            }
            if self.bot.settings.get('Tickets.Count') is None:
                self.bot.settings.set('Tickets.Count', 0)

            current = self.bot.settings.get('Tickets.Count')
            ticketNum = calcTicketNum(current=current)

            category = discord.utils.get(
                interaction.guild.categories,
                id=self.bot.settings.get("Tickets.Category")
            )

            self.bot.settings.set("Tickets.Count", ticketNum)
            
            channel = await interaction.guild.create_text_channel(
                name=f"{self.bot.settings.get(f'Tickets.Type.{interaction.user.name}').lower()}-{ticketNum}",
                category=category,
                overwrites=overwrites
            )

            embed = discord.Embed(
                title="Welcome!",
                description=f"Do you have any questions or concerns? Do you have a player to report? Are you having any trouble within our server? If so, you can create a ticket.",
                color=discord.Color.from_rgb(r=0, g=146, b=253)
            )
            embed.add_field(
                name="<:DE_Arrow:1301549811467817040> Type:",
                value=self.bot.settings.get(f'Tickets.Type.{interaction.user.name}')
            )
            embed.add_field(
                name="<:DE_Arrow:1301549811467817040> Reason:",
                value=self.children[0].value
            )
            embed.set_image(
                url="https://r2.e-z.host/17a2b375-7193-4f28-94c4-be10a3e7c1b4/jwy79kko.png"
            )
            embed.set_footer(
                text="General Ticket",
                icon_url="https://r2.e-z.host/17a2b375-7193-4f28-94c4-be10a3e7c1b4/upq43ww9.png"
            )
            msg = await channel.send(content=f"Welcome to Designerlc, {interaction.user.mention}", embed=embed, view=manageTicket(bot=self.bot))
            await msg.pin(reason="First message in ticket")
            await channel.purge(limit=1, reason="ugly message")

            msg = await channel.send(interaction.guild.get_role(role).mention)
            if interaction.guild.get_role(role).id == self.bot.settings.get('Tickets.OwnershipRole'):
                await msg.delete(reason="Ghost Ping")

            self.bot.settings.remove(f'Tickets.Type.{interaction.user.name}')

            embed = discord.Embed(
                title="Ticket Created!",
                description=
                f"""
                Your ticket has been created.
                Please access it [here]({channel.jump_url}) ({channel.mention})
                """,
                color=discord.Color.green()
            )
            await interaction.edit_original_response(embed=embed)