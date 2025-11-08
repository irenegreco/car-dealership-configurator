#Sede(nome, indirizzo)
from pony.orm import *

# Definizione dell'entità Sede
def define_sede_entity(db):
    class Sede(db.Entity):
        _table_ = "sedi"  # Specifica il nome della tabella
        nome = PrimaryKey(str)
        indirizzo = Required(str)
        
        ordine = Set('Ordine') #si riferisce al nome della classe
    return Sede