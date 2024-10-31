import discord
from discord.ext import commands
from discord.commands import Option
from discord.commands import SlashCommandGroup
import datetime

from utils.others.convertToEmoji import convertIntToEmojis

class Reviews(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        print(f"{self.__class__.__name__} loaded")

    review = SlashCommandGroup(name="review", description="Various review Commands")

    @review.command(
        name="setup",
        description="setup the reviews"
    )
    @commands.has_permissions(administrator=True)
    async def review_setup(
        self,
        ctx: discord.ApplicationContext,
        channel: Option(discord.TextChannel, description="The channel the reviews should be sent in.") #type: ignore
    ):
        self.bot.settings.set('Reviews.Channel', channel.id)
        embed = discord.Embed(
            title="Reviews Channel Set.",
            description=f"Reviews will now be sent in <#{self.bot.settings.get('Reviews.Channel')}>",
            color=discord.Color.blurple()
        )
        await ctx.interaction.response.send_message(embed=embed, ephemeral=True)



    @review.command(
        name='add',
        description='Review a designer'
    )
    async def review_add(
        self,
        ctx: discord.ApplicationContext,
        designer: Option(discord.Member, description="the designer you want to review", required=True), #type: ignore
        product: Option(description="the product the designer made that you want to review", required=True), #type: ignore
        rating: Option(int, description="The rating you want to give /5", required=True), #type: ignore
        note: Option(str, description="Anything else to add? Put it here.", require=False) #type: ignore
    ):
        channel = self.bot.get_channel(self.bot.settings.get('Reviews.Channel'))
        if rating not in range(1, 6):
            embed = discord.Embed(
                title="Error!",
                description="Your rating has to be between 1 and 5.",
                color=discord.Color.red()
            )
            await ctx.interaction.response.send_message(embed=embed, ephemeral=True)
            return

        embed = discord.Embed(
            title="Review Sent",
            description=f"Your review has been sent in <#{self.bot.settings.get('Reviews.Channel')}>",
            color=discord.Color.blurple()
        )
        await ctx.interaction.response.send_message(embed=embed, ephemeral=True)
        embed = discord.Embed(
            title="New Review!",
            color=discord.Color.light_gray()
        )
        embed.set_author(name=f"Sent by: {ctx.user.name}", icon_url=ctx.user.avatar.url)
        embed.add_field(
            name="Designer:",
            value=designer.mention
        )
        embed.add_field(
            name="Product:",
            value=product
        )
        embed.add_field(
            name="Rating:",
            value=convertIntToEmojis(rating)
        )
        embed.add_field(
            name="Extra Note:",
            value=note
        )
        embed.set_image(url='https://r2.e-z.host/17a2b375-7193-4f28-94c4-be10a3e7c1b4/jwy79kko.png')
        embed.set_thumbnail(url='https://r2.e-z.host/17a2b375-7193-4f28-94c4-be10a3e7c1b4/d5zm1xpi.webp')
        embed.set_footer(text='use /review add to review us!',icon_url="https://r2.e-z.host/17a2b375-7193-4f28-94c4-be10a3e7c1b4/upq43ww9.png")
        await channel.send(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(Reviews(bot))