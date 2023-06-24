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

class salmonRun(commands.Cog):

    def __init__(self, bot) -> None:
        self.bot = bot
        self.driver = scrap.Chrome(options=opts)

        bot.loop.create_task(self.salmonRun())
        super().__init__()

    async def salmonRun(self) -> None:
        await self.bot.wait_until_ready()

        while not self.bot.is_closed():
            channel = self.bot.get_channel(1120359792091865168)

            self.driver.get(var.salmon_run_url)

            text_shadow_list = self.driver.find_elements("css selector", "div.text-shadow")

            raw_date = text_shadow_list[1].text
            cuted_date = raw_date.split(" – ")[0]
            date = dt.strptime(cuted_date, "%d/%m %H:%M")
            now = dt.now(tzone)

            if date.astimezone(tzone) <= now:
                font_splatoon2_list = self.driver.find_elements("css selector", 'div.font-splatoon2')
                img_list = self.driver.find_elements("tag name", "img")
                img_w_6 = self.driver.find_elements("css selector", "img.w-6")

                msg_salmon = Embed(title="Salmon Run: Next Wave", description=None, color=0xec5002)
                weapon_list = f"{img_list[3].accessible_name}\n{img_list[4].accessible_name}\n{img_list[5].accessible_name}\n{img_list[6].accessible_name}"
                msg_salmon.add_field(name="Armes fournies", value=weapon_list, inline=False)

                msg_salmon.add_field(name="Stage", value=font_splatoon2_list[4].text, inline=True)
                msg_salmon.add_field(name="Horaires", value=text_shadow_list[1].text, inline=True)
                if "Horrorboros" in img_w_6[1].accessible_name:
                    msg_salmon.add_field(name="Salmonarque", value="Salmophide", inline=True)
                else:
                    msg_salmon.add_field(name="Salmonarque", value="Salmotori", inline=True)
        
                msg_salmon.set_thumbnail(url="https://cdn.wikimg.net/en/splatoonwiki/images/thumb/f/f0/SplatNet_3_icon_Salmon_Run.svg/2048px-SplatNet_3_icon_Salmon_Run.svg.png")
                msg_salmon.set_image(url=img_list[2].get_attribute("src"))
                msg_salmon.set_footer(icon_url="https://splatoon3.ink/apple-touch-icon.png", text="Depuis Splatoon3.ink")

                if "Aléatoire" in weapon_list:
                    await channel.send(content="@everyone, au moins une arme aléatoire est disponible pour cette rotation !", embed=msg_salmon)
                else:
                    await channel.send(embed=msg_salmon)
            
            await asyncio.sleep(60)

async def setup(bot):
    await bot.add_cog(salmonRun(bot))