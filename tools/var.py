# Dictionnaire qui stocke les cogs chargés
loaded_ext = list()

online_message = "la rotation des stages."
ver_num = "0.8.0"

# Fonction pour obtenir les modules chargés
def get_modules() -> list:
    l = list()
    for filename in loaded_ext:
        l.append(filename)
    return l

def add_module(name):
    loaded_ext.append(name)
    
def remove_module(name):
    loaded_ext.remove(name)
