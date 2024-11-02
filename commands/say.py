import discord
from discord.ext import commands
from discord.commands import Option
from bot import bot

class Say(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        print(f"{self.__class__.__name__} loaded")

    @commands.slash_command()
    @commands.has_permissions(manage_messages=True)
    async def say(
        self,
        ctx: discord.ApplicationContext,
        message: Option(str, description="The message that you want the bot to say", required=True), #type: ignore
        embed: Option(str, description="The name of the embed that you've setted before with `/embed add`", choices=bot.settings.print_keys("Embed"), required=False), #type: ignore
    ):
        if embed != None:
            title = self.bot.settings.get(f'Embed.{embed}.title')
            description = self.bot.settings.get(f'Embed.{embed}.description')
            field1_name = self.bot.settings.get(f'Embed.{embed}.field1_name')
            field1_value = self.bot.settings.get(f'Embed.{embed}.field1_value')
            field2_name = self.bot.settings.get(f'Embed.{embed}.field2_name')
            field2_value = self.bot.settings.get(f'Embed.{embed}.field2_value')
            field3_name = self.bot.settings.get(f'Embed.{embed}.field3_name')
            field3_value = self.bot.settings.get(f'Embed.{embed}.field3_value')
            footer_text = self.bot.settings.get(f'Embed.{embed}.footer_text')
            footer_url = self.bot.settings.get(f'Embed.{embed}.footer_url')
            image = self.bot.settings.get(f'Embed.{embed}.image')
            thumbnail = self.bot.settings.get(f'Embed.{embed}.thumbnail')

            embed2 = discord.Embed(
                title=title,
                description=description,
                color=discord.Color.from_rgb(r=0, g=146, b=253)
            )
            if field1_name and field1_value != None:
                embed2.add_field(
                    name=field1_name,
                    value=field1_value
                )
            if field2_name and field2_value != None:
                embed2.add_field(
                    name=field2_name,
                    value=field2_value
                )
            if field3_name and field3_value != None:
                embed2.add_field(
                    name=field3_name,
                    value=field3_value
                )
            if footer_text and footer_url != None:
                embed2.set_footer(
                    text=footer_text,
                    icon_url=footer_url
                )
            if image != None:
                embed2.set_image(
                    url=image
                )
            if thumbnail != None:
                embed2.set_thumbnail(
                    url=thumbnail
                )
            msg = await ctx.channel.send(f"{message}", embed=embed2)
        else:
            msg = await ctx.channel.send(f'{message}')

        await ctx.interaction.response.send_message(f"Sent! {msg.jump_url}", ephemeral=True)


def setup(bot: commands.Bot):
    bot.add_cog(Say(bot))