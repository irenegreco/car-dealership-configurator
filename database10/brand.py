from pony.orm import *

# Definizione dell'entità Brand
def define_brand_entity(db):
    class Brand(db.Entity):
        _table_ = "brand"  # Specifica il nome della tabella
        nome = PrimaryKey(str)
        visibility = Required(str)

        modello = Set('Modello') #si riferisce al nome della classe
    return Brand
