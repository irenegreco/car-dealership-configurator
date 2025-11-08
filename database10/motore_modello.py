from pony.orm import *

def define_motoreModello_entity(db, Motore, Modello):
    class MotoreModello(db.Entity):
        _table_ = "motore modello"  # Specifica il nome della tabella
        id = PrimaryKey(str)
        motore = Required(Motore, column = 'motore')
        modello = Required(Modello, column = 'modello')
        prezzo = Required(float)
        visibility = Required(str)
    return MotoreModello
