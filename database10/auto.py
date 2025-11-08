from pony.orm import *

#Auto(codice, prezzo_totale, cliente, modello, brand, colore, motore)
def define_auto_entity(db, Colore, Motore, Modello, Cliente, Brand):
    class Auto(db.Entity):
        _table_ = "auto"  # Specifica il nome della tabella
        codice = PrimaryKey(str)
        prezzo_totale = Required(float)
        cliente = Required(Cliente, column= 'username')
        modello = Required(Modello, column= 'nome')
        colore = Required(Colore, column= 'colore')
        motore = Required(Motore, column= 'motore')
        
        preventivo = Set('Preventivo') 
        scelta_optional = Set('SceltaOptional') 
        
    return Auto