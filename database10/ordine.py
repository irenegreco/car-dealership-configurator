from pony.orm import *
from sqlite3 import Date
#Ordine(codice, data_ordine, data_consegna, preventivo, sede_ritiro, gestore_ordine)
def define_ordine_entity(db, Sede, Preventivo, Impiegato):
    class Ordine(db.Entity):
        _table_ = "ordini"  # Specifica il nome della tabella
        codice = PrimaryKey(str)
        data_ordine = Required(Date)
        data_consegna = Required(Date)
        preventivo = Required(Preventivo, column= 'id')
        sede_ritiro = Required(Sede, column= 'sede') #foreign key
        gestore_ordine = Optional(Impiegato, column= 'impiegato') #foreign key
        bollettino = Required(bytes)
        
        messaggio = Set('Messaggio')

    return Ordine