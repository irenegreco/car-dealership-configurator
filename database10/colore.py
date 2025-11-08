#Colore(nome)
from pony.orm import *

# Definizione dell'entità Colori
def define_colore_entity(db):
    class Colore(db.Entity):
        _table_ = "colori"  # Specifica il nome della tabella
        nome = PrimaryKey(str)
        visibility = Required(str)

        auto = Set('Auto') #si riferisce al nome della classe
        immagine = Set('Immagine') #si riferisce al nome della classe
        colore_modello = Set('ColoreModello') #si riferisce al nome della classe
    return Colore