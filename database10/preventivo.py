from pony.orm import *
from sqlite3 import Date
#Preventivo(codice, data, auto, cliente, sconto*, auto_rottamata*, valore_sconto_rottamazione*, prezzo)
def define_preventivo_entity(db, Cliente, Auto, Sconto, AutoUsata):
    class Preventivo(db.Entity):
        _table_ = "preventivi"  # Specifica il nome della tabella
        codice = PrimaryKey(str)
        data = Required(Date)
        auto = Required(Auto, column= 'auto')
        cliente = Required(Cliente, column= 'cliente')
        sconto_mese= Optional(Sconto, column= 'sconto')
        valore_sconto = Optional(float)
        auto_rottamata = Optional(AutoUsata, column= 'auto usata')
        valore_sconto_rottamazione = Optional(float)
        prezzo = Required(float)

        ordine = Set('Ordine') #si riferisce al nome della classe
    return Preventivo