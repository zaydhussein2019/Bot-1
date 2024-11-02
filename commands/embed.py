import discord
from discord.ext import commands, pages
from discord.commands import Option
from discord.commands import SlashCommandGroup
from discord.ext.pages import Paginator, Page
from bot import bot
import asyncio


class Embed(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        print(f"{self.__class__.__name__} loaded")
    
    embed = SlashCommandGroup(name="embed", description="Various ticket Commands")

    @embed.command(
        name="add",
        description="adds an embed to the database"
    )
    @commands.has_permissions(manage_messages=True)
    async def embed_add(
        self,
        ctx: discord.ApplicationContext,

        name: Option(str, description="The name of the embed (this is how you'll use it)", required=True), #type: ignore

        title: Option(str, description="The title that the embed should have", required=True), #type: ignore
        description: Option(str, description="The description the embed should have", required=True), #type: ignore

        field1_name: Option(str, description="The name that the first field should have", required=False), #type: ignore
        field1_value: Option(str, description="The value the first field should have", required=False), #type: ignore

        field2_name: Option(str, description="The name that the second field should have", required=False), #type: ignore
        field2_value: Option(str, description="The value the first second should have", required=False), #type: ignore

        field3_name: Option(str, description="The name that the third field should have", required=False), #type: ignore
        field3_value: Option(str, description="The value the third should have", required=False), #type: ignore

        footer_text: Option(str, description="The text that the footer should have", required=False), #type: ignore
        footer_url: Option(str, description="The image that the footer should have (url)", required=False), #type: ignore

        image: Option(str, description="The url of the image that the embed should have", required=False), #type: ignore

        thumbnail: Option(str, description="The thumbnail that the embed should have (url)", required=False), #type: ignore
    ): 
        embed = discord.Embed(
            title="This is a preview of the embed:",
            color=discord.Color.from_rgb(r=0, g=146, b=253)
        )
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

        await ctx.interaction.response.send_message(embeds=[embed, embed2], ephemeral=True)
        

        self.bot.settings.set(f'Embed.{name}.title', title)
        self.bot.settings.set(f'Embed.{name}.description', description)

        if field1_name != None:
            self.bot.settings.set(f'Embed.{name}.field1_name', field1_name)
        if field1_value != None:
            self.bot.settings.set(f'Embed.{name}.field1_value', field1_value)

        if field2_name != None:
            self.bot.settings.set(f'Embed.{name}.field2_name', field2_name)
        if field2_value != None:
            self.bot.settings.set(f'Embed.{name}.field2_value', field2_value)

        if field3_name != None:
            self.bot.settings.set(f'Embed.{name}.field3_name', field3_name)
        if field3_value != None:
            self.bot.settings.set(f'Embed.{name}.field3_value', field3_value)

        if footer_text != None:
            self.bot.settings.set(f'Embed.{name}.footer_text', footer_text)
        if footer_url != None:
            self.bot.settings.set(f'Embed.{name}.footer_url', footer_url)

        if image != None:
            self.bot.settings.set(f'Embed.{name}.image', image)

        if thumbnail != None:
            self.bot.settings.set(f'Embed.{name}.thumbnail', thumbnail)


    @embed.command(
        name="remove",
        description="removes an embed from the database"
    )
    @commands.has_permissions(manage_messages=True)
    async def embed_remove(
        self,
        ctx: discord.ApplicationContext,
        name: Option(str, description="The name of the embed you want to remove", choices=bot.settings.print_keys("Embed")), #type: ignore
    ):

        embed = discord.Embed(
            title="Removing...",
            description=f"Removing {name} from the database",
            color=discord.Color.yellow()
        )
        await ctx.interaction.response.send_message(embed=embed, ephemeral=True)

        if name == "example":
            embed = discord.Embed(
                title="Error!",
                description="Can't remove the example.",
                color=discord.Color.red()
            )
            await ctx.interaction.edit_original_response(embed=embed)
            return

        self.bot.settings.remove(f'Embed.{name}')
        embed = discord.Embed(
            title="Removed!",
            description=f"Removed {name} from the database.",
            color=discord.Color.from_rgb(r=0, g=146, b=253)
        )
        await ctx.interaction.edit_original_response(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(Embed(bot))