import discord
from discord.ext import commands
from discord import app_commands

class Main(commands.Cog):
    
    def __init__(self, bot) -> None:
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("Démarrage du VeemoBot")
        
    # Pour synchroniser les commandes slash
    @commands.command(name="sync")
    async def sync(self, ctx) -> None:
        fmt = await ctx.bot.tree.sync()
        await ctx.send(f"{len(fmt)} commandes ont été synchronisées.")
        
async def setup(bot):
    await bot.add_cog(Main(bot))