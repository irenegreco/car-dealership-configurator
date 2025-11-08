#Immagine(codice, colore, modello, brand)
from pony.orm import *

# Definizione dell'entità Colori
def define_immagine_entity(db, Colore, Modello, Brand):
    class Immagine(db.Entity):
        _table_ = "immagini"  # Specifica il nome della tabella
        codice = PrimaryKey(str)
        codiceURL = Required(str)
        colore = Required(Colore, column='colore')
        modello =  Required(Modello, column='modello')
        visibility = Required(str)
    return Immagine