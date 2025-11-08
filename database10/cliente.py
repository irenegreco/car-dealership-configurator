#Cliente(username, nome, cognome, pw)
from pony.orm import *

def define_cliente_entity(db):
    class Cliente(db.Entity):
        _table_ = "clienti"  # Specifica il nome della tabella
        email = PrimaryKey(str)
        pw = Required(str)
        name = Required(str)
        surname = Required(str)

        
        auto_usata = Set('AutoUsata') #si riferisce al nome della classe
        auto = Set('Auto') #si riferisce al nome della classe
        preventivo = Set('Preventivo') #si riferisce al nome della classe
        
        def get_id(self):
            return self.email
        
        def is_authenticated(self):
            return True
        
        def is_active(self):
            return True
        
    return Cliente