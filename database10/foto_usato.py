#FotoUsato(codice, targaUsato, file)
from pony.orm import *

def define_fotoUsato_entity(db, AutoUsata):
    class FotoUsato(db.Entity):
        _table_ = "foto auto usate"  # Specifica il nome della tabella
        codice = PrimaryKey(str)
        targaUsato = Required(AutoUsata, column= 'targaUsato') #foreign key
        file = Required(bytes)
        
        #preventivo = Set('Preventivo') #si riferisce al nome della classe
    return FotoUsato