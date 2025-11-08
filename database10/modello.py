from pony.orm import *

#Modello(nome, brand, altezza, lunghezza, larghezza, peso, bagagliaio, prezzo_base)
def define_modello_entity(db, Brand):
    
    class Modello(db.Entity):
        _table_ = "modelli"  # Specifica il nome della tabella
        nome = PrimaryKey(str)
        brand = Required("Brand", column= 'brand')
        altezza = Required(int)
        lunghezza = Required(int)
        larghezza = Required(int)
        peso = Required(float)
        bagagliaio = Required(int)
        prezzo_base = Required(float)
        descrizione = Required(str)
        visibility = Required(str)
        
        auto = Set('Auto') #si riferisce al nome della classe
        immagine = Set('Immagine') #si riferisce al nome della classe
        optional_modello = Set('OptionalModello') #si riferisce al nome della classe
        colore_modello = Set('ColoreModello') #si riferisce al nome della classe
        motore_modello = Set('MotoreModello') #si riferisce al nome della classe
        sconto_modello = Set('ScontoModello')
    return Modello