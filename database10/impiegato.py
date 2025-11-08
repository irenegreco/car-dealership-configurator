#Impiegato(matricola, nome, cognome, username, pw)
from pony.orm import *

def define_impiegato_entity(db):
    class Impiegato(db.Entity):
        _table_ = "impiegati"  # Specifica il nome della tabella
        matricola = PrimaryKey(str)
        name = Required(str)
        surname = Required(str)
        pw = Required(str)
        
        valutazione_auto = Set('AutoUsata') #si riferisce al nome della classe
        ordine = Set('Ordine') #si riferisce al nome della classe
               
        
        def get_id(self):
            return self.matricola
        
        def is_authenticated(self):
            return True

        def is_active(self):
            return True

        
    return Impiegato