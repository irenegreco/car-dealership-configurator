from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_file, send_from_directory
from database10.database import *
from pony.orm import db_session
from flask_login import LoginManager, login_user, logout_user, login_required
from flask import jsonify
from datetime import datetime, timedelta
from datetime import date
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image
from io import BytesIO
from uuid import uuid4

import uuid
import json
import os
import random

from amm import init_admin_routes  # Importa la funzione per inizializzare le route dell'amministrazione

app = Flask(__name__)   # SINGLETON

# Inizializza le route dell'amministrazione
init_admin_routes(app)         

app.secret_key = 'chiave_segreta_clienti'
app.config['CLIENT_SESSION_KEY'] = 'cliente_user_id'

login_manager_cliente = LoginManager()
login_manager_cliente.init_app(app)
login_manager_cliente.login_view = 'login_cliente'


# Home page: reindirizza alla home page del sito passando i modelli per marca come dizionario e gli sconti con i modelli associati come lista.
@app.route("/")
@app.route("/home")
def home_page():
    modelli_per_marca = {}
    sconti_con_modelli = []
    
    with db_session:
        # Recupera tutti i modelli divisi per marca
        marche_auto = brand_class.select().order_by(brand_class.nome)
        for marca in marche_auto:
            modelli = modello_class.select(lambda m: m.brand == marca).prefetch(modello_class.immagine)
            modelli_per_marca[marca] = modelli
        
        # Recupera tutti gli sconti con i modelli associati
        sconti = sconto_class.select()
        for sconto in sconti:
            modelli_assoc = [sm.modello for sm in sconto.sconto_modello]
            sconti_con_modelli.append({
                'codice': sconto.codice,
                'dal': sconto.dal,
                'al': sconto.al,
                'modelli': modelli_assoc
            })

        return render_template('home.html', modelli_per_marca=modelli_per_marca, sconti_con_modelli=sconti_con_modelli)     # TEMPLATE

###################################################################### ACCESSO E AREA RISERVATA #################################################################################

# metodo del pacchetto Flask Login per poter modificare il messaggio per segnalare la necessità di accedere per poter entrare nell'are ariservata
@login_manager_cliente.unauthorized_handler
def unauthorized_callback():
    flash('Bisogna effettuare il login per accedere all\'area riservata', 'error')
    return redirect(url_for('login_cliente'))

# metodo del pacchetto Flask Login per ricordarsi dell'utente che ha effettuato l'accesso
@login_manager_cliente.user_loader
@db_session
def load_user(cliente_user_id):
    return cliente_class.get(email=cliente_user_id)

# funzione per autenticare i dati inseriti dall'utente durante l'accesso. Se i valori sono corretti l'utente viene caricato nella sessione
# corrente (in modo da ricordarsi sempre chi è l'utente che ha effettuato l'accesso)
@db_session
def authenticate(username, password):
    # Cerca l'utente nel database in base all'email
    cliente = cliente_class.get(email=username)

    if cliente and cliente.pw == password:
        login_user(cliente)
        session[app.config['CLIENT_SESSION_KEY']] = cliente.email
        return True, "Utente trovato", cliente
    else:
        return False, "Password o email non corrette", None


# Route che gestisce le richieste di accesso da parte del cliente assicurandosi di autenticare le credenziali inserite e di reindirizzare l'utente all'area riservata (route)
@app.route('/login_cliente', methods=['GET', 'POST'])
def login_cliente():
    if request.method == 'POST':
        username = request.form['usrname']
        password = request.form['psw']

        authenticated, message, user = authenticate(username, password)
        if authenticated:
            if user:
                session[app.config['CLIENT_SESSION_KEY']] = user.email
                
                if 'configurazione_utente' in session:
                    return redirect(url_for('save_configuration'))
                
                return redirect(url_for('areaRiservataCliente'))  
            else:
                flash('Utente non trovato', 'error')
        else:
            flash(message, "error")
    return render_template('login.html')


# ROUTE AREA RISERVATA DELL'UTENTE
# controlla se l'utente ha effettuato l'accesso e reindirizza alla pagina riservata dell'utente riportando le informazioni:
#   - configurazioni salvate
#   - preventivi con e senza la valutazione dell'usato
#   - ordini da confermare, confermati e conclusi
#   - messaggi da leggere
#   - sedi
#   - cliente

# altrimenti reindirizza alla pagina di accesso
@app.route('/areaRiservataCliente')
@login_required
def areaRiservataCliente():      
    with db_session:
        oggi = date.today()
        user_email = session[app.config['CLIENT_SESSION_KEY']]
        cliente = cliente_class.get(email=user_email)
        
        if cliente:
            configurazioni = auto_class.select(lambda a: a.cliente == cliente)[:]
            
            # preventivi senza la valutazione dell'usato. Una volta confermati vengono inviati direttamente nella sezione STORICO PREVENTIVI
            preventivi = select(p for p in preventivo_class if p.auto_rottamata is None and p.cliente==cliente) [:]
            
            # Decurtazione del valore dello sconto mensile eventualmente associato ai modelli dei preventivi
            for preventivo in preventivi:
                if not preventivo.valore_sconto and not preventivo.auto_rottamata:
                    sconti_modello = scontoModello_class.select(modello=preventivo.auto.modello)
                    preventivo.prezzo = preventivo.auto.prezzo_totale

                    for sconto_modello in sconti_modello:
                        if sconto_modello.sconto.dal <= oggi <= sconto_modello.sconto.al:
                            preventivo.sconto_mese = sconto_modello.sconto
                        
                        if preventivo.sconto_mese:
                            prezzo_scontato = preventivo.prezzo * (preventivo.sconto_mese.percentuale / 100)
                            preventivo.valore_sconto = round(prezzo_scontato, 2)
                            preventivo.prezzo = preventivo.prezzo - preventivo.valore_sconto
            
            preventiviDaValutare = select(p for p in preventivo_class if p.valore_sconto_rottamazione is None and p.cliente==cliente and p.prezzo==0) [:]
            # preventivi già valutati
            preventiviUsato = select(p for p in preventivo_class if p.auto_rottamata is not None and p.cliente==cliente and p.prezzo!=0) [:]
            
            # Rimuove i preventivi scaduti (non confermati entro 20 giorni)
            for preventivo in preventivi + preventiviUsato:
                if (oggi - preventivo.data).days > 20:
                    preventivo.delete()
                    db.commit()
                    flash('Preventivo scaduto')
                    return redirect(url_for('areaRiservataCliente'))  
                       
            # lista di tutti i preventivi con e senza usato
            totPreventivi = []
            for preventivo in preventivi + preventiviUsato:
                if (oggi - preventivo.data).days <= 20:
                    preventivo.data_scadenza = preventivo.data + timedelta(days=20)
                    totPreventivi.append(preventivo)
            
            sedi = sede_class.select()
                        
            ordiniDaConfermare = select(o for o in ordine_class if o.gestore_ordine is not None and o.preventivo.cliente==cliente) [:]
            ordiniConfermati = select(o for o in ordine_class if o.gestore_ordine is  None and o.preventivo.cliente==cliente) [:]
            ordiniConclusi = select(o for o in ordine_class if o.gestore_ordine is None and o.preventivo.cliente == cliente and ( exists(m for m in messaggio_class if m.ordine == o)))[:]

            messaggi_non_letti = select(m for m in messaggio_class if m.lettura == 'no' and m.ordine.preventivo.cliente == cliente)[:]

            return render_template('utente.html', ordiniConclusi=ordiniConclusi, messaggi_non_letti=messaggi_non_letti, configurazioni=configurazioni, cliente=cliente, ordiniDaConfermare=ordiniDaConfermare, ordiniConfermati=ordiniConfermati, totPreventivi=totPreventivi, sedi=sedi, oggi=oggi, preventiviDaValutare=preventiviDaValutare)
   
        else:
            flash('Utente non trovato', 'error')
            return redirect(url_for('home_page'))


# route che conferma la lettura dei messaggi inviati dagli impiegati andando a modificare l'attributo lettura di messaggio
@app.route('/conferma_lettura/<cod_messaggio>', methods=['POST'])
@login_required
def conferma_lettura(cod_messaggio):
    with db_session:
        ordine = ordine_class.get(codice=cod_messaggio)
        messaggio = messaggio_class.get(ordine=ordine)
        print(messaggio)
        if messaggio:
            messaggio.lettura = 'si'
            db.commit()
            flash('Messaggio segnato come letto.', 'success')
        else:
            flash('Messaggio non trovato.', 'error')
    return redirect(url_for('areaRiservataCliente'))


# route per la registrazione che convalida i valori inseriti dall'utente per registrarlo. Richiama la funzione validate_registration definita in database.py che controlla
# la validità dei parametri inseriti e se l'utente esiste già. Reindirizza alla pagina di accesso se la registrazione va a buon fine, altrimenti rimane 
# sulla pagina della registrazione ripassando i parametri inseriti in modo tale da non dover reinserire da capo tutto.
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']

        username = request.form['usrname']
        password = request.form['psw']

        success, msg = validate_registration(name, surname, username, password)
        if success:
            with db_session:
                user = cliente_class(name=name, surname=surname, email=username, pw=password)
                db.commit()              
            flash(msg, "success") 
            return redirect(url_for('login_cliente'))  
        else:
            flash(msg, "error") 
            
    return render_template('registration.html', name=request.form.get('name'), surname=request.form.get('surname'), usrname=request.form.get('usrname'))


# route che toglie l'utente corrente dalla sessione ed effettua il logout reindirizzando all'home page
@app.route('/logout')
@login_required
def logout():
    if app.config['CLIENT_SESSION_KEY'] in session:
        session.pop(app.config['CLIENT_SESSION_KEY'])
    logout_user()
    return redirect(url_for('home_page'))


###################################################################### CONFIGURATORE #################################################################################
# Route che gestisce le richieste di salvataggio della configurazione. 
#  - Richiesta di tipo POST: se l'utente ha già effettuato l'accesso reindirizza alla route di salvataggio della configurazione, altrimenti reindirizza al login.
#  - Richiesta di tipo GET: se è già presente una configurazione in sessione allora viene passata. In ogni caso rendirizza alla pagina del configuratore.
@app.route("/configuratore", methods=['GET', 'POST'])
@db_session
def configuratore():
    #marche = brand_class.select().order_by(brand_class.nome)[:]
    marche = select(b for b in brand_class if b.visibility == 'si') [:]
    
    if request.method == 'POST':
        # Memorizza la configurazione dell'utente nella sessione
        session['configurazione_utente'] = request.form.to_dict()
        print(session['configurazione_utente'])
        
        if 'cliente_user_id' in session:
            # Se l'utente è autenticato, salva direttamente la configurazione nel database
            return redirect(url_for('save_configuration'))
        else:
            # Se l'utente non è autenticato, reindirizza alla pagina di login
            flash('Per salvare la configurazione è necessario effettuare il login', 'warning')
            return redirect(url_for('login_cliente'))
        
    # Se la configurazione utente è già presente nella sessione, passala al template
    if 'configurazione_utente' in session:
        configurazione_utente = session['configurazione_utente']
        return render_template('configuratore.html', marche=marche, **configurazione_utente)
    
    return render_template('configuratore.html', marche=marche)

# Le route che seguono vengono richiamate da configuratore.html, in particolare da javascript che cambia dinamicamente le informazioni
# mostrate nel configuratore, in base le scelte dell'utente. 
# Questa route riceve in input la marca selezionata dall'utente e recupera dal database tutti i modelli associati a quella marca.
# i modelli vengono inseriti in formato json.
@app.route('/get_modelli/<marca_nome>')
@db_session
def get_modelli(marca_nome):
    marca = brand_class.get(nome=marca_nome)
    if marca:
        #modelli = modello_class.select(lambda m: m.brand == marca).order_by(modello_class.nome)
        modelli = select(m for m in modello_class if m.brand == marca and m.visibility == 'si') [:]
        modelli_json = []
        for modello in modelli:
            modello_dict = {
                'nome': modello.nome,
                'descrizione': modello.descrizione
            }
            modelli_json.append(modello_dict)
        return jsonify(modelli_json)
    return jsonify([]), 404

# Questa route gestisce il recupero del prezzo dei modelli in formato json
@app.route('/get_prezzo_modello/<modello_nome>')
@db_session
def get_prezzo_modello(modello_nome):
    modello = modello_class.get(nome=modello_nome)
    if modello:
        return jsonify({'prezzo_base': modello.prezzo_base})
    return jsonify({'prezzo_base': 0}), 404

# Questa route gestisce il recupero delle immagini associate ai modelli in formato json
@app.route('/get_immagini_modello_colore/<modello_nome>/<colore_nome>')
@db_session
def get_immagini_modello_colore(modello_nome, colore_nome):
    modello = modello_class.get(nome=modello_nome)
    colore = colore_class.get(nome=colore_nome)
    if modello and colore:
        immagini = select(i for i in immagine_class if i.modello.nome == modello_nome and i.colore.nome == colore_nome and i.visibility == 'si')
        immagini_urls = [immagine.codiceURL for immagine in immagini]

        if immagini:
            return jsonify({'immagini_urls': immagini_urls})
    return jsonify({'immagini_urls': []}), 404

# Questa route gestisce il recupero dei colori associati ai modelli e il loro prezzo in formato json
@app.route('/get_colori/<modello_nome>')
@db_session
def get_colori(modello_nome):
    modello = modello_class.get(nome=modello_nome)
    if modello:
        colori_modello = select(cm for cm in coloreModello_class if cm.modello == modello and cm.visibility == 'si')
        colori_json = []
        for cm in colori_modello:
            colori_json.append({
                'nome': cm.colore.nome,
                'prezzo': cm.prezzo
            })
        return jsonify(colori_json)
    return jsonify([]), 404

# Questa route gestisce il recupero dei motori associati ai modelli e il loro prezzo in formato json
@app.route('/get_motori/<modello_nome>')
@db_session
def get_motori(modello_nome):
    modello = modello_class.get(nome=modello_nome)
    if modello:
        motori_modello = select(mm for mm in motoreModello_class if mm.modello == modello and mm.visibility == 'si')
        motori_json = []
        for mm in motori_modello:
            motori_json.append({
                'codice': mm.motore.codice,
                'nome': mm.motore.alimentazione,
                'prezzo': mm.prezzo,
            })
        return jsonify(motori_json)
    return jsonify([]), 404

# Questa route gestisce il recupero degli optional associati ai modelli e il loro prezzo in formato json
@app.route('/get_optional/<modello_nome>')
@db_session
def get_optional(modello_nome):
    modello = modello_class.get(nome=modello_nome)
    if modello:
        optional_modello = select(o for o in optionalModello_class if o.modello == modello and o.visibility == 'si')
        optional_json = [{'nome': o.optional.nome, 'prezzo': o.prezzo} for o in optional_modello]
        return jsonify(optional_json)
    return jsonify([]), 404

# Route che gestisce il salvataggio della configurazione. Viene effettuato un ulteriore controllo, anche se ridondante, sulla presenza dell'utente nella sessione. 
# Il controllo è già effettuato dalla route configuratore.
@app.route('/save_configuration', methods=['GET','POST'])
@login_required
def save_configuration():
    if 'configurazione_utente' in session:
        with db_session:
            user_email = session[app.config['CLIENT_SESSION_KEY']]
            cliente = cliente_class.get(email=user_email)
            if cliente:
                form_data = session.pop('configurazione_utente')
                codice = str(uuid4())
                                   
                configurazione = auto_class(
                    codice=codice,
                    prezzo_totale=float(form_data['prezzo_totale']),
                    cliente=cliente,
                    modello=modello_class.get(nome=form_data['modello']),
                    motore=motore_class.get(codice=form_data['motore']),
                    colore=colore_class.get(nome=form_data['colore']),
                )
                db.commit()
                                
                # Gestisce il recupero degli optional associati alla configurazione e li salva nel database in 'optional_entity'
                optional_data = form_data['optional_data']
                if optional_data:
                    optional_data = json.loads(optional_data)

                    for optional in optional_data:
                        optional_name = optional['nome']

                        optional_price = optional['prezzo']

                        # Cerca l'entità Optional nel database
                        optional_entity = optional_class.get(nome=optional_name)
                        print(type(optional_entity))
                        if optional_entity:
                            # Crea l'entità SceltaOptional e associa con Auto e Optional
                            scelta_optional = sceltaOptional_class(
                                auto=configurazione,
                                optional=optional_entity,
                            )
                            db.commit()  
                        
                flash('Configurazione salvata con successo', 'success')
        return redirect(url_for('areaRiservataCliente'))
    else:
        flash('Nessuna configurazione da salvare', 'warning')
        return redirect(url_for('areaRiservataCliente'))

# Questa route gestisce l'eliminazione della configurazione. L'eliminazione è consentita solamente se non si è già richiesto il preventivo. Se si cerca di eliminare
# una configurazione alla quale è associato un preventivo allora verrà visualizzato un messaggio di errore, altrimenti l'auto verrà eliminata dal database.
@app.route('/elimina_configurazione/<codice>', methods=['POST'])
@login_required
def elimina_configurazione(codice):
    with db_session:
        user_email = session[app.config['CLIENT_SESSION_KEY']]
        cliente = cliente_class.get(email=user_email)
        if cliente:
            configurazione = auto_class.get(codice=codice, cliente=cliente)
            if configurazione:
                preventivo = preventivo_class.get(auto=configurazione)
                if preventivo:
                    flash('Hai inviato una richiesta di preventivo per questa configurazione. Per favore, contatta il nostro servizio clienti al numero +00 012 234 5678. Loro ti potranno aiutare ', 'error')
                    return redirect(url_for('areaRiservataCliente'))
                else:
                    configurazione.delete()  
                    flash('Configurazione eliminata con successo', 'success')
            else:
                flash('Configurazione non trovata', 'error')
        else:
            flash('Utente non trovato', 'error')

    return redirect(url_for('areaRiservataCliente'))

########################################################################  RICHIESTA PREVENTIVI ################################################################################################################

# Route che gestisce le richieste di preventivi con e senza valutazione dell'usato. Innanzitutto si recupera l'auto relativa all'id della configurazione data in input.
# Poi si controlla se è già presente un preventivo per questa configurazione e si ritorna un messaggio di errore. Si recuperano il cliente dalla sessione e gli 
# eventuali dati dal form della valutazione dell'usato. Successivamente si va a controllare il corretto inserimento dei campi per la valutazione usato, se sono inseriti
# verrà creato un preventivo con la valutazione dell'usato, altrimenti senza.
@app.route('/valuta_usato/<configurazione_id>', methods=['POST'])
@db_session
def valuta_usato(configurazione_id):
    configurazione = auto_class.get(codice=configurazione_id)
    
    if not configurazione:
        flash('Configurazione non trovata', 'error')
        return redirect(url_for('areaRiservataCliente'))
    
    preventivo_esistente = preventivo_class.get(auto=configurazione)
    if preventivo_esistente:
        flash('È già stato richiesto un preventivo per questa configurazione', 'error')
        return redirect(url_for('areaRiservataCliente'))
    
    cliente_email = session[app.config['CLIENT_SESSION_KEY']]
    cliente = cliente_class.get(email=cliente_email)
    if not cliente:
        flash('Utente non trovato', 'error')
        return redirect(url_for('areaRiservataCliente'))
       
    targa = request.form.get('targa')
    foto_files = request.files.getlist('foto')
    
    allowed_extensions = {'png', 'jpg', 'jpeg'}

    # controlli campi usato
    if len(foto_files) > 1:
        for file in foto_files:
            if file.filename.split('.')[-1].lower() not in allowed_extensions:
                flash('Si prega di inserire solo foto in formato png, jpg o jpeg.')
                return redirect(url_for('areaRiservataCliente'))

    if targa and len(foto_files) > 0 and len(foto_files) < 4:
        flash('Inserire almeno 4 foto')
        return redirect(url_for('areaRiservataCliente'))
    
    elif len(foto_files) > 1 and not targa:
        flash('Inserire la targa')
        return redirect(url_for('areaRiservataCliente'))
    
    elif targa and foto_files:
        auto_esistente = autoUsata_class.get(targa=targa)
        if auto_esistente:
            flash('Quest\'automobile è già stata utilizzata', 'error')
            return redirect(url_for('areaRiservataCliente'))
        
        # Seleziona un gestore casuale dal database
        gestori = list(select(g for g in impiegato_class))
        if not gestori:
            flash('Nessun gestore disponibile', 'error')
            return redirect(url_for('areaRiservataCliente'))
        gestore_casuale = random.choice(gestori)
    
        auto_usata = autoUsata_class(targa=targa, proprietario=cliente, valutatore=gestore_casuale.matricola)
        db.commit()
    
        # Salva le foto dell'auto usato se presenti
        for file in foto_files:
            foto_data = file.read()
            foto_usato = fotoUsato_class(codice=str(uuid.uuid4()), targaUsato=auto_usata, file=foto_data)
            db.commit()
        
        # preventivo con usato
        preventivo = preventivo_class(
            codice=str(uuid.uuid4()),
            data=datetime.now(),
            auto=configurazione,
            cliente=cliente,
            prezzo=0,
            auto_rottamata=auto_usata
        )
        db.commit()
        
    else:
        # preventivo senza usato
        preventivo = preventivo_class(
            codice=str(uuid.uuid4()),
            data=datetime.now(),
            auto=configurazione,
            cliente=cliente,
            prezzo=0,
            auto_rottamata=None
        )
        db.commit()
        
    flash('Preventivo richiesto con successo', 'success')
    return redirect(url_for('areaRiservataCliente'))

############################################################################  CONFERMA PREVENTIVI ###########################################################################################
# Route che gestisce la conferma del preventivo e quindi la generazione dell'ordine da parte del cliente. Il cliente viene recuperato dalla sessione, mentre il codice
# del preventivo, la sede e il bollettino vengono passati dal form html. Si controlla il corretto inserimento dei campi nel form e se è già stato richiesto un ordine
# per quel preventivo. Vengono recuperate tutte le informazioni per costruire l'oggetto ordine, tra cui il calcolo automatico della consegna.
@app.route('/conferma_preventivo/<cod_preventivo>', methods=['POST'])
@db_session
def conferma_preventivo(cod_preventivo):
    cliente_email = session.get(app.config['CLIENT_SESSION_KEY'])
    if not cliente_email:
        flash('Sessione cliente non trovata', 'error')
        return redirect(url_for('login'))  # o altra pagina di accesso

    cliente = cliente_class.get(email=cliente_email)
    if not cliente:
        flash('Utente non trovato', 'error')
        return redirect(url_for('areaRiservataCliente'))

    preventivo = preventivo_class.get(codice=cod_preventivo)
    if not preventivo:
        flash('Preventivo non trovato', 'error')
        return redirect(url_for('areaRiservataCliente'))

    sede = request.form.get('sceltaSede')
    pagamento_files = request.files.getlist('attestato')
    
    allowed_extensions = {'pdf'}
    for file in pagamento_files:
        if file.filename.split('.')[-1].lower() not in allowed_extensions:
            flash('Si prega di inserire un file pdf')
            return redirect(url_for('areaRiservataCliente'))
    
    if not sede or len(pagamento_files) != 1:
        if len(pagamento_files) > 1:
            flash('Inserire un solo documento', 'error')
            return redirect(url_for('areaRiservataCliente'))
        flash('Si prega di compilare tutti i campi', 'error')
        return redirect(url_for('areaRiservataCliente'))
    
    ordine_esistente = ordine_class.get(preventivo=preventivo)
    if ordine_esistente:
        flash('È già stato richiesto un ordine per questo preventivo', 'error')
        return redirect(url_for('areaRiservataCliente'))

    pagamento_file = pagamento_files[0]
    bollettino = pagamento_file.read()  # Legge il contenuto del file
    
    modello = preventivo.auto.modello
    
    # si contano gli optional relativi alla configurazione del preventivo per calcolare la data di consegna
    optional_modelli = select(so for so in sceltaOptional_class if so.auto == preventivo.auto)
    optionals_count = optional_modelli.count()
    oggettoSede = sede_class.get(nome=sede)

    data_consegna = date.today() + timedelta(days=30 + optionals_count * 10)

    # Seleziona un gestore casuale dal database
    gestori = list(select(g for g in impiegato_class))
    if not gestori:
        flash('Nessun gestore disponibile', 'error')
        return redirect(url_for('areaRiservataCliente'))
    gestore_casuale = random.choice(gestori)

    ordine = ordine_class(
        codice=str(uuid.uuid4().hex)[:5],    # Stringa casuale lunga 5 (più bella esteticamente per la visualizzazione)
        data_ordine=date.today(),
        data_consegna=data_consegna,
        preventivo=preventivo,
        sede_ritiro=oggettoSede,
        gestore_ordine=gestore_casuale.matricola,  
        bollettino=bollettino
    )
    db.commit()

    flash(f'Ordine avvenuto con successo. La data di consegna prevista è il {ordine.data_consegna.strftime("%d/%m/%Y")}')
    return redirect(url_for('areaRiservataCliente'))


# Route per la generazione di file PDF grazie alla libreria reportLab. Prima estrare il preventivo dal database grazie codice dato in input. Estrae anche le altre 
# informazioni utili alla creazione dell'oggetto ordine.
@app.route('/download_preventivo/<cod_preventivo>', methods=['GET'])
@db_session
def download_preventivo(cod_preventivo):
    preventivo = preventivo_class.get(codice=cod_preventivo)
    if not preventivo:
        flash('Preventivo non trovato', 'error')
        return redirect(url_for('areaRiservataCliente'))

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    style_normal = styles['Normal']
    style_heading = styles['Heading1']
    
    style_optional = ParagraphStyle(
        name='Optional',
        parent=style_normal,
        leftIndent=20,
        bulletText='-',
        fontSize=14,  
        spaceAfter=12,  
    )

    style_big = ParagraphStyle(
        name='Big',
        parent=style_normal,
        fontSize=14,  
        spaceAfter=12,  
    )

    content = []

    static_folder = os.path.join(app.root_path, 'static')  
    logo_no_nome_path = os.path.join(static_folder, 'css', 'macchina_senzasfondo.png')
    nome_logo_path = os.path.join(static_folder, 'css', 'nomeLogo.png')

    if os.path.exists(logo_no_nome_path):
        logo_no_nome_img = Image(logo_no_nome_path, width=100, height=75)
        content.append(logo_no_nome_img)

    if os.path.exists(nome_logo_path):
        nome_logo_img = Image(nome_logo_path, width=200, height=50)
        content.append(nome_logo_img)

    # Recupero dati da inserire nel PDF
    colori_modelli = select(cm for cm in coloreModello_class if cm.modello == preventivo.auto.modello and cm.colore == preventivo.auto.colore)[:]
    coloreModello = coloreModello_class.get(id = colori_modelli[0].id)
    motori_modelli = select(mm for mm in motoreModello_class if mm.modello == preventivo.auto.modello and mm.motore == preventivo.auto.motore)[:]
    motoreModello = motoreModello_class.get(id = motori_modelli[0].id)
    optional_scelti = select(os for os in sceltaOptional_class if os.auto == preventivo.auto)[:]
    print(optional_scelti)
    # Inserimento nel PDF dei dati
    content.append(Paragraph(f"<br /><br /><b>Preventivo #{preventivo.codice}</b>", style_heading))
    content.append(Paragraph(f"<br /><b>Cliente:</b> {preventivo.cliente.name} {preventivo.cliente.surname}", style_big))
    content.append(Paragraph(f"<b>Modello:</b> {preventivo.auto.modello.nome} + {preventivo.auto.modello.prezzo_base} €", style_big))
    content.append(Paragraph(f"<b>Colore:</b> {coloreModello.colore.nome} + {coloreModello.prezzo} €", style_big))
    content.append(Paragraph(f"<b>Motore:</b> {motoreModello.motore.alimentazione} + {motoreModello.prezzo} €", style_big))
    ''' 
    for optional in optional_scelti:
        prezzo = select(o.prezzo for o in optionalModello_class if o.optional.nome == optional.optional.nome)
        content.append(Paragraph(f"<b>Optional:</b> {optional.optional.nome} + {prezzo} €", style_optional))
    '''
    for optional in optional_scelti:
        op = select(o for o in optionalModello_class if o.optional.nome == optional.optional.nome and o.modello.nome == optional.auto.modello.nome) [:]
        print('op:', op)
        for o in op:
            content.append(Paragraph(f"<b>Optional:</b> {o.optional.nome} + {o.prezzo} €", style_optional))
        
    if preventivo.valore_sconto:
        content.append(Paragraph(f"<b>Sconto:</b> {preventivo.sconto_mese.codice} - {preventivo.valore_sconto} €", style_big))
        
    if preventivo.valore_sconto_rottamazione:
        content.append(Paragraph(f"<b>Sconto rottamazione:</b> {preventivo.auto_rottamata.targa} - {preventivo.valore_sconto_rottamazione} €", style_big))

    content.append(Paragraph(f"<br /><b>Prezzo Totale:</b> {preventivo.prezzo} €", style_heading))

    doc.build(content)
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=f"Preventivo_{preventivo.codice}.pdf", mimetype='application/pdf')

# Percorso assoluto della cartella statica (la stessa di app.py)
static_folder = os.path.dirname(os.path.abspath(__file__))

# Route per la visualizzazione del PDF
@app.route('/pdf/<nome_file>')
def mostra_pdf(nome_file):
    # Invia il file PDF dalla cartella 
    return send_from_directory(static_folder, nome_file)


if __name__ == '__main__':
    app.run(debug=True)