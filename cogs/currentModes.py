import discord
from discord.ext import commands
from discord.embeds import Embed

from selenium import webdriver as scrap
import asyncio
from datetime import datetime as dt
from pytz import timezone

import var

tzone = timezone("Europe/Paris")

opts = scrap.ChromeOptions()
opts.add_argument("--headless")
opts.add_argument("--no-sandbox")
opts.add_argument("--disable-dev-shm-usage")

class CurrentModes(commands.Cog):
    
    def __init__(self, bot) -> None:
        self.bot = bot
        
        bot.loop.create_task(self.get_match_data())
        
    async def get_match_data(self) -> None:
        await self.bot.wait_until_ready()

        while not self.bot.is_closed():
            current_dt = dt.now(tzone)
            channel = self.bot.get_channel(1120359792091865168)
            
            match_driver = scrap.Chrome(options=opts)
            salmon_driver = scrap.Chrome(options=opts)
            
            if current_dt.hour in [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22] and current_dt.minute == 0:
            #if current_dt.minute >= 0: # To test when not working
                await channel.purge()
                
                match_driver.get(var.planning_url)
                match_font_splatoon2_list = match_driver.find_elements("css selector", 'div.font-splatoon2')
                match_bg_opacity_list = match_driver.find_elements("css selector", "div.bg-opacity-80")
                match_text_shadow_list = match_driver.find_elements("css selector", "div.text-shadow")
                match_img_list = match_driver.find_elements("tag name", "img")
                
                salmon_driver.get(var.salmon_run_url)
                salmon_font_splatoon2_list = salmon_driver.find_elements("css selector", 'div.font-splatoon2')
                salmon_img_list = salmon_driver.find_elements("tag name", "img")
                salmon_img_w_6 = salmon_driver.find_elements("css selector", "img.w-6")
                salmon_text_shadow_list = salmon_driver.find_elements("css selector", "div.text-shadow")
                

                # Embed des Matchs Classiques
                msg_classic = Embed(title="Match Classique - Guerre de Territoire", description="", color=0x17c41a)
                msg_classic.add_field(name="Stages", value=f"{match_font_splatoon2_list[3].text}\n{match_font_splatoon2_list[4].text}", inline=False)
                msg_classic.add_field(name="Horaires", value=f"{match_bg_opacity_list[0].text}")
                msg_classic.set_thumbnail(url="https://cdn.wikimg.net/en/splatoonwiki/images/thumb/4/48/S2_Icon_Regular_Battle.svg/2048px-S2_Icon_Regular_Battle.svg.png")
                msg_classic.set_image(url=f"{match_img_list[2].get_attribute('src')}")
                msg_classic.set_footer(icon_url="https://splatoon3.ink/apple-touch-icon.png", text="Depuis Splatoon3.ink")

                msg_series = Embed(title=f"Match Anarchie (Série) - {match_text_shadow_list[8].text}", description="", color=0xe54412)
                msg_series.add_field(name="Stages", value=f"{match_font_splatoon2_list[12].text}\n{match_font_splatoon2_list[13].text}", inline=False)
                msg_series.add_field(name="Horaires", value=f"{match_bg_opacity_list[1].text}")
                msg_series.set_thumbnail(url="https://cdn.wikimg.net/en/splatoonwiki/images/thumb/c/c5/S2_Icon_Ranked_Battle.svg/2048px-S2_Icon_Ranked_Battle.svg.png")
                msg_series.set_image(url=f"{match_img_list[10].get_attribute('src')}")
                msg_series.set_footer(icon_url="https://splatoon3.ink/apple-touch-icon.png", text="Depuis Splatoon3.ink")

                msg_open = Embed(title=f"Match Anarchie (Ouvert) - {match_text_shadow_list[15].text}", description="", color=0xe54412)
                msg_open.add_field(name="Stages", value=f"{match_font_splatoon2_list[21].text}\n{match_font_splatoon2_list[22].text}", inline=False)
                msg_open.add_field(name="Horaires", value=f"{match_bg_opacity_list[2].text}")
                msg_open.set_thumbnail(url="https://cdn.wikimg.net/en/splatoonwiki/images/thumb/c/c5/S2_Icon_Ranked_Battle.svg/2048px-S2_Icon_Ranked_Battle.svg.png")
                msg_open.set_image(url=f"{match_img_list[18].get_attribute('src')}")
                msg_open.set_footer(icon_url="https://splatoon3.ink/apple-touch-icon.png", text="Depuis Splatoon3.ink")


                # Salmon Run
                msg_salmon = Embed(title="Salmon Run: Next Wave", description=None, color=0xec5002)
                weapon_list = f"{salmon_img_list[3].accessible_name}\n{salmon_img_list[4].accessible_name}\n{salmon_img_list[5].accessible_name}\n{salmon_img_list[6].accessible_name}"
                msg_salmon.add_field(name="Armes fournies", value=weapon_list, inline=False)

                msg_salmon.add_field(name="Stage", value=salmon_font_splatoon2_list[4].text, inline=True)
                msg_salmon.add_field(name="Horaires", value=salmon_text_shadow_list[1].text, inline=True)
                if "Horrorboros" in salmon_img_w_6[1].accessible_name:
                    msg_salmon.add_field(name="Salmonarque", value="Salmophide", inline=True)
                else:
                    msg_salmon.add_field(name="Salmonarque", value="Salmotori", inline=True)
        
                msg_salmon.set_thumbnail(url="https://cdn.wikimg.net/en/splatoonwiki/images/thumb/f/f0/SplatNet_3_icon_Salmon_Run.svg/2048px-SplatNet_3_icon_Salmon_Run.svg.png")
                msg_salmon.set_image(url=salmon_img_list[2].get_attribute("src"))
                msg_salmon.set_footer(icon_url="https://splatoon3.ink/apple-touch-icon.png", text="Depuis Splatoon3.ink")

                await channel.send(embed=msg_classic)
                await channel.send(embed=msg_series)
                await channel.send(embed=msg_open)

                if "Aléatoire" in weapon_list:
                    await channel.send(content="@everyone, au moins une arme aléatoire est disponible pour cette rotation !", embed=msg_salmon)
                else:
                    await channel.send(embed=msg_salmon)
                
            match_driver.quit()
            salmon_driver.quit()
            await asyncio.sleep(60)
        
async def setup(bot):
    await bot.add_cog(CurrentModes(bot))