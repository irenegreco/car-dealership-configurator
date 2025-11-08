from pony import orm
from pony.orm import *
from database import *

# Inserimento delle sedi
@db_session()
def set_sede(Sede, name, ind):
   Sede(
       nome = name,
       indirizzo = ind
   )

n1 = 'Heaven Motors Montinsola'
i1 = 'Via Roma, 123, Montisola (BS)'
set_sede(sede_class, n1, i1)

n2 = 'Heaven Motors Modena'
i2 = 'Via Milano, 321, Modena (MO)'
set_sede(sede_class, n2, i2)

n1 = 'Heaven Motors Reggio Emilia'
i1 = 'Via Reggio Calabria, 1, Reggio Emilia (RE)'
set_sede(sede_class, n1, i1)

n2 = 'Heaven Motors Verona'
i2 = 'Strada Le Grazie, 15, Verona (VR)'
set_sede(sede_class, n2, i2)

# Inserimento degli impiegati
@db_session()
def set_impiegato(Impiegato, mat, nome, cognome, psw):
   Impiegato(
       matricola = mat,
        name = nome,
        surname = cognome,
        pw = psw
   )

mat1 = 'i001'
n1 = 'Maria'
c1 = 'Stuarda'
psw1 = 'venturini1234'
set_impiegato(impiegato_class, mat1, n1, c1, psw1)

mat2 = 'i002'
n2 = 'Luigi'
c2 = 'Mario'
psw2 = 'nonLaso1'
set_impiegato(impiegato_class, mat2, n2, c2, psw2)

mat3 = 'i003'
n3 = 'Emiliana'
c3 = 'Roma'
psw3 = 'password2'
set_impiegato(impiegato_class, mat3, n3, c3, psw3)

mat4 = 'i004'
n4 = 'Luca'
c4 = 'Lowis'
psw4 = 'pass4word'
set_impiegato(impiegato_class, mat4, n4, c4, psw4)

# Inserimento della segreteria
@db_session()
def set_segreteria(Segreteria, mat, nome, cognome, psw):
   Segreteria(
       matricola = mat,
        name = nome,
        surname = cognome,
        pw = psw
   )

mat1 = 's001'
n1 = 'Marco'
c1 = 'Bruni'
psw1 = 'orsoPolare'
set_segreteria(segreteria_class, mat1, n1, c1, psw1)

mat2 = 's002'
n2 = 'Celide'
c2 = 'Dion'
psw2 = 'nonSonoio'
set_segreteria(segreteria_class, mat2, n2, c2, psw2)
