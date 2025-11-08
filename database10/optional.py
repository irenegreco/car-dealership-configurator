#Optional(codice, alimentazione)
from pony.orm import *

# Definizione dell'entità Optional
def define_optional_entity(db):
    class Optional(db.Entity):
        _table_ = "optional"  # Specifica il nome della tabella
        nome = PrimaryKey(str)
        visibility = Required(str)

        scelta_optional = Set('SceltaOptional') #si riferisce al nome della classe
        optional_modello = Set('OptionalModello') #si riferisce al nome della classe
    return Optional