from pony.orm import *

def define_coloreModello_entity(db, Colore, Modello):
    class ColoreModello(db.Entity):
        _table_ = "colore modello"  # Specifica il nome della tabella
        id = PrimaryKey(str)
        colore = Required(Colore, column = 'colore')
        modello = Required(Modello, column = 'modello')
        prezzo = Required(float)
        visibility = Required(str)

    return ColoreModello
