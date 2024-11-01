import discord
from discord.ext import commands

class onJoin(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        print(f"{self.__class__.__name__} loaded")

    @commands.Cog.listener()
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
    bot.add_cog(onJoin(bot))