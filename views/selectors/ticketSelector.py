import discord
from utils.others.calcTicketNum import calcTicketNum

from views.buttons.manageTickets import manageTicket

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
            embed = discord.Embed(
                title="Creating your ticket...",
                description="Please be patient as we are working to create your ticket.",
                color=discord.Color.yellow()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                interaction.guild.me: discord.PermissionOverwrite(view_channel=True),
                interaction.user: discord.PermissionOverwrite(view_channel=True), 
                interaction.guild.get_role(self.bot.settings.get('Tickets.GeneralRole')): discord.PermissionOverwrite(view_channel=True)
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
                name=f"general-{interaction.user.name}-{ticketNum}",
                category=category,
                overwrites=overwrites
            )
            

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
                value="nique ta mere"
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


#-----------------------------------------------------------------------------------------------------------------------------------------------------


        if select.values[0] == "General":
            embed = discord.Embed(
                title="Creating your ticket...",
                description="Please be patient as we are working to create your ticket.",
                color=discord.Color.yellow()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                interaction.guild.me: discord.PermissionOverwrite(view_channel=True),
                interaction.user: discord.PermissionOverwrite(view_channel=True), 
                interaction.guild.get_role(self.bot.settings.get('Tickets.GeneralRole')): discord.PermissionOverwrite(view_channel=True)
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
                name=f"general-{interaction.user.name}-{ticketNum}",
                category=category,
                overwrites=overwrites
            )
            

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
                value="nique ta mere"
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