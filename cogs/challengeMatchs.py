import discord
from discord.ext import commands

from selenium import webdriver as scrap
from datetime import datetime as dt
import asyncio
from pytz import timezone

import var

tzone = timezone("Europe/Paris")

opts = scrap.ChromeOptions()
opts.add_argument("--headless")
opts.add_argument("--no-sandbox")
opts.add_argument("--disable-dev-shm-usage")

class ChallengeMatchs(commands.Cog):
    
    def __init__(self, bot) -> None:
        self.bot = bot
        self.driver = scrap.Chrome(options=opts)
        
        bot.loop.create_task(self.get_match_data())
        
    async def get_match_data(self) -> None:
        await self.bot.wait_until_ready()
        event_already_created = False
        
        while not self.bot.is_closed():
            self.driver.get(var.challenge_url)
            text_shadow_list = self.driver.find_elements("css selector", 'div.text-shadow')
            
            event_list = await self.bot.get_guild(1027361429529034843).fetch_scheduled_events()
            
            for event in event_list:
                if event.name == f"{text_shadow_list[1].text} - {text_shadow_list[2].text}":
                    event_already_created = True
                    break
                else:
                    event_already_created = False
                    
            if not event_already_created:
                font_splatoon2_list = self.driver.find_elements("css selector", 'div.font-splatoon2')
                #img = self.driver.find_elements("tag name", "img")
                
                description = f"{font_splatoon2_list[10].text}\n\nStages:\n{font_splatoon2_list[4].text}\n{font_splatoon2_list[5].text}"
                event = await self.bot.get_guild(1027361429529034843).create_scheduled_event(
                    name=f"{text_shadow_list[1].text} - {text_shadow_list[2].text}",
                    description=description,
                    channel=self.bot.get_channel(1027618500337995826),
                    entity_type=discord.EntityType.voice,
                    start_time=dt.strptime(f"{text_shadow_list[5].text[5:15]} 2023", "%d/%m %H:%M %Y").astimezone(tzone),
                    end_time= dt.strptime(f"{text_shadow_list[5].text[19:]} 2023", "%d/%m %H:%M %Y").astimezone(tzone),
                    privacy_level=discord.PrivacyLevel.guild_only)
                    #cover_image=discord.Asset(state=discord.VoiceState.channel, url=img[2].get_attribute("src"), key="img")
            
                await self.bot.get_channel(1027619568362983484).send(f"@everyone L'événement pour le nouveau match challenge a été créé ! - {event.url}")
            await asyncio.sleep(900)
    
async def setup(bot):
    await bot.add_cog(ChallengeMatchs(bot))