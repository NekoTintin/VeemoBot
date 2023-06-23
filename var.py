driver_path = "/home/Tintin/discord_bot/VeemoBot/chromedriver/chromedriver"

challenge_url = "https://splatoon3.ink/challenges"
planning_url = "https://splatoon3.ink/"

# Dictionnaire qui stocke les cogs chargés
loaded_ext = list()

online_message = "la rotation des stages"
ver_num = "0.2.0"

# Fonction pour obtenir les modules chargés
def get_modules() -> list():
    l = list()
    for filename in loaded_ext:
        l.append(filename)
    return l

def add_module(name):
    loaded_ext.append(name)
    
def remove_module(name):
    loaded_ext.remove(name)