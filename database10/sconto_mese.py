#Sconto(codice, dal, al, percenuale)
from sqlite3 import Date
from pony.orm import *

# Definizione dell'entità Sconto
def define_sconto_entity(db):
    class Sconto(db.Entity):
        _table_ = "sconti"  # Specifica il nome della tabella
        codice = PrimaryKey(str)
        dal = Required(Date)
        al = Required(Date)
        percentuale = Required(float)

        preventivo = Set('Preventivo') #si riferisce al nome della classe
        sconto_modello = Set('ScontoModello')

    return Sconto