from pony import orm
from pony.orm import *
import re


# CREAZIONE DB
db = Database()
db.bind(provider='sqlite', filename='database.db', create_db=True)

# Importa e definisce l'entità Cliente
from database10.cliente import define_cliente_entity
#from cliente import define_cliente_entity
cliente_class = define_cliente_entity(db)

# Importa e definisce l'entità Segreteria
from database10.segreteria import define_segreteria_entity
#from segreteria import define_segreteria_entity
segreteria_class = define_segreteria_entity(db)

# Importa e definisce l'entità Impiegato
from database10.impiegato import define_impiegato_entity
#from impiegato import define_impiegato_entity
impiegato_class = define_impiegato_entity(db)

# Importa e definisce l'entità AutoUsata
from database10.autoUsata import define_autoUsata_entity
#from autoUsata import define_autoUsata_entity
autoUsata_class = define_autoUsata_entity(db, cliente_class, impiegato_class)

# Importa e definisce l'entità AutoUsata
from database10.foto_usato import define_fotoUsato_entity
#from foto_usato import define_fotoUsato_entity
fotoUsato_class = define_fotoUsato_entity(db, autoUsata_class)

# Importa e definisce l'entità Brand
from database10.brand import define_brand_entity
#from brand import define_brand_entity
brand_class = define_brand_entity(db)

# Importa e definisce l'entità Colore
from database10.colore import define_colore_entity
#from colore import define_colore_entity
colore_class = define_colore_entity(db)

# Importa e definisce l'entità Modello
from database10.modello import define_modello_entity
#from modello import define_modello_entity
modello_class = define_modello_entity(db, brand_class)

# Importa e definisce l'entità Motore
from database10.motore import define_motore_entity
#from motore import define_motore_entity
motore_class = define_motore_entity(db)

# Importa e definisce l'entità Auto
from database10.auto import define_auto_entity
#from auto import define_auto_entity
auto_class = define_auto_entity(db, colore_class, motore_class, modello_class, cliente_class, brand_class)

# Importa e definisce l'entità Optional
from database10.optional import define_optional_entity
#from optional import define_optional_entity
optional_class = define_optional_entity(db)

# Importa e definisce l'entità Sede
from database10.sede import define_sede_entity
#from sede import define_sede_entity
sede_class = define_sede_entity(db)

# Importa e definisce l'entità Sconto
from database10.sconto_mese import define_sconto_entity
#from sconto_mese import define_sconto_entity
sconto_class = define_sconto_entity(db)

# Importa e definisce l'entità Preventivo
from database10.preventivo import define_preventivo_entity
#from preventivo import define_preventivo_entity
preventivo_class = define_preventivo_entity(db, cliente_class, auto_class, sconto_class, autoUsata_class)

# Importa e definisce l'entità Ordine
from database10.ordine import define_ordine_entity
#from ordine import define_ordine_entity
ordine_class = define_ordine_entity(db, sede_class, preventivo_class, impiegato_class)

# Importa e definisce l'entità Immagine
from database10.immagine import define_immagine_entity
#from immagine import define_immagine_entity
immagine_class = define_immagine_entity(db, colore_class, modello_class, brand_class)

# Importa e definisce l'entità SceltaOptional
from database10.scelta_optional import define_sceltaOptional_entity
#from scelta_optional import define_sceltaOptional_entity
sceltaOptional_class = define_sceltaOptional_entity(db, auto_class, optional_class)

# Importa e definisce l'entità OptionalModello
from database10.optional_modello import define_optionalModello_entity
#from optional_modello import define_optionalModello_entity
optionalModello_class = define_optionalModello_entity(db, optional_class, modello_class)

# Importa e definisce l'entità ColoreModello
from database10.colore_modello import define_coloreModello_entity
#from colore_modello import define_coloreModello_entity
coloreModello_class = define_coloreModello_entity(db, colore_class, modello_class)

# Importa e definisce l'entità ColoreModello
from database10.motore_modello import define_motoreModello_entity
#from motore_modello import define_motoreModello_entity
motoreModello_class = define_motoreModello_entity(db, motore_class, modello_class)

# Importa e definisce l'entità ScontoModello
from database10.sconto_modello import define_scontoModello_entity
#from sconto_modello import define_scontoModello_entity
scontoModello_class = define_scontoModello_entity(db, sconto_class, modello_class)

# Importa e definisce l'entità Messaggio
from database10.messaggio import define_messaggio_entity
messaggio_class = define_messaggio_entity(db, ordine_class)


# Genera il mapping delle entità e crea le tabelle
db.generate_mapping(create_tables=True)

# FUNZIONI
# validazione username
@db_session
def is_username_taken (username):
    return cliente_class.get(email=username)

@db_session
def validate_registration(name, surname, username, password):
    # Verifica che lo username sia un'email valida
    if not re.match(r"[^@]+@[^@]+\.[^@]+", username):
        return False, "Lo username non è un'email valida"

    if is_username_taken(username):
        return False, "Username già in uso"
    if len(username) < 4:
        return False, "Username deve essere almeno 4 caratteri"
    if len(password) < 6:
        return False, "Password deve essere almeno 6 caratteri"
    if len(name) < 2:
        return False, "Nome deve essere almeno 2 caratteri"
    if len(surname) < 2:
        return False, "Cognome deve essere almeno 2 caratteri"
    return True, "Registrazione avvenuta con successo"


# validazione login Personale
@db_session
def authenticatePersonale(username, password) -> tuple[bool, int, str]:
    # Cerca l'utente nel database in base allo username
    segreteria = segreteria_class.get(matricola=username)
    tipo = 1
    if not segreteria or not segreteria.pw == password:
        impiegato = impiegato_class.get(matricola=username)
        tipo = 2
    # Se non trova l'utente o la password non corrisponde, restituisci False
        if not impiegato or not impiegato.pw == password:
            tipo = 0
            return False, tipo, "Utente non trovato o password errata"

    # Se le credenziali sono corrette, restituisci True
    return True, tipo, "Utente trovato"