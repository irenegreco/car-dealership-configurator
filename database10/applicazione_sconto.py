from pony.orm import *

#ApplicazioneSconto(preventivo, sconto)
def define_applicazioneSconto_entity(db, Preventivo, Sconto):
    class ApplicazioneSconto(db.Entity):
        _table_ = "scelta optional"  # Specifica il nome della tabella
        
        preventivo = Set('Preventivo')
        sconto = Set('Sconto')
    return ApplicazioneSconto