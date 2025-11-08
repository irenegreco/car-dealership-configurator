from pony.orm import *

def define_messaggio_entity(db, Ordine):
    class Messaggio(db.Entity):
        _table_ = "messaggi"
        ordine =  Required(Ordine, column = 'ordine')
        testo = Required(str)
        lettura = Optional(str)
    return Messaggio
