from pony.orm import *

def define_scontoModello_entity(db, Sconto, Modello):
    class ScontoModello(db.Entity):
        _table_ = "sconto modello"  # Specifica il nome della tabella
        id = PrimaryKey(str)
        sconto = Required(Sconto, column = 'sconto')
        modello = Required(Modello, column = 'modello')
        visibility = Required(str)
        
    return ScontoModello
