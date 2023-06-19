import discord
from discord.ext import commands
from discord import app_commands
from discord.embeds import Embed

class CurrentRota(commands.Cog):
    
    def __init__(self, bot) -> None:
        self.bot = bot
        
async def setup(bot):
    await bot.add_cog(CurrentRota(bot))