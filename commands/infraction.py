import discord
from discord.ext import commands, pages
from discord.commands import Option
from discord.commands import SlashCommandGroup
from discord.ext.pages import Paginator, Page
import asyncio

warns = []
mods = []

class Infractions(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        print(f"{self.__class__.__name__} loaded")

    def get_pages(self):
        return self.pages

    infractions = SlashCommandGroup(name="infractions", description="Various ticket Commands")

    @infractions.command(
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

        self.bot.settings.set(f'Infractions.{member.name}.Warns.{self.bot.settings.get(f'Infractions.{member.name}.Warns.Count')}.Mod', ctx.user.mention)

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
            value=f"{self.bot.settings.get(f'Infractions.{member.name}.Count')}/18"
        )
        embed.set_footer(
            text="Something missing ? report to @asicalug.",
            icon_url="https://r2.e-z.host/17a2b375-7193-4f28-94c4-be10a3e7c1b4/upq43ww9.png"
        )
        await ctx.interaction.edit_original_response(embed=embed)

    @infractions.command(
        name="case",
        description="Case of a member"
    )
    @commands.has_permissions(moderate_members=True)
    async def infractions_case(
        self,
        ctx: discord.ApplicationContext,
        member: Option(discord.Member, description="The member's case you want to check", required=False), #type: ignore
    ):
        if member == None:
            member = ctx.user

        wAmount = self.bot.settings.get(f"Infractions.{member.name}.Warns.Count")

        if self.bot.settings.get(f"Infractions.{member.name}.Warns.Count") != None:
            for i in range(wAmount+1):
                if i == 0:
                    pass
                else:
                    warns.append(self.bot.settings.get(f'Infractions.{member.name}.Warns.{i}.Reason'))
                    mods.append(self.bot.settings.get(f'Infractions.{member.name}.Warns.{str(i)}.Mod'))

        joinedWarns = "\n".join(warns)
        joinedMods = "\n".join(mods)
        
        self.pages = [
            Page(
                embeds=[
                    discord.Embed(title=f"{member.name}'s Infractions Status", description=f"{self.bot.settings.get(f'Infractions.{member.name}.Count')}/18", color=discord.Color.from_rgb(r=0, g=146, b=253))
                ]
            ),
            Page(
                embeds=[
                    discord.Embed(title=f"{member.name}'s Warns", description=f"", color=discord.Color.yellow()).set_thumbnail(url=member.avatar.url)
                    .set_image(url="https://r2.e-z.host/17a2b375-7193-4f28-94c4-be10a3e7c1b4/jwy79kko.png")
                    .add_field(name="Reasons", value=joinedWarns)
                    .add_field(name="Mods", value=f'{joinedMods}')
                    .set_footer(text=f"Designerlc", icon_url="https://r2.e-z.host/17a2b375-7193-4f28-94c4-be10a3e7c1b4/d5zm1xpi.webp"),
                ],
            ),
            Page(
                embeds=[
                    discord.Embed(title=f"{member.name}'s Warns", description=f"W.I.P", color=discord.Color.yellow())
                ]
            )
        ]
        paginator = pages.Paginator(pages=self.get_pages())

        await paginator.respond(ctx.interaction, ephemeral=True)
        
        warns.clear()
        mods.clear()

        
        
        

def setup(bot: commands.Bot):
    bot.add_cog(Infractions(bot))