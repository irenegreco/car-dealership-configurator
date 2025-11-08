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

set_brand(brand_class, 'Ferrari', 'si')
set_brand(brand_class, 'Mercedes', 'si')
set_brand(brand_class, 'Porsche', 'si')

#Inserimento dei colori
@db_session()
def set_colors(Colore, name, vis):
   Colore(
       nome = name,
       visibility = vis
   )

set_colors(colore_class, 'Giallo Modena', 'si') #solo Ferrari
set_colors(colore_class, 'Rosso Imola', 'si') #solo Ferrari
set_colors(colore_class, 'Nero', 'si')
set_colors(colore_class, 'Bianco', 'si')
set_colors(colore_class, 'Blu', 'si')
set_colors(colore_class, 'Grigio', 'si')

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

d = 'La Ferrari Purosangue è la prima vettura a quattro porte e quattro sedili della Casa di Maranello, ma le auto con due posti posteriori hanno avuto un ruolo di rilievo nella strategia aziendale fin dai primi giorni: molte sono state infatti le Ferrari che hanno fatto dell’unione tra prestazioni assolute e comfort di primordine uno dei loro pilastri.'
set_modelli(modello_class, 'Purosangue', 'Ferrari', 1589, 4973, 2028, 2245, 473, 385730, d, 'si')

d = 'La Ferrari Roma, nuova coupé 2+ a motore centrale-anteriore della Casa di Maranello, è caratterizzata da un design senza tempo, da una spiccata raffinatezza e da guidabilità e prestazioni di assoluta eccellenza. Grazie al suo stile inconfondibile, la vettura reinterpreta in chiave contemporanea il lifestyle della città di Roma tipico degli anni ‘50-‘60, caratterizzato dalla leggerezza e dal piacere di vivere.'
set_modelli(modello_class, 'Roma', 'Ferrari', 1302, 4656, 1974, 1655, 272, 207001, d, 'si')

d = 'Il nome stesso raccoglie il vero significato di quanto è stato ottenuto a livello di prestazioni - il richiamo alla vettura di Formula 1 sottolinea lo stretto legame che è sempre esistito tra il mondo delle corse e le vetture stradali. La SF90 Stradale, espressione più avanzata della tecnologia sviluppata a Maranello, è la dimostrazione di come le conoscenze acquisite attraverso le competizioni hanno trovato immediata applicazione su di una vettura Ferrari di produzione.'
set_modelli(modello_class, 'SF90 Stradale', 'Ferrari', 1186, 4710, 1972, 1850, 74, 427930, d, 'si')

d = 'La Panamera è pensata per coloro che vogliono sentirsi liberi di seguire il proprio istinto. Che esprimono liberamente se stessi. Che prendono decisioni in base a ciò che vogliono fare e non a ciò che pensano gli altri. Abbiamo costruito questa vettura sportiva proprio per queste persone.'
set_modelli(modello_class, 'Panamera', 'Porsche', 1423, 5052, 1937, 1960, 494, 112182, d, 'si')

d = 'Chi sogna una Porsche, di solito ha in mente questo modello: da 60 anni la 911 è la quintessenza di una vettura sportiva emozionante e potente, adatta ad un uso quotidiano. Siediti al volante della nuova 911 ed entra a far parte di una community unica.'
set_modelli(modello_class, '911', 'Porsche', 1298, 4519, 1852, 1580, 396, 127420, d, 'si')

d = 'Oltre 20 anni fa ci siamo chiesti se una vettura sportiva potesse essere qualcosa di più che l\'espressione dell  \'individualità. La risposta è stata la Cayenne. Una vettura che non ha cessato di evolversi. Per coloro che vogliono raggiungere luoghi incontaminati. Oggi per andare in ufficio, domani per guidare fuoristrada o su circuito: la Cayenne offre piacere di guida su qualsiasi terreno, combinato con il design tipico di Porsche. '
set_modelli(modello_class, 'Cayenne', 'Porsche', 1698, 4930, 1983, 2245, 772, 103582, d, 'si')

d = 'Mercedes-Benz GLC Coupé stupisce per lo stile unico, coniugando l\'iconico design Mercedes-Benz coupé con le linee decise e sportive di un SUV. Le caratteristiche distintive si rivelano in alcuni dettagli specifici ed è perfetta su qualsiasi tipologia di terreno.'
set_modelli(modello_class, 'GLC Coupè', 'Mercedes', 1603, 4792, 2076, 2860, 390, 70922, d, 'si')

d = 'Avventura ed eleganza si incontrano negli interni di Classe G, dove il DNA da fuoristrada e la tecnologia più all’avanguardia si fondono per un\'esperienza senza eguali. Qui, ogni dettaglio, dall\'MBUX al COCKPIT OFFROAD, è stato progettato per superare ogni aspettativa e per riconfermare Classe G come uno dei migliori fuoristrada al mondo , anche nella versione Full Electric.'
set_modelli(modello_class, 'Classe G', 'Mercedes', 1976, 4873, 2187, 3200, 640, 138409, d, 'si')

d = 'L’affascinante design di Nuova Mercedes-AMG GT combina linee sensuali con proporzioni da auto sportiva, nello stile tipico del marchio. SO AMG: sviluppata interamente da AMG, l\'auto dimostra la nostra passione per le prestazioni eccezionali e la guida sportiva.'
set_modelli(modello_class, 'AMG GT Coupé', 'Mercedes', 1455, 5054, 1953, 2380, 456, 114290, d, 'si')

# Inserimento dei motori
@db_session()
def set_motori(Motore, codice, alimentazione, vis):
    Motore(
        codice = codice,
        alimentazione = alimentazione,
        visibility = vis
    )

set_motori(motore_class, 'mb001', 'Benzina 1999', 'si') 
set_motori(motore_class, 'mb002', 'Benzina 3982', 'si') 
set_motori(motore_class, 'mb003', 'Benzina 3996', 'si') 
set_motori(motore_class, 'mi001', 'Ibrido 2894', 'si') 
set_motori(motore_class, 'mi002', 'Ibrido 3996', 'si') 
set_motori(motore_class, 'me001', 'Elettrico 3996', 'si') 
set_motori(motore_class, 'me002', 'Elettrico 2995', 'si') 
set_motori(motore_class, 'mpi001', 'Ibrido Plug-In 1999', 'si')
set_motori(motore_class, 'mpi002', 'Ibrido Plug-In 2894', 'si')
set_motori(motore_class, 'mpi003', 'Ibrido Plug-In 3996', 'si')

# Inserimento degli optional
@db_session()
def set_optional(Optional, nome, vis):
    Optional(
        nome = nome,
        visibility = vis
    )

set_optional(optional_class, 'Sedili in pelle', 'si')
set_optional(optional_class, 'Tetto panoramico', 'si')
set_optional(optional_class, 'Vetri Oscurati', 'si')
set_optional(optional_class, 'Cerchi diametro 21 pollici in carbonio', 'si')


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
set_sconti(sconto_class, 'SESSIONE', datetime.date(2024, 6, 1), datetime.date(2024, 7, 31), 20)

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
def set_immagini(Immagine, cod, url, colore, modello, vis):
   Immagine(
       codice = cod,
       codiceURL = url,
       colore = colore,
       modello = modello,
       visibility = vis
   )

#Ferrari Purosangue
set_immagini(immagine_class, 'fpgr001', 'https://immagini.alvolante.it/sites/default/files/styles/image_gallery_big/public/news_galleria/2022/09/ferrari-purosangue-2022-09_02.jpg?itok=H-LLVcEh','Grigio', 'Purosangue', 'si')
set_immagini(immagine_class, 'fpgr002', 'https://immagini.alvolante.it/sites/default/files/styles/image_gallery_big/public/news_galleria/2022/09/ferrari-purosangue-2022-09_01.jpg?itok=bScNp_O2','Grigio', 'Purosangue', 'si')
set_immagini(immagine_class, 'fpgr003', 'https://ocdn.eu/pulscms-transforms/1/BR2ktkpTURBXy9hYmQ2NmM4Nzg0YTNlM2ZhNDYwMzVmZDM1NDQ2NDQ3MS5qcGeSlQMAzQI7zQ3XzQfJkwXNBLDNAnY','Grigio', 'Purosangue', 'si')
set_immagini(immagine_class, 'fpgr004', 'https://dimages2.gazzettaobjects.it/files/image_768_434/files/fp/uploads/2022/09/12/631f8401ccc7e.r_d.1077-896-3750.jpeg','Grigio', 'Purosangue', 'si')

set_immagini(immagine_class, 'fpgm001', 'https://media.motorbox.com/image/ferrari-purosangue-configuratore-online-colori-cerchi-interni/7/6/8/768044/768044-16x9-lg.jpg','Giallo Modena', 'Purosangue', 'si')
set_immagini(immagine_class, 'fpgm002', 'https://s1.cdn.autoevolution.com/images/news/gallery/here-s-our-2023-ferrari-purosangue-you-can-build-one-too_8.jpg','Giallo Modena', 'Purosangue', 'si')
set_immagini(immagine_class, 'fpgm003', 'https://s1.cdn.autoevolution.com/images/news/gallery/here-s-our-2023-ferrari-purosangue-you-can-build-one-too_5.jpg','Giallo Modena', 'Purosangue', 'si')
set_immagini(immagine_class, 'fpgm004', 'https://s1.cdn.autoevolution.com/images/news/gallery/here-s-our-2023-ferrari-purosangue-you-can-build-one-too_4.jpg','Giallo Modena', 'Purosangue', 'si')

#Ferrari SF90 Stradale
set_immagini(immagine_class, 'fsf90ri001' , 'https://www.infomotori.com/content/uploads/2021/03/ferrari-sf90-stradale-imola-leclerc-sainz-14-728x415.jpg', 'Rosso Imola', 'SF90 Stradale', 'si')
set_immagini(immagine_class, 'fsf90ri002' , 'https://www.infomotori.com/content/uploads/2021/03/ferrari-sf90-stradale-imola-leclerc-sainz-4-728x415.jpg', 'Rosso Imola', 'SF90 Stradale', 'si')
set_immagini(immagine_class, 'fsf90ri003' , 'https://www.infomotori.com/content/uploads/2021/03/ferrari-sf90-stradale-imola-leclerc-sainz-15-973x544.jpg', 'Rosso Imola', 'SF90 Stradale', 'si')
set_immagini(immagine_class, 'fsf90ri004' , 'https://www.infomotori.com/content/uploads/2021/03/ferrari-sf90-stradale-imola-leclerc-sainz-16-973x544.jpg', 'Rosso Imola', 'SF90 Stradale', 'si')

set_immagini(immagine_class, 'fsf90n001', 'https://www.motoridilusso.com/wp-content/uploads/2021/07/ferrari-sf90-stradale-by-novitec-1.jpg', 'Nero', 'SF90 Stradale', 'si')
set_immagini(immagine_class, 'fsf90n002', 'https://f7432d8eadcf865aa9d9-9c672a3a4ecaaacdf2fee3b3e6fd2716.ssl.cf3.rackcdn.com/C395/U4889/IMG_51330-medium.jpg', 'Nero', 'SF90 Stradale', 'si')
set_immagini(immagine_class, 'fsf90n003', 'https://f7432d8eadcf865aa9d9-9c672a3a4ecaaacdf2fee3b3e6fd2716.ssl.cf3.rackcdn.com/C395/U4889/IMG_51282-medium.jpg', 'Nero', 'SF90 Stradale', 'si')
set_immagini(immagine_class, 'fsf90n004', 'https://cdn-images.motor.es/image/m/1320w.webp/fotos-noticias/2021/07/ferrari-sf90-novitec-202179772-1626810302_7.jpg', 'Nero', 'SF90 Stradale', 'si')

#Ferrari Roma
set_immagini(immagine_class, 'frg001', 'https://cdn.dicklovett.co.uk/uploads/used_stock_image/1_1577586_e.jpg?v=1715960407', 'Grigio', 'Roma', 'si')
set_immagini(immagine_class, 'frg002', 'https://cdn.dicklovett.co.uk/uploads/used_stock_image/1_1577588_e.jpg?v=1715960411', 'Grigio', 'Roma', 'si')
set_immagini(immagine_class, 'frg003', 'https://cdn.dicklovett.co.uk/uploads/used_stock_image/1_1577609_e.jpg?v=1715960433', 'Grigio', 'Roma', 'si')
set_immagini(immagine_class, 'frg004', 'https://cdn.dicklovett.co.uk/uploads/used_stock_image/1_1577600_e.jpg?v=1715960425', 'Grigio', 'Roma', 'si')

set_immagini(immagine_class, 'frbi001', 'https://tailormade.ferrari.com/static/media/20220406124719/Esterni_small_272612_015.jpg', 'Bianco', 'Roma', 'si')
set_immagini(immagine_class, 'frbi002', 'https://tailormade.ferrari.com/static/media/20220406124717/Esterni_small_272612_014.jpg', 'Bianco', 'Roma', 'si')
set_immagini(immagine_class, 'frbi003', 'https://tailormade.ferrari.com/static/media/20220406124723/Esterni_small_272612_023.jpg', 'Bianco', 'Roma', 'si')
set_immagini(immagine_class, 'frbi004', 'https://tailormade.ferrari.com/static/media/20220406124721/Esterni_small_272612_018.jpg', 'Bianco', 'Roma', 'si')

#Porsche Panamera
set_immagini(immagine_class, 'ppn001', 'https://pictures.porsche.com/rtt/iris?COSY-EU-100-1711coMvsi60AAt5FwcmBEgA4qP8iBUDxPE3Cb9pNXkBuNYdMGF4tl3U0%25z8rMHIspMBvMZq6G5OtgSv31nBJaA4qh4NSEGkaW%25cz91wxuzbUUdMGLqk0DtWoQDcFGH6zYnfurKT95yPewFJRCvNzxuWFGXoq1quyr6FObOhswRuT06sqx7e2HfWQDcFG6huWXsOw30eV6iTaXBzhRc2GapqA7fQrzcOJUPYwUnTBsN5ozG2dioCyWlQD9AzXCKuAIKyHNTwMzt5FTmnEBc6XdG6', 'Nero', 'Panamera', 'si')
set_immagini(immagine_class, 'ppn002', 'https://pictures.porsche.com/rtt/iris?COSY-EU-100-1711coMvsi60AAt5FwcmBEgA4qP8iBUDxPE3Cb9pNXkBuNYdMGF4tl3U0%25z8rMH1spMBvMZq6G5OtgSv31nBJaA4qh4NSEGkaW%25cz91wxuzbUUdMGLqk0DtWoQDcFGH6zYnfurKT95yPewFJRCvNzxuWFGXoq1quyr6FObOhswRuT06sqx7e2HfWQDcFG6huWXsOw30eV6iTaXBzhRc2GapqA7fQrzcOJUPYwUnTBsN5ozG2dioCyWlQD9AzXCKuAIKyHNTwMzt5FTmnEBc6XdG6', 'Nero', 'Panamera', 'si')
set_immagini(immagine_class, 'ppn003', 'https://pictures.porsche.com/rtt/iris?COSY-EU-100-1711coMvsi60AAt5FwcmBEgA4qP8iBUDxPE3Cb9pNXkBuNYdMGF4tl3U0%25z8rMbjAuWgRcgVGPK0rh4mctLsR6EXdGvdTmJKlEnDzCBLMkYCIFF7gKpGl3Uhn21UzQKjPCbsqYSawB0iO5MQ6NHcTCkYnQKf2GLGYiSPQrIrvuMNYw3PuGko5xjqn1UzQKPvYnfurMt35yPewEfRCvNzxKEWGXoq1SCzr6FObMFswRuT02CKx7e2Hin%251UBXCfHaYXZaijTwMgCh0Qw9sJRzPf7KP', 'Nero', 'Panamera', 'si')
set_immagini(immagine_class, 'ppn004', 'https://pictures.porsche.com/rtt/iris?COSY-EU-100-1711coMvsi60AAt5FwcmBEgA4qP8iBUDxPE3LUUEssTugNTb7gKOCl3UBb%25cUzW1TipaIKyGZPm21rmv31%25J1jNdTqoaLxJK5h%254M9pNEpUxgTbMtZ6Pl5QYcPCyyW1T0NbGVGBfeV6iTdjctBvo%25mXj4AUPrb6a0LDpUuBLTugFhvczDx7Jv5mb3%25ZpjsZuWgFXnJPeP3IrS', 'Nero', 'Panamera', 'si')

set_immagini(immagine_class, 'ppbi001', 'https://pictures.porsche.com/rtt/iris?COSY-EU-100-1711coMvsi60AAt5FwcmBEgA4qP8iBUDxPE3Cb9pNXkBuNYdMGF4tl3U0%25z8rMHIspMBvMZq6G5OtgSv31nBJaA4qh4NSEGkaW%25cz91wxuzbUUdMGLqk0DxIF%25vUqjZUuWXsOGBfeV6iTrogzhRc2s9dqA7fQiZsOJUPYPihTBsN5N8y2dioCByPQDcFG6huWXsOw30eV6iTaXBzhRc2GapqA7fQrzcOJUPYwUnTBsN5ozG2dioCyWlQD9AzXCKuAIKyHNTwMzt5FTmnEBc6XdG6', 'Bianco', 'Panamera', 'si')
set_immagini(immagine_class, 'ppbi002', 'https://pictures.porsche.com/rtt/iris?COSY-EU-100-1711coMvsi60AAt5FwcmBEgA4qP8iBUDxPE3Cb9pNXkBuNYdMGF4tl3U0%25z8rMH1spMBvMZq6G5OtgSv31nBJaA4qh4NSEGkaW%25cz91wxuzbUUdMGLqk0DxIF%25vUqjZUuWXsOGBfeV6iTrogzhRc2s9dqA7fQiZsOJUPYPihTBsN5N8y2dioCByPQDcFG6huWXsOw30eV6iTaXBzhRc2GapqA7fQrzcOJUPYwUnTBsN5ozG2dioCyWlQD9AzXCKuAIKyHNTwMzt5FTmnEBc6XdG6', 'Bianco', 'Panamera', 'si')
set_immagini(immagine_class, 'ppbi003', 'https://pictures.porsche.com/rtt/iris?COSY-EU-100-1711coMvsi60AAt5FwcmBEgA4qP8iBUDxPE3Cb9pNXkBuNYdMGF4tl3U0%25z8rMbjAuWgRcgVGPK0rh4mctLsR6EXdGvdTmJKlEnDzCBLMkYCIFF7gKpGl3UkZQDcFG8VFYnfurKRq5yPewS24CvNzxuB7GXoq1eVur6FObOevwRuT0TAix7e2HRiO1UzQKPvYnfurMt35yPewEfRCvNzxKEWGXoq1SCzr6FObMFswRuT02CKx7e2Hin%251UBXCfHaYXZaijTwMgCh0Qw9sJRzPf7KP', 'Bianco', 'Panamera', 'si')
set_immagini(immagine_class, 'ppbi004', 'https://pictures.porsche.com/rtt/iris?COSY-EU-100-1711coMvsi60AAt5FwcmBEgA4qP8iBUDxPE3Cb9pNXkBuNYdMGF4tl3U0%25z8rMH8spMBvMZq6G5OtgSv31nBJaA4qh4NSEGkaW%25cz91wxuzbUUdMGLqk0DxIF%25vUqjZUuWXsOGBfeV6iTrogzhRc2s9dqA7fQiZsOJUPYPihTBsN5N8y2dioCByPQDcFG6huWXsOw30eV6iTaXBzhRc2GapqA7fQrzcOJUPYwUnTBsN5ozG2dioCyWlQD9AzXCKuAIKyHNTwMzt5FTmnEBc6XdG6', 'Bianco', 'Panamera', 'si')

#Porsche 911
set_immagini(immagine_class, 'p911bl001', 'https://pictures.porsche.com/rtt/iris?COSY-EU-100-1711coMvsi60AAt5FwcmBEgA4qP8iBUDxPE3Cb9pNXkBuNYdMGF4tl3U0%25z8rMHIspMBvMZq6G5OtgSv31nBJaA4qh4NSEGkaW%25cz91wxuzbUUdMGLqk0DLfF%25vUqj7AuWXsOGBTeV6iTi7%25zhRc2VBsqA7fQnSPED6u5MwN9nReLDVo4y7zQ0fF%25vUqYvAuWgEfJqriE0rhWn3AbvjzsoMVm4XBJ%25OBU', 'Blu', '911', 'si')
set_immagini(immagine_class, 'p911bl002', 'https://pictures.porsche.com/rtt/iris?COSY-EU-100-1711coMvsi60AAt5FwcmBEgA4qP8iBUDxPE3Cb9pNXkBuNYdMGF4tl3U0%25z8rMH1spMBvMZq6G5OtgSv31nBJaA4qh4NSEGkaW%25cz91wxuzbUUdMGLqk0DLfF%25vUqj7AuWXsOGBTeV6iTi7%25zhRc2VBsqA7fQnSPED6u5MwN9nReLDVo4y7zQ0fF%25vUqYvAuWgEfJqriE0rhWn3AbvjzsoMVm4XBJ%25OBU', 'Blu', '911', 'si')
set_immagini(immagine_class, 'p911bl003', 'https://pictures.porsche.com/rtt/iris?COSY-EU-100-1711coMvsi60AAt5FwcmBEgA4qP8iBUDxPE3Cb9pNXkBuNYdMGF4tl3U0%25z8rMH8spMBvMZq6G5OtgSv31nBJaA4qh4NSEGkaW%25cz91wxuzbUUdMGLqk0DLfF%25vUqj7AuWXsOGBTeV6iTi7%25zhRc2VBsqA7fQnSPED6u5MwN9nReLDVo4y7zQ0fF%25vUqYvAuWgEfJqriE0rhWn3AbvjzsoMVm4XBJ%25OBU', 'Blu', '911', 'si')
set_immagini(immagine_class, 'p911bl004', 'https://pictures.porsche.com/rtt/iris?COSY-EU-100-1711coMvsi60AAt5FwcmBEgA4qP8iBUDxPE3Cb9pNXkBuNYdMGF4tl3U0%25z8rMbjUuWgRcgVGPK0rh4mctLsR6EXdGvdTmJKlEnDzCBLMkYCIFF7gKpGl3UpqQDcFG8oXYnfurKRw5yPeweoDCvNzxyRuGXoq1smOJUPY0gMTBsN5pUy2dioC13qQDcFGbcXYn4Jq6GSeJ3SvnstXIc8Cu2gy9dfR6DrRF', 'Blu', '911', 'si')

set_immagini(immagine_class, 'p911g001', 'https://pictures.porsche.com/rtt/iris?COSY-EU-100-1711coMvsi60AAt5FwcmBEgA4qP8iBUDxPE3Cb9pNXkBuNYdMGF4tl3U0%25z8rMHIspMBvMZq6G5OtgSv31nBJaA4qh4NSEGkaW%25cz91wxuzbUUdMGLqk0Dx4F%25vUqj7AuWXsOGBTeV6iTi7%25zhRc2VBsqA7fQnSPED6u5MwN9nReLDVo4y7zQ0fF%25vUqYvAuWgEfJqriE0rhWn3AbvjzsoMVm4XBJ%25OBU', 'Grigio', '911', 'si') 
set_immagini(immagine_class, 'p911g002', 'https://pictures.porsche.com/rtt/iris?COSY-EU-100-1711coMvsi60AAt5FwcmBEgA4qP8iBUDxPE3Cb9pNXkBuNYdMGF4tl3U0%25z8rMH1spMBvMZq6G5OtgSv31nBJaA4qh4NSEGkaW%25cz91wxuzbUUdMGLqk0Dx4F%25vUqj7AuWXsOGBTeV6iTi7%25zhRc2VBsqA7fQnSPED6u5MwN9nReLDVo4y7zQ0fF%25vUqYvAuWgEfJqriE0rhWn3AbvjzsoMVm4XBJ%25OBU', 'Grigio', '911', 'si') 
set_immagini(immagine_class, 'p911g003', 'https://pictures.porsche.com/rtt/iris?COSY-EU-100-1711coMvsi60AAt5FwcmBEgA4qP8iBUDxPE3Cb9pNXkBuNYdMGF4tl3U0%25z8rMH8spMBvMZq6G5OtgSv31nBJaA4qh4NSEGkaW%25cz91wxuzbUUdMGLqk0Dx4F%25vUqj7AuWXsOGBTeV6iTi7%25zhRc2VBsqA7fQnSPED6u5MwN9nReLDVo4y7zQ0fF%25vUqYvAuWgEfJqriE0rhWn3AbvjzsoMVm4XBJ%25OBU', 'Grigio', '911', 'si') 
set_immagini(immagine_class, 'p911g004', 'https://pictures.porsche.com/rtt/iris?COSY-EU-100-1711coMvsi60AAt5FwcmBEgA4qP8iBUDxPE3Cb9pNXkBuNYdMGF4tl3U0%25z8rMbjUuWgRcgVGPK0rh4mctLsR6EXdGvdTmJKlEnDzCBLMkYCIFF7gKpGl3UkdQDcFG8oXYnfurKRw5yPeweoDCvNzxyRuGXoq1smOJUPY0gMTBsN5pUy2dioC13qQDcFGbcXYn4Jq6GSeJ3SvnstXIc8Cu2gy9dfR6DrRF', 'Grigio', '911', 'si') 

#Porsche Cayenne
set_immagini(immagine_class, 'pcbi001', 'https://pictures.porsche.com/rtt/iris?COSY-EU-100-1711coMvsi60AAt5FwcmBEgA4qP8iBUDxPE3Cb9pNXkBuNYdMGF4tl3U0%25z8rMHIspMBvMZq6G5OtgSv31nBJaA4qh4NSEGkaW%25cz91wxuzbUUdMGLqk0DLFxQDcFG13uWXsOaRteV6iTV9UzhRc2hGjqA7fQxupOJUPYc%25nTBsN5frq2dioCofJQDcFGFO8YnfurBJT5yPew7bzhRc2q0dqA7fQbmZOJUPYl7nTBsN5xlz2dioC1TNQDcFGbcXYnfurXhh5y%25BORrMzBjMXymQ1TOEGeQlv4DP7Rnwm', 'Bianco', 'Cayenne', 'si')
set_immagini(immagine_class, 'pcbi002', 'https://pictures.porsche.com/rtt/iris?COSY-EU-100-1711coMvsi60AAt5FwcmBEgA4qP8iBUDxPE3Cb9pNXkBuNYdMGF4tl3U0%25z8rMH1spMBvMZq6G5OtgSv31nBJaA4qh4NSEGkaW%25cz91wxuzbUUdMGLqk0DLFxQDcFG13uWXsOaRteV6iTV9UzhRc2hGjqA7fQxupOJUPYc%25nTBsN5frq2dioCofJQDcFGFO8YnfurBJT5yPew7bzhRc2q0dqA7fQbmZOJUPYl7nTBsN5xlz2dioC1TNQDcFGbcXYnfurXhh5y%25BORrMzBjMXymQ1TOEGeQlv4DP7Rnwm', 'Bianco', 'Cayenne', 'si')
set_immagini(immagine_class, 'pcbi003', 'https://pictures.porsche.com/rtt/iris?COSY-EU-100-1711coMvsi60AAt5FwcmBEgA4qP8iBUDxPE3Cb9pNXkBuNYdMGF4tl3U0%25z8rMH8spMBvMZq6G5OtgSv31nBJaA4qh4NSEGkaW%25cz91wxuzbUUdMGLqk0DLFxQDcFG13uWXsOaRteV6iTV9UzhRc2hGjqA7fQxupOJUPYc%25nTBsN5frq2dioCofJQDcFGFO8YnfurBJT5yPew7bzhRc2q0dqA7fQbmZOJUPYl7nTBsN5xlz2dioC1TNQDcFGbcXYnfurXhh5y%25BORrMzBjMXymQ1TOEGeQlv4DP7Rnwm', 'Bianco', 'Cayenne', 'si')
set_immagini(immagine_class, 'pcbi004', 'https://pictures.porsche.com/rtt/iris?COSY-EU-100-1711coMvsi60AAt5FwcmBEgA4qP8iBUDxPE3Cb9pNXkBuNYdMGF4tl3U0%25z8rMbjUuWgRcgVGPK0rh4mctLsR6EXdGvdTmJKlEnDzCBLMkYCIFF7gKpGl3UpQk1UzQKLtYnfurENh5yPewyBFCvNzxvK8GXoq1kYWr6FObzDswRuT0qSGx7e2H2q61UzQKQrAbsqYSR6w0iO5MoICvNzxG37GXoq1I9Vr6FOb%25oswRuT0k%25Cx7e2HLwT1UzQKIzfbsqYSfvv0iDRrNSgCR8gfi91LwrJK51%25cdUOoNsM9', 'Bianco', 'Cayenne', 'si')

set_immagini(immagine_class, 'pcn001', 'https://pictures.porsche.com/rtt/iris?COSY-EU-100-1711coMvsi60AAt5FwcmBEgA4qP8iBUDxPE3Cb9pNXkBuNYdMGF4tl3U0%25z8rMHIspMBvMZq6G5OtgSv31nBJaA4qh4NSEGkaW%25cz91wxuzbUUdMGLqk0D36F%25vUqbsQuWXsOaRteV6iTV9UzhRc2hGjqA7fQxupOJUPYc%25nTBsN5frq2dioCofJQDcFGFO8YnfurBJT5yPew7bzhRc2q0dqA7fQbmZOJUPYl7nTBsN5xlz2dioC1TNQDcFGbcXYnfurXhh5y%25BORrMzBjMXymQ1TOEGeQlv4DP7Rnwm', 'Nero', 'Cayenne', 'si')
set_immagini(immagine_class, 'pcn002', 'https://pictures.porsche.com/rtt/iris?COSY-EU-100-1711coMvsi60AAt5FwcmBEgA4qP8iBUDxPE3Cb9pNXkBuNYdMGF4tl3U0%25z8rMH1spMBvMZq6G5OtgSv31nBJaA4qh4NSEGkaW%25cz91wxuzbUUdMGLqk0D36F%25vUqbsQuWXsOaRteV6iTV9UzhRc2hGjqA7fQxupOJUPYc%25nTBsN5frq2dioCofJQDcFGFO8YnfurBJT5yPew7bzhRc2q0dqA7fQbmZOJUPYl7nTBsN5xlz2dioC1TNQDcFGbcXYnfurXhh5y%25BORrMzBjMXymQ1TOEGeQlv4DP7Rnwm', 'Nero', 'Cayenne', 'si')
set_immagini(immagine_class, 'pcn003', 'https://pictures.porsche.com/rtt/iris?COSY-EU-100-1711coMvsi60AAt5FwcmBEgA4qP8iBUDxPE3Cb9pNXkBuNYdMGF4tl3U0%25z8rMH8spMBvMZq6G5OtgSv31nBJaA4qh4NSEGkaW%25cz91wxuzbUUdMGLqk0D36F%25vUqbsQuWXsOaRteV6iTV9UzhRc2hGjqA7fQxupOJUPYc%25nTBsN5frq2dioCofJQDcFGFO8YnfurBJT5yPew7bzhRc2q0dqA7fQbmZOJUPYl7nTBsN5xlz2dioC1TNQDcFGbcXYnfurXhh5y%25BORrMzBjMXymQ1TOEGeQlv4DP7Rnwm', 'Nero', 'Cayenne', 'si')
set_immagini(immagine_class, 'pcn004', 'https://pictures.porsche.com/rtt/iris?COSY-EU-100-1711coMvsi60AAt5FwcmBEgA4qP8iBUDxPE3Cb9pNXkBuNYdMGF4tl3U0%25z8rMbjUuWgRcgVGPK0rh4mctLsR6EXdGvdTmJKlEnDzCBLMkYCIFF7gKpGl3UtPQDcFGIu1YnfurENh5yPewyBFCvNzxvK8GXoq1kYWr6FObzDswRuT0qSGx7e2H2q61UzQKQrAbsqYSR6w0iO5MoICvNzxG37GXoq1I9Vr6FOb%25oswRuT0k%25Cx7e2HLwT1UzQKIzfbsqYSfvv0iDRrNSgCR8gfi91LwrJK51%25cdUOoNsM9', 'Nero', 'Cayenne', 'si')

#Mercedes Classe G
set_immagini(immagine_class, 'mcgn001', 'https://api.beesmart.digitalitis.eu//thumbnail/1024/768/?url=https://digitalitis-bonera.cust.nl.phyron.com/repo/U_1093291/bg-removal-9b2c708806266334d9d2f354ffa397d368d60e38a6a142bc36a8258feeae4223.jpg', 'Nero', 'Classe G', 'si')
set_immagini(immagine_class, 'mcgn002', 'https://api.beesmart.digitalitis.eu//thumbnail/1024/768/?url=https://digitalitis-bonera.cust.nl.phyron.com/repo/U_1093291/bg-removal-886f0d80e305aa5f929ce73c956b9c5527aa5917c7377470c97d06ba7d9bb5af.jpg', 'Nero', 'Classe G', 'si')
set_immagini(immagine_class, 'mcgn003', 'https://api.beesmart.digitalitis.eu//thumbnail/1024/768/?url=https://digitalitis-bonera.cust.nl.phyron.com/repo/U_1093291/bg-removal-cf18a7c8b69c4f19a67fdb1ff6c7e3caf3f2af791d81ebfde9f724241a43dee4.jpg', 'Nero', 'Classe G', 'si')
set_immagini(immagine_class, 'mcgn004', 'https://api.beesmart.digitalitis.eu//thumbnail/1024/768/?url=https://digitalitis-bonera.cust.nl.phyron.com/repo/U_1093291/bg-removal-a75509d13cdae4279eff8f9fad995e4a555339717505708f98f938c10c87177c.jpg', 'Nero', 'Classe G', 'si')

set_immagini(immagine_class, 'mcgb001', 'https://img.sm360.ca/ir/w640h390c/images/newcar/ca/2024/mercedes-benz/classe-g/550v/suv/exteriorColors/2024_mercedes-benz_classe-g_1-550v_1-ext_032_149.png', 'Bianco', 'Classe G', 'si')
set_immagini(immagine_class, 'mcgb002', 'https://img.sm360.ca/ir/w640h480/images/newcar/ca/2023/mercedes-benz/classe-g/550v/suv/2023_mercedes-benz_classe-g_550v_photos_003.jpg', 'Bianco', 'Classe G', 'si')
set_immagini(immagine_class, 'mcgb003', 'https://cdni.autocarindia.com/Utils/ImageResizerV2.ashx?n=https://cms.haymarketindia.net/model/uploads/modelimages/G-ClassModelImage.jpg&w=872&h=578&q=75&c=1', 'Bianco', 'Classe G', 'si')
set_immagini(immagine_class, 'mcgb004', 'https://www.trivellato.it/data_files/landing/eqg-7-f15kkq.jpg', 'Bianco', 'Classe G', 'si')

#Mercedes GLC Coupè
set_immagini(immagine_class, 'mglccn001', 'https://player.hu/uploads/2023/03/mercedes-benz-glc-coupe-22.jpg', 'Nero', 'GLC Coupè', 'si')
set_immagini(immagine_class, 'mglccn002', 'https://stimg.cardekho.com/images/carexteriorimages/630x420/Mercedes-Benz/GLC-Coupe-2023/9730/1678950667198/rear-right-side-48.jpg?imwidth=420&impolicy=resize', 'Nero', 'GLC Coupè', 'si')
set_immagini(immagine_class, 'mglccn003', 'https://autoportal.hr/wp-content/uploads/2023/03/Mercedes-GLC-Coupe-2023-1-1.jpg', 'Nero', 'GLC Coupè', 'si')
set_immagini(immagine_class, 'mglccn004', 'https://ecomento.de/wp-content/uploads/2023/03/Mercedes-Benz-GLC-Coupe-Plug-in-Hybrid-2023-3-1200x689.jpg', 'Nero', 'GLC Coupè', 'si')

set_immagini(immagine_class, 'mglccbl001', 'https://www.mercedes-benz.it/content/dam/hq/passengercars/cars/glc/glc-coupe-c254-fl-pi/overview/highlights/04-2023/images/mercedes-benz-glc-coupe-c254-highlights-videostill-3302x1858-04-2023.jpg', 'Blu', 'GLC Coupè', 'si')
set_immagini(immagine_class, 'mglccbl002', 'https://www.mercedes-benz.it/content/italy/it/passengercars/models/suv/c254-24-1/overview/_jcr_content/root/responsivegrid/media_slider/media_slider_item_905520351/image.component.damq1.3394488588988.jpg/mercedes-benz-glc-coupe-c254-highlights-exterior-3302x1858-04-2023.jpg', 'Blu', 'GLC Coupè', 'si')
set_immagini(immagine_class, 'mglccbl003', 'https://www.merbag.ch/media/qdrde3y2/mercedes-glc-coupe-04.jpg?width=2280&quality=100&preferFocalPoint=false&useCropDimensions=false&maxwidth=3840&maxheight=3840&format=webp&lazyload=true&lazyloadPixelated=true&c.focalPoint=0.5,0.5&mode=crop&c.finalmode=crop&c.zoom=false', 'Blu', 'GLC Coupè', 'si')
set_immagini(immagine_class, 'mglccbl004', 'https://www.mercedes-benz.it/content/italy/it/passengercars/models/suv/c254-24-1/overview/_jcr_content/root/responsivegrid/media_slider/media_slider_item/internal_video.component.damq1.3394488592305.jpg/mercedes-benz-glc-coupe-c254-highlights-videostill-3302x1858-04-2023.jpg', 'Blu', 'GLC Coupè', 'si')

#Mercedes AMG GT Coupé
set_immagini(immagine_class, 'mamggtcg001', 'https://www.mercedes-benz.it/content/italy/it/passengercars/models/coupe/amg-gt-c192/overview/_jcr_content/root/responsivegrid/media_slider_copy_co/media_slider_item/internal_video.component.damq1.3389376203351.jpg/mercedes-amg-gt-c192-highlights-videostill-3302x1858-07-2023.jpg', 'Grigio', 'AMG GT Coupé', 'si')
set_immagini(immagine_class, 'mamggtcg002', 'https://www.mercedes-benz.it/content/italy/it/passengercars/models/coupe/amg-gt-c192/overview/_jcr_content/root/responsivegrid/media_gallery_copy/media_gallery_item_542640333/image.component.damq1.3389376360570.jpg/mercedes-amg-gt-c192-exterior-gt63-rear-2176x1224-07-2023.jpg', 'Grigio', 'AMG GT Coupé', 'si')
set_immagini(immagine_class, 'mamggtcg003', 'https://cdn.unitycms.io/images/41qQqNAEqby9VhCSgFdVoQ.jpg?op=ocroped&val=1200,1200,843,749,139,93&sum=cmnOfXuNiLY', 'Grigio', 'AMG GT Coupé', 'si')
set_immagini(immagine_class, 'mamggtcg004', 'https://www.mercedes-benz.it/content/italy/it/passengercars/models/coupe/amg-gt-c192/overview/_jcr_content/root/responsivegrid/media_slider_copy_co/media_slider_item_711472719/image.component.damq1.3389376204733.jpg/mercedes-amg-gt-c192-higlights-exterior-3302x1858-07-2023.jpg', 'Grigio', 'AMG GT Coupé', 'si')

set_immagini(immagine_class, 'mamggtcb001', 'https://listings-prod.tcimg.net/listings/283013/75/25/WDDYJ7HA8HA012575/377PR3VM3BMYPQMAJTT43MPDJI-cr-860.jpg', 'Bianco', 'AMG GT Coupé', 'si')
set_immagini(immagine_class, 'mamggtcb002', 'https://listings-prod.tcimg.net/listings/283013/75/25/WDDYJ7HA8HA012575/SUWWYGHDDHT6NCHTT7ITQB7ZFE-cr-860.jpg', 'Bianco', 'AMG GT Coupé', 'si')
set_immagini(immagine_class, 'mamggtcb003', 'https://listings-prod.tcimg.net/listings/283013/75/25/WDDYJ7HA8HA012575/LXBZFHVPNNHAHUPSXZYY7BELEE-cr-860.jpg', 'Bianco', 'AMG GT Coupé', 'si')
set_immagini(immagine_class, 'mamggtcb004', 'https://listings-prod.tcimg.net/listings/283013/75/25/WDDYJ7HA8HA012575/INVNUGU7BEPCHPUQJJQ67CG4D4-cr-860.jpg', 'Bianco', 'AMG GT Coupé', 'si')

# Inserimento delle auto usate
@db_session()
def set_autoUsata(AutoUsata, targa, proprietario, valutatore):
   AutoUsata(
       targa = targa, 
       proprietario = proprietario, 
       valutatore = valutatore
   )

set_autoUsata(autoUsata_class, 'AA123BB', 'vale46@gmail.com', 'i002')
set_autoUsata(autoUsata_class, 'AB987BA', 'cav.reb@gmail.com', 'i003')

# Inserimento colore modello
@db_session()
def set_coloremodello(ColoreModello, id, colore, modello, prezzo, vis):
   ColoreModello(
       id = id, 
       colore = colore, 
       modello = modello, 
       prezzo = prezzo,
       visibility = vis
   )

#Ferrari
set_coloremodello(coloreModello_class, 'fpgr', 'Grigio', 'Purosangue', '1000', 'si')
set_coloremodello(coloreModello_class, 'fpgm', 'Giallo Modena', 'Purosangue', '3000', 'si')
set_coloremodello(coloreModello_class, 'fsf90n', 'Nero', 'Purosangue', '1000', 'si')
set_coloremodello(coloreModello_class, 'fsf90ri', 'Rosso Imola', 'SF90 Stradale', '3000', 'si')
set_coloremodello(coloreModello_class, 'frgr', 'Grigio', 'Roma', '1000', 'si')
set_coloremodello(coloreModello_class, 'frbi', 'Bianco', 'Roma', '1000', 'si')

#Porsche
set_coloremodello(coloreModello_class, 'ppn', 'Nero', 'Panamera', '1000', 'si')
set_coloremodello(coloreModello_class, 'ppb', 'Bianco', 'Panamera', '1000', 'si')
set_coloremodello(coloreModello_class, 'p911bl', 'Blu', '911', '3000', 'si')
set_coloremodello(coloreModello_class, 'p911gr', 'Grigio', '911', '1000', 'si')
set_coloremodello(coloreModello_class, 'pcn', 'Nero', 'Cayenne', '1000', 'si')
set_coloremodello(coloreModello_class, 'pcb', 'Bianco', 'Cayenne', '1000', 'si')

#Mercedes
set_coloremodello(coloreModello_class, 'mcgn', 'Nero', 'Classe G', '1000', 'si')
set_coloremodello(coloreModello_class, 'mcgb', 'Bianco', 'Classe G', '1000', 'si')
set_coloremodello(coloreModello_class, 'mglccn', 'Nero', 'GLC Coupè', '1000', 'si')
set_coloremodello(coloreModello_class, 'mglccbl', 'Blu', 'GLC Coupè', '2500', 'si')
set_coloremodello(coloreModello_class, 'mamggtcgr', 'Grigio', 'AMG GT Coupé', '1500', 'si')
set_coloremodello(coloreModello_class, 'mamggtcb', 'Bianco', 'AMG GT Coupé', '1000', 'si')

# Inserimento motore modello
@db_session()
def set_motoremodello(MotoreModello, id, motore, modello, prezzo, vis):
   MotoreModello(
       id = id, 
       motore = motore, 
       modello = modello, 
       prezzo = prezzo,
       visibility = vis
   )

#Ferrari
set_motoremodello(motoreModello_class, 'fpbe', 'mb001', 'Purosangue', 2000, 'si')
set_motoremodello(motoreModello_class, 'fpe', 'mi002', 'Purosangue', 3000, 'si')

set_motoremodello(motoreModello_class, 'fsf90be', 'mb003', 'SF90 Stradale', 2500, 'si')

set_motoremodello(motoreModello_class, 'frbe', 'mb003', 'Roma', 2000, 'si')

#Porsche
set_motoremodello(motoreModello_class, 'ppbe', 'mb003', 'Panamera', 1000, 'si')
set_motoremodello(motoreModello_class, 'ppi', 'mi001', 'Panamera', 2500, 'si')
set_motoremodello(motoreModello_class, 'ppe', 'me001', 'Panamera', 3000, 'si')
set_motoremodello(motoreModello_class, 'ppip', 'mpi003', 'Panamera', 2500, 'si')

set_motoremodello(motoreModello_class, 'p911be', 'mb003', '911', 2000, 'si')
set_motoremodello(motoreModello_class, 'p911i', 'mi001', '911', 3000, 'si')

set_motoremodello(motoreModello_class, 'pcbe', 'mb003', 'Cayenne', 1000, 'si')
set_motoremodello(motoreModello_class, 'pce', 'mpi002', 'Cayenne', 2000, 'si')

#Mercedes
set_motoremodello(motoreModello_class, 'mcgbe', 'mb001', 'Classe G', 1000, 'si')
set_motoremodello(motoreModello_class, 'mcge', 'me002', 'Classe G', 2500, 'si')

set_motoremodello(motoreModello_class, 'mglccbe', 'mb002', 'GLC Coupè', 2000, 'si')
set_motoremodello(motoreModello_class, 'mglccib', 'mpi001', 'GLC Coupè', 2500, 'si')

set_motoremodello(motoreModello_class, 'mamggtcbe', 'mb002', 'AMG GT Coupé', 1500, 'si')

# Inserimento optional modello
@db_session()
def set_optionalmodello(OptionalModello, id, optional, modello, prezzo, vis):
   OptionalModello(
       id = id, 
       optional = optional, 
       modello = modello, 
       prezzo = prezzo,
       visibility = vis
   )

#Ferrari
set_optionalmodello(optionalModello_class, 'fp001', 'Sedili in pelle', 'Purosangue', 1500, 'si')
set_optionalmodello(optionalModello_class, 'fp002', 'Cerchi diametro 21 pollici in carbonio', 'Purosangue', 1000, 'si')
set_optionalmodello(optionalModello_class, 'fp003', 'Tetto panoramico', 'Purosangue', 3500, 'si')
set_optionalmodello(optionalModello_class, 'fp004', 'Vetri Oscurati', 'Purosangue', 1000, 'si')

set_optionalmodello(optionalModello_class, 'fsf90001', 'Sedili in pelle', 'SF90 Stradale', 3500, 'si')
set_optionalmodello(optionalModello_class, 'fsf90002', 'Cerchi diametro 21 pollici in carbonio', 'SF90 Stradale', 2500, 'si')

set_optionalmodello(optionalModello_class, 'fr001', 'Sedili in pelle', 'Roma', 2500, 'si')
set_optionalmodello(optionalModello_class, 'fr002', 'Vetri Oscurati', 'Roma', 1000, 'si')

#Porsche
set_optionalmodello(optionalModello_class, 'pp001', 'Sedili in pelle', 'Panamera', 1500, 'si')
set_optionalmodello(optionalModello_class, 'pp002', 'Tetto panoramico', 'Panamera', 1000, 'si')

set_optionalmodello(optionalModello_class, 'p911001', 'Sedili in pelle', '911', 2500, 'si')
set_optionalmodello(optionalModello_class, 'p911002', 'Cerchi diametro 21 pollici in carbonio', '911', 1500, 'si')
set_optionalmodello(optionalModello_class, 'p911003', 'Tetto panoramico', '911', 2500, 'si')
set_optionalmodello(optionalModello_class, 'p911004', 'Vetri Oscurati', '911', 1000, 'si')

set_optionalmodello(optionalModello_class, 'pc001', 'Sedili in pelle', 'Cayenne', 1000, 'si')
set_optionalmodello(optionalModello_class, 'pc002', 'Vetri Oscurati', 'Cayenne', 2000, 'si')
set_optionalmodello(optionalModello_class, 'pc003', 'Tetto panoramico', 'Cayenne', 2500, 'si')

#Mercedes
set_optionalmodello(optionalModello_class, 'mcg001', 'Sedili in pelle', 'Classe G', 1000, 'si')
set_optionalmodello(optionalModello_class, 'mcg002', 'Vetri Oscurati', 'Classe G', 2000, 'si')
set_optionalmodello(optionalModello_class, 'mcg003', 'Tetto panoramico', 'Classe G', 2500, 'si')

set_optionalmodello(optionalModello_class, 'mglcc001', 'Sedili in pelle', 'GLC Coupè', 1500, 'si')
set_optionalmodello(optionalModello_class, 'mglcc002', 'Vetri Oscurati', 'GLC Coupè', 2500, 'si')

set_optionalmodello(optionalModello_class, 'mamggtc001', 'Sedili in pelle', 'AMG GT Coupé', 2000, 'si')
set_optionalmodello(optionalModello_class, 'mamggtc002', 'Cerchi diametro 21 pollici in carbonio', 'AMG GT Coupé', 2500, 'si')


# Inserimento sconti modello
@db_session()
def set_scontomodello(ScontoModello, id, sconto, modello, vis):
   ScontoModello(
       id = id, 
       sconto = sconto, 
       modello = modello,
       visibility = vis
   )

#Ferrari
set_scontomodello(scontoModello_class, 'sfp002', 'REDp', 'Purosangue', 'si')
set_scontomodello(scontoModello_class, 'sfp003', 'SESSIONE', 'Purosangue', 'si')

set_scontomodello(scontoModello_class, 'sfsf90002', 'REDp', 'SF90 Stradale', 'si')

set_scontomodello(scontoModello_class, 'sfr001', 'REDp', 'Roma', 'si')
set_scontomodello(scontoModello_class, 'sfr002', 'SESSIONE', 'Roma', 'si')

#Porsche
set_scontomodello(scontoModello_class, 'spp001', 'BF2024', 'Panamera', 'si')
set_scontomodello(scontoModello_class, 'spp002', 'SESSIONE', 'Panamera', 'si')

set_scontomodello(scontoModello_class, 'sp911001', 'BF2024', '911', 'si')
set_scontomodello(scontoModello_class, 'sp911002', 'SESSIONE', '911', 'si')

set_scontomodello(scontoModello_class, 'spc001', 'BF2024', 'Cayenne', 'si')
set_scontomodello(scontoModello_class, 'spc002', 'SESSIONE', 'Cayenne', 'si')

#Mercedes
set_scontomodello(scontoModello_class, 'smcg001', 'SESSIONE', 'Classe G', 'si')

set_scontomodello(scontoModello_class, 'smglcc001', 'SESSIONE', 'GLC Coupè', 'si')

set_scontomodello(scontoModello_class, 'smamggtc001', 'SESSIONE', 'AMG GT Coupé', 'si')