import discord
from discord.ext import commands

from platform import python_version

import tools.var as var

class Main(commands.Cog):
    
    def __init__(self, bot) -> None:
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("Démarrage du VeemoBot")
        print(f"Version Python: {python_version()}")
        print(f"Version Discord.py: {discord.__version__ }")
        print(f"Version du bot: {var.ver_num}")
        await self.bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching,
            name=var.online_message))
        
    # Se déclenche à chaque message
    @commands.Cog.listener()
    async def on_message(self, message):
        msg_str = str(message.content)
        if message.author == self.bot.user:
            return
        if self.bot.user.mentioned_in(message) and message.mention_everyone == False:
            await message.channel.send(f"Hey {message.author.mention}, utilise **/** pour afficher la liste des commandes.")
        
    # Pour synchroniser les commandes slash
    @commands.command(name="sync")
    async def sync(self, ctx) -> None:
        fmt = await ctx.bot.tree.sync()
        await ctx.send(f"{len(fmt)} commandes ont été synchronisées.")
        
    # Permet de charger un cog
    @commands.command(name="load")
    async def load(self, ctx, extention):
        await ctx.message.delete()
        await self.bot.load_extension(f"cogs.{extention}")
        var.add_module(extention)
        await ctx.send(f"Le module {extention} a bien été chargé")
        
    # Permet de décharger un cog
    @commands.command(name="unload")
    async def unload(self, ctx, extention):
        await ctx.message.delete()
        await self.bot.unload_extension(f"cogs.{extention}")
        var.remove_module(extention)
        await ctx.send(f"Le module {extention} a bien été déchargé")
        
    # Permet de recharger un cog
    @commands.command(name="reload")
    async def reload(self, ctx, extention):
        await ctx.message.delete()
        await self.bot.unload_extension(f"cogs.{extention}")
        await self.bot.load_extension(f"cogs.{extention}")
        await ctx.send(f"Le module {extention} a bien été rechargé")
        
    # Envoie un message avec la liste des modules chargés
    @commands.command(name="modules", aliases=['mod'])
    async def modules(self, ctx):
        message = f"Liste des modules chargés:\n"
        for mod in var.get_modules():
            message += f"- **{mod}**\n"
        await ctx.send(message)
        
async def setup(bot):
    await bot.add_cog(Main(bot))