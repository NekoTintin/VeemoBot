from discord.ext import commands
from discord.embeds import Embed

import asyncio
from datetime import datetime as dt
from pytz import timezone
from requests import get
from os.path import exists, getsize

from data import vs_stages, rules

tzone = timezone("Europe/Paris")
url = "https://splatoon.oatmealdome.me/api/v1/three/versus/phases?count=12"
channel_id = 1034344413851299850
params = {'count': '12'}
headers = {'accept': 'application/json'}

class Ping_schedule(commands.Cog):
    
    def __init__(self, bot) -> None:
        self.bot = bot
        bot.loop.create_task(self._verify_data())
        super().__init__()
        
    async def _verify_data(self):
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(channel_id)
        
        while not self.bot.is_closed():
            if getsize("/home/Tintin/discord_bot/VeemoBot/last_message") == 0:
                #data = self._check_data()
                data = self._force_to_test()
                if data != None:
                    await channel.send(embed=self._create_embed(data))
                    end_time = dt.fromisoformat(data["endTime"][:-1])
                    with open("/home/Tintin/discord_bot/VeemoBot/last_message", "w") as file:
                        file.write(f"{end_time.hour:02d}:{end_time.minute:02d} {end_time.day}/{end_time.month}/{end_time.year}")          
            else:
                with open("/home/Tintin/discord_bot/VeemoBot/last_message", "r") as file:
                    endate = dt.strptime(file.read().strip(), "%H:%M %d/%m/%Y").replace(tzinfo=tzone)
                    if dt.now(tzone) >= endate:
                        await channel.purge()

                        with open("/home/Tintin/discord_bot/VeemoBot/last_message", "w") as empty_file:
                            empty_file.truncate(0)
                    else:
                        await self._send_reminder()
            await asyncio.sleep(60)

    def _create_embed(self, data: dict) -> Embed:
        emb = Embed(title=rules[data["BankaraOpen"]["rule"]]["name"], description=f"@everyone", color=0x290029,
                    url="https://splatoon.oatmealdome.me")
        emb.set_image(url=vs_stages[data["BankaraOpen"]["stages"][0]]["image"])
        emb.set_thumbnail(url=rules[data["BankaraOpen"]["rule"]]["icon"])
        emb.set_footer(icon_url="https://splatoon.oatmealdome.me/img/pwa/icon/apple-touch-icon-ipad-retina-152x152.png",
            text="Depuis splatoon.oatmealdome.me")
        emb.add_field(name="Stages",
            value=f'{vs_stages[data["BankaraOpen"]["stages"][0]]["name"]}\n{vs_stages[data["BankaraOpen"]["stages"][1]]["name"]}')
        emb.add_field(name='Horaires',
            value=f'De {data["startTime"][11:-4]} à {data["endTime"][11:-4]}')
        return emb
            
    def _check_data(self) -> dict:
        response = get(url, params=params, headers=headers)
        if response.status_code == 200:
            json_data = response.json()
                
            for mode in json_data["normal"]:
                rule = mode["BankaraOpen"]["rule"]
                start_time = dt.fromisoformat(mode["startTime"][:-1])
                    
                if (rule == "Clam" or rule == "Goal") and start_time.hour == 22:
                    return mode
            return None
        
    async def _send_reminder(self):
        if getsize("/home/Tintin/discord_bot/VeemoBot/last_message") != 0:
            if dt.now(tzone).hour == 16 and dt.now(tzone).minute == 0:
                await self.bot.get_channel(channel_id).send("@everyone, la session commencera dans **6 heures** !")
            elif dt.now(tzone).hour == 22 and dt.now(tzone).minute == 0:
                await self.bot.get_channel(channel_id).send("@everyone, la session a commencée !")
        
async def setup(bot) -> None:
    await bot.add_cog(Ping_schedule(bot))