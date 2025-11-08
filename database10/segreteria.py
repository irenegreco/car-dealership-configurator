#Segreteria(matricola, nome, cognome, username, pw)
from pony.orm import *

def define_segreteria_entity(db):
    class Segreteria(db.Entity):
        _table_ = "segreteria"  # Specifica il nome della tabella
        matricola = PrimaryKey(str)
        name = Required(str)
        surname = Required(str)
        pw = Required(str)
        
        def get_id(self):
            return self.matricola
        
        def is_authenticated(self):
            return True

        def is_active(self):
            return True

    return Segreteria