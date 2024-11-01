import discord
from discord.ext import commands
from discord.commands import Option
from discord.commands import SlashCommandGroup

class Infractions(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        print(f"{self.__class__.__name__} loaded")

    @commands.command(
        name="warn",
        description="Warn a member"
    )
    @commands.has_permissions(moderate_members=True)
    async def warn(
        self,
        ctx: discord.ApplicationContext,
        member: Option(discord.Member, description="The member you want to warn (this will add one point to their infraction count)", required=True), #type: ignore
        reason: Option(str, description="The reason why you've warned them.", required=False), #type: ignore
    ):
        embed = discord.Embed(
            title="Adding...",
            description="Adding warns and infraction count to database...",
            color=discord.Color.yellow()
        )
        await ctx.interaction.response.send_message(embed=embed, ephemeral=True)

        if self.bot.settings.get(f'Infractions.{member.name}.Warns.Count') == None or 0:
            self.bot.settings.set(f'Infractions.{member.name}.Warns.Count', 1)
        else:
            self.bot.settings.set(f'Infractions.{member.name}.Warns.Count', self.bot.settings.get(f'Infractions.{member.name}.Warns.Count')+1)

        if reason != None:
            self.bot.settings.set(f'Infractions.{member.name}.Warns.{self.bot.settings.get(f'Infractions.{member.name}.Warns.Count')}.Reason', reason)

        if self.bot.settings.get(f'Infractions.{member.name}.Count') == None:
            self.bot.settings.set(f'Infractions.{member.name}.Count', 1)
        else:
            self.bot.settings.set(f'Infractions.{member.name}.Count', self.bot.settings.get(f'Infractions.{member.name}.Count')+1)

        embed = discord.Embed(
            title="Added!",
            description="Everything has been added to the database successfully!",
            color=discord.Color.green()
        )
        embed.add_field(
            name='Warn Count:',
            value=self.bot.settings.get(f'Infractions.{member.name}.Warns.Count')
        )
        embed.add_field(
            name='Warn Reason: (if specified)',
            value=self.bot.settings.get(f'Infractions.{member.name}.Warns.{self.bot.settings.get(f'Infractions.{member.name}.Warns.Count')}.Reason')
        )
        embed.add_field(
            name="Infractions Count:",
            value=self.bot.settings.get(f'Infractions.{member.name}.Count')
        )
        embed.set_footer(
            text="Something missing ? report to @asicalug.",
            icon_url="https://r2.e-z.host/17a2b375-7193-4f28-94c4-be10a3e7c1b4/upq43ww9.png"
        )
        await ctx.interaction.edit_original_response(embed=embed)

        

def setup(bot: commands.Bot):
    bot.add_cog(Infractions(bot))