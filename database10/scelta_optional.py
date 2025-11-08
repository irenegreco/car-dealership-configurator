from pony.orm import *

#SceltaOptional(auto, optional)
def define_sceltaOptional_entity(db, Auto, Optional):
    class SceltaOptional(db.Entity):
        _table_ = "scelta optional"  # Specifica il nome della tabella
        
        auto = Required(Auto, column= 'auto')
        optional = Required(Optional, column='nome')
    return SceltaOptional
