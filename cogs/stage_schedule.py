from discord.ext import commands
from discord.embeds import Embed

import asyncio
from datetime import datetime as dt
from pytz import timezone
import requests

from data.splatoon_data import vs_stages, vs_modes, rules, coop_stages, boss, weapons

tzone = timezone('Europe/Paris')
url = "https://splatoon.oatmealdome.me/api/v1/three/versus/phases?count=1"
url_salmon = "https://splatoon.oatmealdome.me/api/v1/three/coop/phases?count=1"
params = {'count': '1'}
headers = {'accept': 'application/json'}

def create_embed(json_dict: dict, mode: str, color, is_unlimited: bool=False) -> Embed:
    msg = Embed(title=f"{vs_modes[mode]} - {rules[json_dict['rule']]['name']}", description=None, color=color,
                url="https://splatoon.oatmealdome.me")
    if not is_unlimited:
        msg.add_field(name="Stages", value=f"{vs_stages[json_dict['stages'][0]]['name']}\n{vs_stages[json_dict['stages'][1]]['name']}")
    else:
        stages_list = str()
        for stage_name in json_dict['stages']:
            stages_list += f"{vs_stages[stage_name]['name']}\n"
        msg.add_field(name="Stages", value=stages_list)
    msg.set_thumbnail(url=rules[json_dict["rule"]]["icon"])
    msg.set_image(url=vs_stages[json_dict['stages'][0]]['image'])
    msg.set_footer(icon_url="https://splatoon.oatmealdome.me/img/pwa/icon/apple-touch-icon-ipad-retina-152x152.png",
        text="Depuis splatoon.oatmealdome.me")
    return msg

def create_embed_salmon(json_dict: dict) -> Embed:
    weapon_list = ""
    
    msg = Embed(title="Salmon Run: Next Wave", description=None, color=0xec5002, url="https://splatoon.oatmealdome.me")
    msg.add_field(name="Stage", value=coop_stages[json_dict[0]['stage']]['name'])
    msg.add_field(name="Salmonarque", value=boss[json_dict[0]['bigBoss']]['name'])
    
    for weapon in json_dict[0]['weapons']:
        if weapons[weapon] not in weapon_list:
            weapon_list += f"{weapons[weapon]}\n"
    msg.add_field(name="Armes disponibles", inline=False, value=weapon_list)
    
    if json_dict[0]["rareWeapons"] != []:
        rare_weapon_list = ""
        for weapon in json_dict[0]["rareWeapons"]:
            rare_weapon_list += f"{weapons[weapon]}\n"
        msg.add_field(name="Armes Rares", value=rare_weapon_list)
    msg.set_image(url=coop_stages[json_dict[0]['stage']]['image'])
    msg.set_thumbnail(url=boss[json_dict[0]['bigBoss']]['icon'])
    msg.set_footer(icon_url="https://splatoon.oatmealdome.me/img/pwa/icon/apple-touch-icon-ipad-retina-152x152.png",
                   text="Depuis splatoon.oatmealdome.me")
    return msg

class Match_stage(commands.Cog):

    def __init__(self, bot) -> None:
        self.bot = bot
        bot.loop.create_task(self._stage_task())

    async def _stage_task(self):
        await self.bot.wait_until_ready()

        while not self.bot.is_closed():
            current_time = dt.now(tzone)
            channel = self.bot.get_channel(1120359792091865168)

            if current_time.hour % 2 != 0 and current_time.minute == 0:
            #if current_time.minute >= 0: # To test when not working
                response = requests.get(url, params=params, headers=headers)
                salmon_response = requests.get(url_salmon, params=params, headers=headers)

                if response.status_code == 200:
                    await channel.purge()
                    json_data = response.json()

                    if json_data["normal"] != []:
                        await channel.send(embed=create_embed(json_data["normal"][0]["Regular"], "Regular", 0x17c41a))
                        await channel.send(embed=create_embed(json_data["normal"][0]["Bankara"], "Bankara", 0xe54412))
                        await channel.send(embed=create_embed(json_data["normal"][0]["BankaraOpen"], "BankaraOpen", 0xe54412))
                        await channel.send(embed=create_embed(json_data["normal"][0]["X"], "X", 0x67ddab))
                    else:
                        ite = iter(json_data["fest"].items())
                        key, val = next(ite)
                        
                        await channel.send(embed=create_embed(json_data["fest"][key][0]["FestRegular"], "FestRegular", 0x06ff97))
                        await channel.send(embed=create_embed(json_data["fest"][key][0]["FestChallenge"], "FestChallenge", 0xffbe2e))
                        if json_data["fest"][key][0]["FestTriColor"]["rule"] != None:
                            await channel.send(embed=create_embed(json_data["fest"][key][0]["FestTriColor"], "FestTriColor", 0xffbe2e, True))
                else:
                    return False
                
                if salmon_response.status_code == 200:
                    json_data = salmon_response.json()
                    await channel.send(embed=create_embed_salmon(json_data["Normal"]))
                else:
                    return False
            await asyncio.sleep(60)

async def setup(bot):
    await bot.add_cog(Match_stage(bot))