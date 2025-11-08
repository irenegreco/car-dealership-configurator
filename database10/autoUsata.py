#AutoUsata(targa, modello, proprietario, valutatore)
from pony.orm import *

def define_autoUsata_entity(db, Cliente, Impiegato):
    class AutoUsata(db.Entity):
        _table_ = "auto usate"  # Specifica il nome della tabella
        targa = PrimaryKey(str)
        proprietario = Required(Cliente, column= 'proprietario') #foreign key
        valutatore = Required(Impiegato, column= 'valutatore') #foreign key
        
        preventivo = Set('Preventivo') #si riferisce al nome della classe
        fotoUsato = Set('FotoUsato') #si riferisce al nome della classe
    return AutoUsata