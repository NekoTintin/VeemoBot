from os import listdir

import discord
from discord.ext import commands
from discord.embeds import Embed
import asyncio

import passwords as passwd

default_intents = discord.Intents.default()
default_intents.message_content = True
default_intents.guild_scheduled_events = True
bot = commands.Bot(command_prefix=";", intents=default_intents, help_command=None)

@bot.command()
async def startup(bot) -> None:
    async with bot:
        for file in listdir('/home/Tintin/discord_bot/VeemoBot/cogs'):
            if file.endswith(".py"):
                await bot.load_extension(f"cogs.{file[:-3]}")
        await bot.start(passwd.bot_token)
        
asyncio.run(startup(bot))