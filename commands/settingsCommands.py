import discord
from discord.ext import commands
from discord.commands import Option
from discord.commands import SlashCommandGroup

class SettingsCommand(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        print(f"{self.__class__.__name__} loaded")
        
    settings = SlashCommandGroup(name="settings", description="Various settings Commands")

    @settings.command(
        name="welcoming",
        description="Settings for the welcoming system"
    )
    @commands.has_permissions(administrator=True)
    async def settings_welcoming(
        self,
        ctx: discord.ApplicationContext,
        channel: Option(discord.TextChannel, description="The channel where the bot should greet new members"),#type: ignore
    ):
        embed = discord.Embed(
            title="Saving...",
            description="saving to Systems.Welcoming.Channel",
            color=discord.Color.yellow()
        )
        await ctx.interaction.response.send_message(embed=embed, ephemeral=True)
        self.bot.settings.set('Systems.Welcoming.Channel', channel.id)
        embed = discord.Embed(
            title="Saved!",
            description=f"{channel.mention} has been successfully saved to `settings.json`!",
            color=discord.Color.green()
        )
        await ctx.interaction.edit_original_response(embed=embed)

    @settings.command(
        name="sync",
        description="syncs commands to the bot"
    )
    @commands.has_permissions(administrator=True)
    async def sync(
        self,
        ctx: discord.ApplicationContext, 
        guild: Option(discord.Guild, description="the guild you want to sync the commands to", required=False), #type: ignore
    ):
        embed = discord.Embed(
            title="Syncing...",
            description="Syncing bot commands",
            color=discord.Color.yellow()
        )
        await ctx.interaction.response.send_message(embed=embed, ephemeral=True)
        if guild != None:
            embed = discord.Embed(
                title="Syncing...",
                description=f"Syncing bot commands to `{guild.name}`...",
                color=discord.Color.yellow()
            )
            await ctx.interaction.edit_original_response(embed=embed)
            await self.bot.sync_commands(guild_ids=guild.id)
        if guild == None:
            embed = discord.Embed(
                title="Syncing...",
                description=f"Syncing bot commands globally.",
                color=discord.Color.yellow()
            )
            await ctx.interaction.edit_original_response(embed=embed)
            await self.bot.sync_commands()




def setup(bot: commands.Bot):
    bot.add_cog(SettingsCommand(bot))