from pony.orm import *

def define_optionalModello_entity(db, Optional, Modello):
    class OptionalModello(db.Entity):
        _table_ = "optional modello"  # Specifica il nome della tabella
        id = PrimaryKey(str)
        optional = Required(Optional, column = 'optional')
        modello = Required(Modello, column = 'modello')
        prezzo = Required(float)
        visibility = Required(str)

    return OptionalModello
