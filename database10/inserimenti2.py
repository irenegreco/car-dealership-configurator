from pony import orm
from pony.orm import *
from database import *
import datetime

# Inserimento dei brand
@db_session()
def set_brand(Brand, name, vis):
   Brand(
       nome = name,
       visibility = vis
   )

n1 = 'Ferrari'
set_brand(brand_class, n1, 'si')
n2 = 'Porsche'
set_brand(brand_class, n2, 'si')
n3 = 'Mercedes'
set_brand(brand_class, n3, 'si')
n4 = 'Lamborghini'
set_brand(brand_class, n4, 'si')


#Inserimento dei colori
@db_session()
def set_colors(Colore, name, vis):
   Colore(
       nome = name,
       visibility = vis
   )

n1 = 'Giallo Modena' #solo Ferrari
set_colors(colore_class, n1, 'si')
n2 = 'Rosso Imola' #solo Ferrari
set_colors(colore_class, n2, 'si')
n3 = 'Nero'
set_colors(colore_class, n3, 'si')
n4 = 'Grigio'
set_colors(colore_class, n4, 'si')
n5 = 'Bianco'
set_colors(colore_class, n5, 'si')
n6 = 'Verde'
set_colors(colore_class, n6, 'si')
n7 = 'Giallo'
set_colors(colore_class, n7, 'si')
n8 = 'Rosso'
set_colors(colore_class, n8, 'si')

# Inserimento dei modelli
@db_session()
def set_modelli(Modello, nome, brand, altezza, lunghezza, larghezza, peso, bagagliaio, prezzo_base, descrizione, vis):
   Modello(
       nome = nome,
       brand = brand,
       altezza = altezza,
       lunghezza = lunghezza,
       larghezza = larghezza,
       peso = peso,
       bagagliaio = bagagliaio,
       prezzo_base = prezzo_base,
       descrizione = descrizione,
       visibility = vis
   )

d1 = 'La Ferrari Purosangue è la prima vettura a quattro porte e quattro sedili della Casa di Maranello, ma le auto con due posti posteriori hanno avuto un ruolo di rilievo nella strategia aziendale fin dai primi giorni: molte sono state infatti le Ferrari che hanno fatto dell’unione tra prestazioni assolute e comfort di primordine uno dei loro pilastri.'
set_modelli(modello_class, 'Purosangue', 'Ferrari', 1589, 4973, 2028, 2245, 473, 385.730, d1, 'si')

d2 = 'La Panamera è pensata per coloro che vogliono sentirsi liberi di seguire il proprio istinto. Che esprimono liberamente se stessi. Che prendono decisioni in base a ciò che vogliono fare e non a ciò che pensano gli altri. Abbiamo costruito questa vettura sportiva proprio per queste persone.'
set_modelli(modello_class, 'Panamera', 'Porsche', 1423, 5052, 1937, 1960, 494, 112.182, d2, 'si')

# Inserimento dei motori
@db_session()
def set_motori(Motore, codice, alimentazione, vis):
    Motore(
        codice = codice,
        alimentazione = alimentazione,
        visibility = vis
    )

set_motori(motore_class, 'm001', 'Benzina', 'si')
set_motori(motore_class, 'm002', 'Ibrido', 'si')

# Inserimento degli optional
@db_session()
def set_optional(Optional, nome, vis):
    Optional(
        nome = nome,
        visibility = vis
    )

set_optional(optional_class, 'Sedili in pelle', 'si')
set_optional(optional_class, 'Tetto panoramico', 'si')

# Inserimento degli sconti
@db_session()
def set_sconti(Optional, codice, dal, al, percentuale):
    Optional(
        codice = codice,
        dal = dal,
        al = al,
        percentuale = percentuale
    )

set_sconti(sconto_class, 'BF2024', datetime.date(2024, 11, 10), datetime.date(2024, 11, 28), 30)
set_sconti(sconto_class, 'REDp', datetime.date(2024, 10, 10), datetime.date(2024, 11, 1), 15)

# Inserimento dei clienti
@db_session()
def set_cliente(Cliente, nome, cognome, email, pw):
   Cliente(
       name = nome,
       surname = cognome,
       email = email,
       pw = pw
   )

set_cliente(cliente_class, 'Michael','Ferrari', 'm.ferrari@gmail.com','Shiumi2000')
set_cliente(cliente_class, 'Valentina','Grandi', 'vale46@gmail.com','i234s')
set_cliente(cliente_class, 'Rebecca','Cavour', 'cav.reb@gmail.com','cors0123')
set_cliente(cliente_class, 'Alessandro','Tristo', 'ssandro@gmail.com','trist3iso')

# Inserimento delle immagini
@db_session()
def set_immagini(Immagine, cod, url, colore, modello):
   Immagine(
       codice = cod,
       codiceURL = url,
       colore = colore,
       modello = modello
   )

#Ferrari Purosangue
set_immagini(immagine_class, 'fpgr001', 'https://www.google.com/url?sa=i&url=https%3A%2F%2Fit.motor1.com%2Fnews%2F609754%2Fferrari-purosangue-caratteristiche-motore-prezzo%2F&psig=AOvVaw0MVxGBd2dL8SsUsRoaPwhr&ust=1716908773095000&source=images&cd=vfe&opi=89978449&ved=0CBIQjRxqFwoTCMC3vN-NroYDFQAAAAAdAAAAABAJ','Grigio', 'Purosangue')
set_immagini(immagine_class, 'fpgr002', 'https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.ferrari.com%2Fit-IT%2Fauto%2Fferrari-purosangue&psig=AOvVaw0MVxGBd2dL8SsUsRoaPwhr&ust=1716908773095000&source=images&cd=vfe&opi=89978449&ved=0CBIQjRxqFwoTCMC3vN-NroYDFQAAAAAdAAAAABAW','Grigio', 'Purosangue')
set_immagini(immagine_class, 'fpgr003', 'https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.ferrari.com%2Fit-IT%2Fauto%2Fferrari-purosangue&psig=AOvVaw0MVxGBd2dL8SsUsRoaPwhr&ust=1716908773095000&source=images&cd=vfe&opi=89978449&ved=0CBIQjRxqFwoTCMC3vN-NroYDFQAAAAAdAAAAABBN','Grigio', 'Purosangue')
set_immagini(immagine_class, 'fpgr004', 'https://www.google.com/url?sa=i&url=https%3A%2F%2Femerald-estate.com%2F%3Fs%3Dferrari-officially-reveals-the-purosangue-suv-hypebeast-ss-e9BXynTE&psig=AOvVaw0MVxGBd2dL8SsUsRoaPwhr&ust=1716908773095000&source=images&cd=vfe&opi=89978449&ved=0CBIQjRxqFwoTCMC3vN-NroYDFQAAAAAdAAAAABAx','Grigio', 'Purosangue')

set_immagini(immagine_class, 'fpgm001', 'https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.motorbox.com%2Fauto%2Fmagazine%2Fauto-novita%2Fferrari-purosangue-configuratore-online-colori-cerchi-interni&psig=AOvVaw2ulkFhCAp1WJgfvcvxQWHX&ust=1716909285585000&source=images&cd=vfe&opi=89978449&ved=0CBIQjRxqFwoTCOjrztWProYDFQAAAAAdAAAAABAQ','Giallo Modena', 'Purosangue')
set_immagini(immagine_class, 'fpgm002', 'https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.autoevolution.com%2Fnews%2Fhere-s-our-2023-ferrari-purosangue-you-can-build-one-too-198577.html&psig=AOvVaw2ulkFhCAp1WJgfvcvxQWHX&ust=1716909285585000&source=images&cd=vfe&opi=89978449&ved=0CBIQjRxqFwoTCOjrztWProYDFQAAAAAdAAAAABAX','Giallo Modena', 'Purosangue')
set_immagini(immagine_class, 'fpgm003', 'https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.autoevolution.com%2Fnews%2Fhere-s-our-2023-ferrari-purosangue-you-can-build-one-too-198577.html&psig=AOvVaw2ulkFhCAp1WJgfvcvxQWHX&ust=1716909285585000&source=images&cd=vfe&opi=89978449&ved=0CBIQjRxqFwoTCOjrztWProYDFQAAAAAdAAAAABAe','Giallo Modena', 'Purosangue')
set_immagini(immagine_class, 'fpgm004', 'https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.autoevolution.com%2Fnews%2Fhere-s-our-2023-ferrari-purosangue-you-can-build-one-too-198577.html&psig=AOvVaw2ulkFhCAp1WJgfvcvxQWHX&ust=1716909285585000&source=images&cd=vfe&opi=89978449&ved=0CBIQjRxqFwoTCOjrztWProYDFQAAAAAdAAAAABAl','Giallo Modena', 'Purosangue')

#Porsche Panamera
set_immagini(immagine_class, 'ppn001', 'https://pictures.porsche.com/rtt/iris?COSY-EU-100-1711coMvsi60AAt5FwcmBEgA4qP8iBUDxPE3Cb9pNXkBuNYdMGF4tl3U0%25z8rMHIspMBvMZq6G5OtgSv31nBJaA4qh4NSEGkaW%25cz91wxuzbUUdMGLqk0DtWoQDcFGH6zYnfurKT95yPewFJRCvNzxuWFGXoq1quyr6FObOhswRuT06sqx7e2HfWQDcFG6huWXsOw30eV6iTaXBzhRc2GapqA7fQrzcOJUPYwUnTBsN5ozG2dioCyWlQD9AzXCKuAIKyHNTwMzt5FTmnEBc6XdG6', 'Nero', 'Panamera')
set_immagini(immagine_class, 'ppn002', 'https://pictures.porsche.com/rtt/iris?COSY-EU-100-1711coMvsi60AAt5FwcmBEgA4qP8iBUDxPE3Cb9pNXkBuNYdMGF4tl3U0%25z8rMH1spMBvMZq6G5OtgSv31nBJaA4qh4NSEGkaW%25cz91wxuzbUUdMGLqk0DtWoQDcFGH6zYnfurKT95yPewFJRCvNzxuWFGXoq1quyr6FObOhswRuT06sqx7e2HfWQDcFG6huWXsOw30eV6iTaXBzhRc2GapqA7fQrzcOJUPYwUnTBsN5ozG2dioCyWlQD9AzXCKuAIKyHNTwMzt5FTmnEBc6XdG6', 'Nero', 'Panamera')
set_immagini(immagine_class, 'ppn003', 'https://pictures.porsche.com/rtt/iris?COSY-EU-100-1711coMvsi60AAt5FwcmBEgA4qP8iBUDxPE3Cb9pNXkBuNYdMGF4tl3U0%25z8rMbjAuWgRcgVGPK0rh4mctLsR6EXdGvdTmJKlEnDzCBLMkYCIFF7gKpGl3Uhn21UzQKjPCbsqYSawB0iO5MQ6NHcTCkYnQKf2GLGYiSPQrIrvuMNYw3PuGko5xjqn1UzQKPvYnfurMt35yPewEfRCvNzxKEWGXoq1SCzr6FObMFswRuT02CKx7e2Hin%251UBXCfHaYXZaijTwMgCh0Qw9sJRzPf7KP', 'Nero', 'Panamera')
set_immagini(immagine_class, 'ppn004', 'https://pictures.porsche.com/rtt/iris?COSY-EU-100-1711coMvsi60AAt5FwcmBEgA4qP8iBUDxPE3LUUEssTugNTb7gKOCl3UBb%25cUzW1TipaIKyGZPm21rmv31%25J1jNdTqoaLxJK5h%254M9pNEpUxgTbMtZ6Pl5QYcPCyyW1T0NbGVGBfeV6iTdjctBvo%25mXj4AUPrb6a0LDpUuBLTugFhvczDx7Jv5mb3%25ZpjsZuWgFXnJPeP3IrS', 'Nero', 'Panamera')

set_immagini(immagine_class, 'ppb001', 'https://pictures.porsche.com/rtt/iris?COSY-EU-100-1711coMvsi60AAt5FwcmBEgA4qP8iBUDxPE3Cb9pNXkBuNYdMGF4tl3U0%25z8rMHIspMBvMZq6G5OtgSv31nBJaA4qh4NSEGkaW%25cz91wxuzbUUdMGLqk0DxIF%25vUqjZUuWXsOGBfeV6iTrogzhRc2s9dqA7fQiZsOJUPYPihTBsN5N8y2dioCByPQDcFG6huWXsOw30eV6iTaXBzhRc2GapqA7fQrzcOJUPYwUnTBsN5ozG2dioCyWlQD9AzXCKuAIKyHNTwMzt5FTmnEBc6XdG6', 'Bianco', 'Panamera')
set_immagini(immagine_class, 'ppb002', 'https://pictures.porsche.com/rtt/iris?COSY-EU-100-1711coMvsi60AAt5FwcmBEgA4qP8iBUDxPE3Cb9pNXkBuNYdMGF4tl3U0%25z8rMH1spMBvMZq6G5OtgSv31nBJaA4qh4NSEGkaW%25cz91wxuzbUUdMGLqk0DxIF%25vUqjZUuWXsOGBfeV6iTrogzhRc2s9dqA7fQiZsOJUPYPihTBsN5N8y2dioCByPQDcFG6huWXsOw30eV6iTaXBzhRc2GapqA7fQrzcOJUPYwUnTBsN5ozG2dioCyWlQD9AzXCKuAIKyHNTwMzt5FTmnEBc6XdG6', 'Bianco', 'Panamera')
set_immagini(immagine_class, 'ppb003', 'https://pictures.porsche.com/rtt/iris?COSY-EU-100-1711coMvsi60AAt5FwcmBEgA4qP8iBUDxPE3Cb9pNXkBuNYdMGF4tl3U0%25z8rMbjAuWgRcgVGPK0rh4mctLsR6EXdGvdTmJKlEnDzCBLMkYCIFF7gKpGl3UkZQDcFG8VFYnfurKRq5yPewS24CvNzxuB7GXoq1eVur6FObOevwRuT0TAix7e2HRiO1UzQKPvYnfurMt35yPewEfRCvNzxKEWGXoq1SCzr6FObMFswRuT02CKx7e2Hin%251UBXCfHaYXZaijTwMgCh0Qw9sJRzPf7KP', 'Bianco', 'Panamera')
set_immagini(immagine_class, 'ppb004', 'https://pictures.porsche.com/rtt/iris?COSY-EU-100-1711coMvsi60AAt5FwcmBEgA4qP8iBUDxPE3Cb9pNXkBuNYdMGF4tl3U0%25z8rMH8spMBvMZq6G5OtgSv31nBJaA4qh4NSEGkaW%25cz91wxuzbUUdMGLqk0DxIF%25vUqjZUuWXsOGBfeV6iTrogzhRc2s9dqA7fQiZsOJUPYPihTBsN5N8y2dioCByPQDcFG6huWXsOw30eV6iTaXBzhRc2GapqA7fQrzcOJUPYwUnTBsN5ozG2dioCyWlQD9AzXCKuAIKyHNTwMzt5FTmnEBc6XdG6', 'Bianco', 'Panamera')

# Inserimento delle auto usate
@db_session()
def set_autoUsata(AutoUsata, targa, modello, proprietario, valutatore):
   AutoUsata(
       targa = targa, 
       modello = modello, 
       proprietario = proprietario, 
       valutatore = valutatore
   )

set_autoUsata(autoUsata_class, 'AA123BB', 'Fiat 500', 'vale46@gmail.com', 'i002')
set_autoUsata(autoUsata_class, 'AB987BA', 'Mercedes Classe C', 'cav.reb@gmail.com', 'i003')

# Inserimento colore modello
@db_session()
def set_coloremodello(ColoreModello, id, colore, modello, prezzo):
   ColoreModello(
       id = id, 
       colore = colore, 
       modello = modello, 
       prezzo = prezzo
   )

set_coloremodello(coloreModello_class, 'fpgr', 'Grigio', 'Purosangue', '1000')
set_coloremodello(coloreModello_class, 'fpgm', 'Giallo Modena', 'Purosangue', '3000')
set_coloremodello(coloreModello_class, 'ppn', 'Nero', 'Panamera', '1000')
set_coloremodello(coloreModello_class, 'ppb', 'Bianco', 'Panamera', '1000')

# Inserimento motore modello
@db_session()
def set_motoremodello(MotoreModello, id, motore, modello, prezzo):
   MotoreModello(
       id = id, 
       motore = motore, 
       modello = modello, 
       prezzo = prezzo
   )

set_motoremodello(motoreModello_class, 'fpb', 'm001', 'Purosangue', '1000')
set_motoremodello(motoreModello_class, 'ppb', 'm001', 'Panamera', '500')
set_motoremodello(motoreModello_class, 'ppn', 'm002', 'Panamera', '500')

# Inserimento optional modello
@db_session()
def set_optionalmodello(OptionalModello, id, optional, modello, prezzo):
   OptionalModello(
       id = id, 
       optional = optional, 
       modello = modello, 
       prezzo = prezzo
   )

set_optionalmodello(optionalModello_class, 'fp001', 'Sedili in pelle', 'Purosangue', '1500')
set_optionalmodello(optionalModello_class, 'pp001', 'Sedili in pelle', 'Panamera', '1500')
set_optionalmodello(optionalModello_class, 'pp002', 'Tetto panoramico', 'Panamera', '1000')

# Inserimento delle auto
@db_session()
def set_auto(Auto, codice, prezzo_totale, cliente, modello, colore, motore):
   Auto(
       codice = codice,
       prezzo_totale = prezzo_totale,
       cliente = cliente,
       modello = modello,
       colore = colore,
       motore = motore
   )

set_auto(auto_class, 'a001', 500000, 'vale46@gmail.com', 'Purosangue', 'Grigio', 'm001')
set_auto(auto_class, 'a002', 500200, 'm.ferrari@gmail.com', 'Purosangue', 'Giallo Modena', 'm001')
set_auto(auto_class, 'a003', 250000, 'cav.reb@gmail.com', 'Panamera', 'Nero', 'm001')
set_auto(auto_class, 'a004', 250000, 'ssandro@gmail.com', 'Panamera', 'Bianco', 'm002')

# Inserimento dei preventivi
@db_session()
def set_preventivo(Preventivo, codice, data, auto, cliente, sconto_mese, valore_sconto, auto_rottamata, valore_sconto_rottamazione, prezzo):
   Preventivo(
       codice = codice,
       data = data,
       auto = auto,
       cliente = cliente,
       sconto_mese = sconto_mese,
       valore_sconto = valore_sconto,
       auto_rottamata = auto_rottamata,
       valore_sconto_rottamazione = valore_sconto_rottamazione,
       prezzo = prezzo
   )
calcPrezzo = 250000 + 1000 + 1500 + 1500
set_preventivo(preventivo_class, 'prev001', datetime.date(2024, 10, 10), 'a001', 'vale46@gmail.com','BF2024', 2500.50, 'AA123BB',2000, calcPrezzo)

# Inserimento degli ordini
@db_session()
def set_ordini(Ordine, codice, data_ordine, data_consegna, preventivo, sede_ritiro, gestore_ordine):
   Ordine(
       codice = codice,
       data_ordine = data_ordine,
       data_consegna = data_consegna,
       preventivo = preventivo,
       sede_ritiro = sede_ritiro,
       gestore_ordine = gestore_ordine
   )

calcConsegna = datetime.date(2024, 11, 28)
set_ordini(ordine_class, 'ord001', datetime.date(2024, 11, 10), calcConsegna, 'prev001', 'Heaven Motors Verona', 'i001')

# Inserimento scelta optional
@db_session()
def set_sceltaoptional(SceltaOptional, auto, nome):
   SceltaOptional(
       auto = auto,
       optional = nome
   )

set_sceltaoptional(sceltaOptional_class, 'a001', 'Sedili in pelle')
set_sceltaoptional(sceltaOptional_class, 'a003', 'Tetto panoramico')
set_sceltaoptional(sceltaOptional_class, 'a003', 'Sedili in pelle')

# Inserimento sconti modello
@db_session()
def set_scontomodello(ScontoModello, id, sconto, modello):
   ScontoModello(
       id = id, 
       sconto = sconto, 
       modello = modello
   )

set_scontomodello(scontoModello_class, 'fp001', 'BF2024', 'Purosangue')
set_scontomodello(scontoModello_class, 'fp002', 'REDp', 'Purosangue')
set_scontomodello(scontoModello_class, 'pp001', 'BF2024', 'Panamera')