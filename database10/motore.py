#Motore(codice, alimentazione, prezzo)
from pony.orm import *

# Definizione dell'entità Motore
def define_motore_entity(db):
    class Motore(db.Entity):
        _table_ = "motori"  # Specifica il nome della tabella
        codice = PrimaryKey(str)
        alimentazione = Required(str)
        visibility = Required(str)
        
        auto = Set('Auto') #si riferisce al nome della classe
        motore_modello = Set('MotoreModello') #si riferisce al nome della classe
    return Motore