from flask import render_template, request, redirect, url_for, flash, session, send_file
from database10.database import *
from pony.orm import *
from datetime import datetime, date
from flask_login import LoginManager, login_user, logout_user

from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user
from pony.orm import db_session

import json
import uuid
import io


def init_admin_routes(app):
    app.config['ADMIN_SESSION_KEY'] = 'admin_user_id'
    
    login_manager_lavoratori = LoginManager()
    login_manager_lavoratori.init_app(app)
    login_manager_lavoratori.login_view = 'loginPersonale'

###################################################################### ACCESSO #################################################################################

    # metodo del pacchetto Flask Login per ricordarsi dell'impiegato o del segretario che ha effettuato l'accesso
    @login_manager_lavoratori.user_loader
    @db_session
    def load_admin_user(matricola):
        return segreteria_class.get(matricola=matricola) or impiegato_class.get(matricola=matricola)

    # Route per la pagina della segreteria e dell'accesso che reindirizzano entrambe a loginSegreteria.html
    @app.route('/admin')
    def amministrazione():
        return render_template('loginSegreteria.html')
    
    @app.route('/homeSegreteria')
    def homeSegreteria():
        return render_template('loginSegreteria.html')

    # funzione per autenticare i dati inseriti dall'impiegato/segretario durante l'accesso. Se i valori sono corretti l'utente viene caricato nella sessione
    # corrente (in modo da ricordarsi sempre chi è il dipendente che ha effettuato l'accesso) e reindirizzato alla route della propria areaRiservata.
    @db_session
    def authenticatePersonale(username, password):
        segreteria = segreteria_class.get(matricola=username)
        impiegato = impiegato_class.get(matricola=username)

        if segreteria and segreteria.pw == password and username.startswith('s'):
            login_user(segreteria)
            session[app.config['ADMIN_SESSION_KEY']] = segreteria.matricola
            return redirect(url_for('segreteria'))
        
        elif impiegato and impiegato.pw == password and username.startswith('i'):
            login_user(impiegato)
            session[app.config['ADMIN_SESSION_KEY']] = impiegato.matricola
            
            flash("Login impiegato effettuato con successo", "success")
            return redirect(url_for('impiegati'))
        else:
            flash("Username o password errata", "error")
            return redirect(url_for('amministrazione'))


    # route che gestisce le richieste di accesso da parte del cliente assicurandosi di autenticare le credenziali inserite.
    @app.route('/loginPersonale', methods=['GET', 'POST'])
    @db_session
    def loginPersonale():
        if request.method == 'POST':
            username = request.form['usrname']
            password = request.form['psw']

            return authenticatePersonale(username, password)

        return render_template('loginSegreteria.html')

    # route che toglie il dipendente corrente dalla sessione ed effettua il logout reindirizzando all'alla pagina dell'amministrazione
    @app.route('/logoutImpiegato')
    def logout_impiegato():
        if app.config['ADMIN_SESSION_KEY'] in session:
            session.pop(app.config['ADMIN_SESSION_KEY'])
        logout_user()
        return redirect(url_for('homeSegreteria'))

###################################################################### SEGRETERIA #################################################################################
    # Funzione che aggiorna a cascata la visibilità degli oggetti delle varie classi:
    #   - modelli associati ai brand
    #   - colori associati ai modelli e ai colori
    #   - optional associati ai modelli e agli optional
    #   - motori asosciati ai modelli e ai motori
    #   - immagini associate ai modelli e ai colori
    
    def visibilityControl():
        with db_session:
            for modello in select(m for m in modello_class):
                if modello.brand.visibility == 'no':
                    modello.visibility = 'no'
            
            for motoreModello in select(mm for mm in motoreModello_class):
                if motoreModello.modello.visibility == 'no' or motoreModello.motore.visibility == 'no':
                    motoreModello.visibility = 'no'

            for coloreModello in select(cm for cm in coloreModello_class):
                if coloreModello.modello.visibility == 'no' or coloreModello.colore.visibility == 'no':
                    coloreModello.visibility = 'no'

            for optionalModello in select(om for om in optionalModello_class):
                if optionalModello.modello.visibility == 'no' or optionalModello.optional.visibility == 'no':
                    optionalModello.visibility = 'no'
            
            for image in select(imm for imm in immagine_class):
                if image.modello.visibility == 'no' or image.colore.visibility == 'no':
                    image.visibility = 'no'
            
            for scontoModello in select(sm for sm in scontoModello_class):
                if scontoModello.modello.visibility == 'no':
                    scontoModello.visibility = 'no'

            db.commit()

    # Route della pagina dedicata dei segretari che estrae e passa al template html i preventivi filtrati e la matricola del segretario dalla sessione e:
    #   - modelli
    #   - colori
    #   - brand
    #   - colori - modelli
    #   - optional
    #   - optional - modelli
    #   - brand
    #   - motori
    #   - motori - modelli
    #   - sconti
    #   - sconti - modelli
    #   - ordini
    #   - sedi
    #   - clienti
    # dal database (opportunamente filtrati)
    @app.route('/segreteria')
    @db_session
    def segreteria():
        # Aggiorna la visibilità degli oggetti
        visibilityControl()
        
        # Recupera e deserializza i preventivi filtrati dalla sessione
        preventivi_filtrati_json = session.pop('preventivi_filtrati', '[]')
        preventivi_filtrati = json.loads(preventivi_filtrati_json)
        
        sconti = sconto_class.select()
        
        modelli_auto = select(m for m in modello_class if m.visibility == 'si' and m.brand.visibility == 'si') [:]
        motori = select(m for m in motore_class if m.visibility == 'si') [:]
        marche_auto = select(m for m in brand_class if m.visibility == 'si') [:]
        optionals = select(o for o in optional_class if o.visibility == 'si') [:]
        colore_auto = select(c for c in colore_class if c.visibility == 'si') [:]
        immagini = select(imm for imm in immagine_class if imm.visibility == 'si') [:]
        
        motoreModello = select(mm for mm in motoreModello_class if mm.visibility == 'si') [:]
        coloreModello = select(cm for cm in coloreModello_class if cm.visibility == 'si') [:]
        optionalModello = select(om for om in optionalModello_class if om.visibility == 'si') [:]
        scontiModello = select(sm for sm in scontoModello_class if sm.visibility == 'si') [:]
        
        matricola = session.get(app.config['ADMIN_SESSION_KEY'])      
        
        ordini = select(o for o in ordine_class if o.gestore_ordine is  None) [:]
        sedi = sede_class.select()
        clienti = cliente_class.select()

        return render_template('segreteria.html', preventivi_filtrati=preventivi_filtrati, clienti=clienti, sedi=sedi, matricola=matricola, modelli_auto=modelli_auto, motori=motori, marche_auto=marche_auto, optionals=optionals, colore_auto=colore_auto, coloreModello=coloreModello, optionalModello=optionalModello, sconti=sconti, scontiModello=scontiModello, immagini=immagini, motoreModello=motoreModello, ordini=ordini)
        
        
# GESTIONE DETTAGLI AUTO: inserimento, assegnamento e cancellazione

    #################### Motore #####################
    # Route che gestisce l'inserimento dei motori. Il segretario sceglie il tipo di alimentazione e viene generato automaticamente un codice univoco.
    # per la creazione dell'oggetto. Il sistema controlla se l'oggetto è già presente nel database prima di crearlo.

    @app.route('/aggiungi_motore', methods=['POST'])
    @db_session
    def aggiungi_motore():
        alimentazione = request.form.get('alimentazione')
        if not alimentazione:
            flash('Inserisci l\'alimentazione del motore', 'danger')
            return redirect(url_for('segreteria'))

        existing_motore = select(m for m in motore_class if (m.alimentazione).lower() == alimentazione.lower()) [:]
        
        if existing_motore:
            flash('Questa alimentazione è già presente nel database', 'danger')
            return redirect(url_for('segreteria'))

        try:
            codice = str(uuid.uuid4().hex)[:10]  # Generazione del codice univoco di 10 caratteri
            motore_class(codice=codice, alimentazione=alimentazione, visibility='si')
            db.commit()
            flash('Motore inserito correttamente', 'success')
        except Exception as e:
            flash(f'Errore durante l\'inserimento del motore: {str(e)}', 'danger')

        return redirect(url_for('segreteria'))

    # Route che gestisce l'eliminazione dei motori. I motori non vengono veramente eliminati dal database ma la loro visibilità al cliente è stata negata
    @app.route('/rimuovi_motore/<codice>', methods=['GET'])
    @db_session
    def rimuovi_motore(codice):
        motore = motore_class.get(codice=codice)
        if not motore:
            flash('Il motore con codice {} non esiste'.format(codice), 'danger')
            return redirect(url_for('segreteria'))

        try:
            motore.visibility = 'no'
            flash('Motore rimosso correttamente', 'success')
            return redirect(url_for('segreteria'))
        except Exception as e:
            flash(f'Errore durante la rimozione del motore: {str(e)}', 'danger')

        return redirect(url_for('segreteria'))

    # Route che gestisce l'assegnamento dei motori ai modelli. Il segretario sceglie il motore e il modello al quale assegnarlo e viene generato automaticamente 
    # un codice univoco per la creazione dell'oggetto. Il sistema controlla se l'assegnamento è già presente nel database prima di crearlo.

    @app.route('/assegna_motore', methods=['POST'])
    @db_session
    def assegna_motore():
        modello = request.form.get('modello')
        motore_codice = request.form.get('motore')
        prezzo = request.form.get('prezzo')
        
        if not modello or not motore_codice or not prezzo:
            flash('Inserire tutti i campi richiesti', 'danger')
            return redirect(url_for('segreteria'))

        try:
            modello_obj = modello_class.get(nome=modello)
            motore_obj = motore_class.get(codice=motore_codice)
            
            if motoreModello_class.exists(modello=modello_obj, motore=motore_obj):
                flash('Il motore è già stato assegnato a questo modello', 'danger')
                return redirect(url_for('segreteria'))
            
            id = str(uuid.uuid4().hex)[:10]  # Generazione del codice univoco di 10 caratteri
            
            motoreModello_class(id=id, modello=modello_obj, motore=motore_obj, prezzo=prezzo, visibility='si')
            db.commit()
            
            flash('Motore assegnato correttamente', 'success')
        except Exception as e:
            flash(f'Errore durante l\'assegnamento del motore: {str(e)}', 'danger')

        return redirect(url_for('segreteria'))
    
    # Route che gestisce l'eliminazione dell'assegnamento motore-modello. L'assegnamento non viene eliminato dal database ma la sua visibilità al cliente viene negata
    @app.route('/elimina_assegnamentoMotore/<string:nome>')
    @db_session
    def elimina_assegnamentoMotore(nome):
        motore = motoreModello_class[nome]
        if motore:
            try:
                motore.visibility = 'no'
                flash('Assegnamento eliminato correttamente', 'success')
                return redirect(url_for('segreteria'))
            except Exception as e:
                flash(f'Errore durante l\'eliminazione dell\'assegnamento: {str(e)}', 'danger')
        else:
            flash('Assegnamento non trovato', 'danger')
        return redirect(url_for('segreteria'))
    
    
    #################### Modello #####################
    # Route che gestisce l'inserimento dei modelli. Il segretario inserisce tutti i dettagli dell'auto e sceglie il brand tra quelli presenti. Il sistema 
    # controlla se l'oggetto è già presente nel database prima di crearlo.
    @app.route('/aggiungi_modello', methods=['POST'])
    @db_session
    def aggiungi_modello():
        nome = request.form.get('nome').lower()
        marca = request.form.get('marca').lower()
        descrizione = request.form.get('descrizione').lower()
        altezza = int(request.form.get('altezza'))
        lunghezza = int(request.form.get('lunghezza'))
        larghezza = int(request.form.get('larghezza'))
        peso = float(request.form.get('peso'))
        bagagliaio = int(request.form.get('bagagliaio'))
        prezzo_base = float(request.form.get('prezzo_base'))
        if not nome or not marca or not altezza or not lunghezza or not larghezza or not peso or not bagagliaio or not prezzo_base or not descrizione:
            flash('Inserisci tutti i campi richiesti')
            return redirect(url_for('segreteria'))
        
        try:
            existing_model = select(m for m in modello_class if (m.nome).lower() == nome.lower()) [:]

            if existing_model:
                flash('Il modello {} è già presente nel database'.format(nome), 'danger')
                return redirect(url_for('segreteria'))
            else:
                modello_class(
                    nome=nome, 
                    brand=marca, 
                    descrizione=descrizione, 
                    altezza=altezza, 
                    lunghezza=lunghezza, 
                    larghezza=larghezza, 
                    peso=peso, 
                    bagagliaio=bagagliaio, 
                    prezzo_base=prezzo_base,
                    visibility = 'si'
                )
                flash('Modello inserito correttamente', 'success')
                return redirect(url_for('segreteria'))
        except Exception as e:
            flash(f'Errore durante l\'inserimento del modello: {str(e)}', 'danger')

        return redirect(url_for('segreteria'))

    # Route che gestisce l'eliminazione dei modelli. Il modello non viene eliminato dal database ma la sua visibilità al cliente viene negata
    @app.route('/rimuovi_modello/<nome>', methods=['GET'])
    @db_session
    def rimuovi_modello(nome):
        modello = modello_class.get(nome=nome)
        
        ordine = select(p for p in preventivo_class if p.auto.modello == modello) [:]
        if ordine:
            flash('Impossibile eliminare il modello. Esistono dei preventivi associati.')
            return redirect(url_for('segreteria'))
        
        if not modello:
            flash('Il modello {} non esiste'.format(nome), 'danger')
            return redirect(url_for('segreteria'))

        try:
            modello.visibility = 'no'
            flash('Modello rimosso correttamente', 'success')
            return redirect(url_for('segreteria'))

        except Exception as e:
            flash(f'Errore durante la rimozione del modello: {str(e)}', 'danger')

        return redirect(url_for('segreteria'))

    #################### Immagini #####################
    # Route che gestisce l'inserimento delle immagini. Il segretario inserisce il codice Url e sceglie la coppia colore-modello dell'immagine.
    @app.route('/aggiungi_immagine', methods=['POST'])
    @db_session
    def aggiungi_immagine():
        codiceURL = request.form.get('codiceURL')
        colore_modello = request.form.get('colore_modello')

        if not colore_modello or not codiceURL:
            flash('Inserisci tutti i campi richiesti')
            return redirect(url_for('segreteria'))
        
        codice = str(uuid.uuid4().hex)[:10]  # Generazione del codice univoco di 10 caratteri

        try:
            modello, colore = colore_modello.split('_')
            colore_obj = colore_class.get(nome=colore)
            modello_obj = modello_class.get(nome=modello)
            immagine_class(codice=codice, codiceURL=codiceURL, colore=colore_obj, modello=modello_obj)
            flash('Immagine inserita  correttamente', 'success')
            return redirect(url_for('segreteria'))

        except Exception as e:
            flash(f'Errore durante l\'inserimento del modello: {str(e)}', 'danger')

        return redirect(url_for('segreteria'))

    # Route che gestisce l'eliminazione delle immagini. L'immagine non viene eliminata dal database ma la sua visibilità al cliente viene negata
    @app.route('/elimina_immagini/<string:cod>')
    @db_session
    def elimina_immagini(cod):
        immagine = immagine_class[cod]
        if immagine:
            try:
                immagine.delete()
                db.commit()
                flash('Immagine eliminata correttamente', 'success')
                return redirect(url_for('segreteria'))
            except Exception as e:
                flash(f'Errore durante l\'eliminazione dell\'immagine: {str(e)}', 'danger')
        else:
            flash('Immagine non trovata', 'danger')
        return redirect(url_for('segreteria'))


    #################### Optional #####################
    # Route che gestisce l'inserimento degli optional. Il segretario inserisce il nome dell'optional e un codice univoco viene generato automaticamente come 
    # identificativo dell'oggetto. Il sistema controlla se l'oggetto è già presente nel database prima di crearlo.
    @app.route('/aggiungi_optional', methods=['POST'])
    @db_session
    def aggiungi_optional():
        nome = str(request.form.get('nome'))
        if not nome:
            flash('Inserisci il nome dell\'optional', 'danger')
            return redirect(url_for('segreteria'))
        
        try:
            existing_optional = select(o for o in optional_class if (o.nome).lower() == nome.lower()) [:]
            if existing_optional:
                flash('L\'optional con questo nome esiste già', 'danger')
                return redirect(url_for('segreteria'))
            optional_class(nome=nome, visibility='si')
            db.commit()
            flash('Optional aggiunto correttamente', 'success')
            return redirect(url_for('segreteria'))
        except Exception as e:
            flash(f'Errore durante l\'aggiunta dell\'optional: {str(e)}', 'danger')

        return redirect(url_for('segreteria'))

    # Route che gestisce l'eliminazione degli optional. L'optional non viene eliminato dal database ma la sua visibilità al cliente viene negata
    @app.route('/rimuovi_optional/<nome>', methods=['GET'])
    @db_session
    def rimuovi_optional(nome):
        optional = optional_class.get(nome=nome)
        if not optional:
            flash('L\'optional {} non esiste'.format(nome), 'danger')
            return redirect(url_for('segreteria'))

        try:
            optional.visibility = 'no'
            flash('Optional rimosso correttamente', 'success')
            return redirect(url_for('segreteria'))
        except Exception as e:
            flash(f'Errore durante la rimozione dell\'optional: {str(e)}', 'danger')

        return redirect(url_for('segreteria'))

    # Route che gestisce l'assegnamento optional-modello. Il segretario sceglie il modello e l'optional e un codice univoco viene generato automaticamente come 
    # identificativo univoco dell'assegnamento. Il sistema controlla se l'assegnamento è già presente nel database prima di crearlo.
    @app.route('/assegna_optional', methods=['POST'])
    @db_session
    def assegna_optional():
        modello = request.form.get('modello')
        optional_nome = request.form.get('optional')
        prezzo = request.form.get('prezzo')
        
        if not modello or not optional_nome or not prezzo:
            flash('Inserire tutti i campi richiesti', 'danger')
            return redirect(url_for('segreteria'))

        try:
            modello_obj = modello_class.get(nome=modello)
            optional_obj = optional_class.get(nome=optional_nome)
            
            if optionalModello_class.exists(modello=modello_obj, optional=optional_obj):
                flash(f'L\'optional "{optional_nome}" è già stato assegnato a questo modello', 'danger')
                return redirect(url_for('segreteria'))
            
            id = str(uuid.uuid4().hex)[:10]  # Generazione del codice univoco di 10 caratteri
            
            optionalModello_class(id=id, modello=modello_obj, optional=optional_obj, prezzo=prezzo, visibility='si')
            db.commit()
            
            flash('Optional assegnato correttamente', 'success')
        except Exception as e:
            flash(f'Errore durante l\'assegnamento dell\'optional: {str(e)}', 'danger')

        return redirect(url_for('segreteria'))

    # Route che gestisce l'eliminazione dell'assegnamento optional-modello. L'assegnamento non viene eliminato dal database ma la sua visibilità al cliente viene negata
    @app.route('/elimina_assegnamentoOptional/<string:optional_nome>')
    @db_session
    def elimina_assegnamentoOptional(optional_nome):
        optional = optionalModello_class[optional_nome]
        if optional:
            try:
                optional.visibility ='no'
                flash('Assegnamento eliminato correttamente', 'success')
                return redirect(url_for('segreteria'))
            except Exception as e:
                flash(f'Errore durante l\'eliminazione dell\'assegnamento: {str(e)}', 'danger')
        else:
            flash('Assegnamento non trovato', 'danger')
        return redirect(url_for('segreteria'))


    #################### Brand #####################
    # Route che gestisce l'inserimento dei brand. Il segretario inserisce il nome del brand. Il sistema controlla se l'oggetto è già presente nel database prima di crearlo.
    @app.route('/aggiungi_brand', methods=['GET', 'POST'])
    @db_session
    def aggiungi_brand():
        if request.method == 'POST':
            nome = request.form.get('nome')
            existing_brand = select(b for b in brand_class if (b.nome).lower() == nome.lower()) [:]
            if existing_brand:
                flash('Questo brand è già stato inserito', 'danger')
                return redirect(url_for('segreteria'))

            if not nome:
                flash('Il nome del brand è obbligatorio', 'danger')
                return redirect(url_for('segreteria'))

            try:
                brand_class(nome=nome, visibility='si')
                flash('Brand aggiunto correttamente', 'success')
                return redirect(url_for('segreteria'))
            except Exception as e:
                flash(f'Errore durante l\'aggiunta del brand: {str(e)}', 'danger')
        return render_template('segreteria.html')

    # Route che gestisce l'eliminazione brand. Il brand non viene eliminato dal database ma la sua visibilità al cliente viene negata
    @app.route('/elimina_brand/<string:brand_nome>')
    @db_session
    def elimina_brand(brand_nome):
        brand = brand_class[brand_nome]
        if brand:
            try:
                brand.visibility = 'no'
                flash('Brand eliminato correttamente', 'success')
                return redirect(url_for('segreteria'))
            except Exception as e:
                flash(f'Errore durante l\'eliminazione del brand: {str(e)}', 'danger')
        else:
            flash('Brand non trovato', 'danger')
        return redirect(url_for('segreteria'))


    #################### Colore #####################
    # Route che gestisce l'inserimento dei colori. Il segretario inserisce il nome del colore. Il sistema controlla se l'oggetto è già presente nel database prima di crearlo.
    @app.route('/aggiungi_colore', methods=['GET', 'POST'])
    def aggiungi_colore():
        if request.method == 'POST':
            nome = request.form.get('nome').lower()
            if nome:
                with db_session():
                    existing_color = select(c for c in colore_class if (c.nome).lower() == nome.lower()) [:]

                    if existing_color:
                        flash('Il colore {} è già presente nel database'.format(nome), 'danger')
                        return redirect(url_for('segreteria'))
                    else:
                        colore_class(nome=nome, visibility='si')
                        flash('Colore aggiunto correttamente', 'success')
                        return redirect(url_for('segreteria'))
            else:
                flash('Il nome del colore è obbligatorio', 'danger')
        return render_template('segreteria.html')

    # Route che gestisce l'eliminazione del colore. Il colore non viene eliminato dal database ma la sua visibilità al cliente viene negata
    @app.route('/elimina_colore/<string:colore_nome>')
    @db_session
    def elimina_colore(colore_nome):
        colore = colore_class[colore_nome]
        
        ordine = select(p for p in preventivo_class if p.auto.colore == colore) [:]
        if ordine:
            flash('Impossibile eliminare il colore. Esistono dei preventivi associati.')
            return redirect(url_for('segreteria'))
        
        if colore:
            try:
                colore.visibility = 'no'
                flash('Colore eliminato correttamente', 'success')
                return redirect(url_for('segreteria'))
            except Exception as e:
                flash(f'Errore durante l\'eliminazione del colore: {str(e)}', 'danger')
        else:
            flash('Colore non trovato', 'danger')
        return redirect(url_for('segreteria'))

    # Route che gestisce l'assegnamento colore-modello. Il segretario sceglie il modello e il colore da assegnare e il sistema genera automaticamente un codice univoco.
    # Il sistema controlla se l'assegnamento è già presente nel database prima di crearlo.
    @app.route('/assegna_colore', methods=['POST'])
    @db_session
    def assegna_colore():
        modello = request.form.get('modello')
        colore_nome = request.form.get('colore')
        prezzo = request.form.get('prezzo')
        
        if not modello or not colore_nome or not prezzo:
            flash('Inserire tutti i campi richiesti', 'danger')
            return redirect(url_for('segreteria'))

        try:
            # Controllo se il colore è già stato assegnato al modello
            modello_obj = modello_class.get(nome=modello)
            colore_obj = colore_class.get(nome=colore_nome)
            
            if coloreModello_class.exists(modello=modello_obj, colore=colore_obj):
                flash(f'Il colore "{colore_nome}" è già stato assegnato a questo modello', 'danger')
                return redirect(url_for('segreteria'))
            
            id = str(uuid.uuid4().hex)[:10] # Generazione del codice univoco di 10 caratteri
            
            coloreModello_class(id=id, modello=modello_obj, colore=colore_obj, prezzo=prezzo, visibility='si')
            db.commit()
            
            flash('Colore assegnato correttamente', 'success')
        except Exception as e:
            flash(f'Errore durante l\'assegnamento del colore: {str(e)}', 'danger')

        return redirect(url_for('segreteria'))
    
    # Route che gestisce l'eliminazione dell'assegnamento colore-modello. L'assegnamento non viene eliminato dal database ma la sua visibilità al cliente viene negata
    @app.route('/elimina_assegnamentoColore/<string:colore_nome>')
    @db_session
    def elimina_assegnamentoColore(colore_nome):
        colore = coloreModello_class[colore_nome]
        if colore:
            try:
                colore.visibility = 'no'
                flash('Assegnamento eliminato correttamente', 'success')
                return redirect(url_for('segreteria'))
            except Exception as e:
                flash(f'Errore durante l\'eliminazione dell\'assegnamento: {str(e)}', 'danger')
        else:
            flash('Assegnamento non trovato', 'danger')
        return redirect(url_for('segreteria'))


    #################### Sconto #####################
    # Funzione chiamata dalla route aggiungi_sconto che controlla che lo sconto inserito sia valido andando a confrontare le date.
    def controllo_sconto(codice, dal, al, percentuale):
        oggi = date.today()
        
        if not codice or not dal or not al or not percentuale:
            return False, 'Inserire tutti i campi'
        elif dal < oggi or al < oggi:
            return False, 'Le date devono essere postume alla data odierna'
        elif al <= dal:
            return False, 'La data di fine sconto deve essere postuma alla data di inizio'

        try:
            dal_date = datetime.strptime(dal, '%Y-%m-%d')
            al_date = datetime.strptime(al, '%Y-%m-%d')
            if dal_date > al_date:
                return False, 'La data di inizio sconto non può essere successiva alla data di fine sconto'
            if dal_date < datetime.now():
                return False, 'La data di inizio sconto non può essere antecedente alla data odierna'
            if int(percentuale) < 1:
                return False, 'Valore dello sconto non accettato'
        except ValueError:
            return False, 'Formato data non valido'

        return True, 'Sconto valido'

    # Route che gestisce l'inserimento degli sconti. Il segretario inserisce il codice, la durata e la percentuale. Il sistema controlla se l'oggetto è già 
    # presente nel database prima di crearlo
    @app.route('/aggiungi_sconto', methods=['GET', 'POST'])
    def aggiungi_sconto():        
        if request.method == 'POST':
            codice = request.form.get('codice')
            dal = request.form.get('dal')
            al = request.form.get('al')
            percentuale = request.form.get('percentuale')
            
            success, msg = controllo_sconto(codice, dal, al, percentuale)
            
            if success:
                with db_session():
                    existing_sconto = sconto_class.get(codice=codice)
                    if existing_sconto:
                        flash('Lo sconto {} è già presente nel database'.format(codice), 'danger')
                        return redirect(url_for('segreteria'))
                    else:
                        sconto_class(codice=codice, dal=dal, al=al, percentuale=percentuale)
                        flash('Sconto aggiunto correttamente', 'success')
                        return redirect(url_for('segreteria'))
            else:
                flash(msg, 'danger')
        return render_template('segreteria.html')

    # Route che gestisce l'eliminazione dello sconto dal database
    @app.route('/elimina_sconto/<string:codice>')
    @db_session
    def elimina_sconto(codice):
        sconto = sconto_class[codice]
        if sconto:
            try:
                sconto.delete()
                db.commit()
                flash('Sconto eliminato correttamente', 'success')
                return redirect(url_for('segreteria'))
            except Exception as e:
                flash(f'Errore durante l\'eliminazione dello sconto: {str(e)}', 'danger')
        else:
            flash('Sconto non trovato', 'danger')
        return redirect(url_for('segreteria'))

    # Route che gestisce l'assegnamento sconto-modello. Il segretario sceglie il modello e lo sconto e il sistema genera automaticamente un codice identificativo univoco.
    # Il sistema controlla se l'assegnamento è già presente nel database prima di crearlo.
    @app.route('/assegna_sconto', methods=['POST'])
    @db_session
    def assegna_sconto():
        modello = request.form.get('modello')
        sconto_codice = request.form.get('sconto')
        
        if not modello or not sconto_codice:
            flash('Inserire tutti i campi richiesti', 'danger')
            return redirect(url_for('segreteria'))

        try:
            modello_obj = modello_class.get(nome=modello)
            sconto_obj = sconto_class.get(codice=sconto_codice)
            
            if scontoModello_class.exists(modello=modello_obj, sconto=sconto_obj):
                flash(f'Lo sconto "{sconto_codice}" è già stato assegnato a questo modello', 'danger')
                return redirect(url_for('segreteria'))
            
            id = str(uuid.uuid4().hex)[:10] 
            
            scontoModello_class(id=id, modello=modello_obj, sconto=sconto_obj)
            db.commit()
            
            flash('Sconto assegnato correttamente', 'success')
        except Exception as e:
            flash(f'Errore durante l\'assegnamento dello sconto: {str(e)}', 'danger')

        return redirect(url_for('segreteria'))

    # Route che elimina dal database l'assegnamento sconto-modello
    @app.route('/elimina_assegnamentoSconto/<string:codice>')
    @db_session
    def elimina_assegnamentoSconto(codice):
        sconto = scontoModello_class[codice]
        if sconto:
            try:
                sconto.delete()
                db.commit()
                flash('Assegnamento eliminato correttamente', 'success')
                return redirect(url_for('segreteria'))
            except Exception as e:
                flash(f'Errore durante l\'eliminazione dell\'assegnamento: {str(e)}', 'danger')
        else:
            flash('Assegnamento non trovato', 'danger')
        return redirect(url_for('segreteria'))


    # VISUALIZZAZIONE DEI PREVENTIVI (ORDINI) FILTRANDO CLIENTE, SEDE E BRAND
    # Route che gestisce il filtraggio degli ordini sulla base delle scelte del segretario, il quale può filtrare gli ordini per brand, cliente e/o sede. Il sistema 
    # estrae dal database gli ordini relativi alle scelte e crea un lista di dizionari che viene salvata nella sessione. Reindirizza alla route degli ordini.
    @app.route('/visualizza_ordini', methods=['GET', 'POST'])
    @db_session
    def visualizza_ordini():
        sede = request.form.get('sede') or request.args.get('sede')
        cliente = request.form.get('cliente') or request.args.get('cliente')
        brand_auto = request.form.get('brand_auto') or request.args.get('brand_auto')
        
        if sede:
            sede_obj = sede_class.get(nome=sede)
        else:
            sede_obj = None
        if cliente:
            cliente_obj = cliente_class.get(email=cliente)
        else:
            cliente_obj = None
        if brand_auto:
            brand_obj = brand_class.get(nome=brand_auto)
        else:
            brand_obj = None

        query = select(o for o in ordine_class if
                    (not sede_obj or o.sede_ritiro == sede_obj) and
                    (not cliente_obj or o.preventivo.cliente == cliente_obj) and
                    (not brand_obj or o.preventivo.auto.modello.brand == brand_obj))

        preventivi_filtrati = list(query)  # Converte il risultato in una lista di oggetti dell classe ordine

        # Converte preventivi_filtrati in una lista di dizionari JSON serializzabili
        preventivi_serializzabili = []
        for ordine in preventivi_filtrati:
            preventivo_dict = {
                'codice': ordine.codice,
                'sede_ritiro': ordine.sede_ritiro.nome,
                'cliente_email': ordine.preventivo.cliente.email,
                'brand_auto': ordine.preventivo.auto.modello.brand.nome
            }
            preventivi_serializzabili.append(preventivo_dict)

        # preventivi_serializzabili serializzati in JSON e memorizzati nella sessione
        session['preventivi_filtrati'] = json.dumps(preventivi_serializzabili)

        return redirect(url_for('pagina_ordini'))
    
    # Route che visualizza le informazioni relative alla pagina nella quale la segreteria può filtrare gli ordini per brand, cliente e/o sede. Estrae dalla sessione
    # i preventivi filtrati e li passa alla pagina html degli ordini.
    @app.route('/pagina_ordini')
    @db_session
    def pagina_ordini():
        # Recupera e deserializza i preventivi filtrati dalla sessione
        preventivi_filtrati_json = session.pop('preventivi_filtrati', '[]')
        preventivi_filtrati = json.loads(preventivi_filtrati_json)
        
        ordini = select(o for o in ordine_class if o.gestore_ordine is  None) [:]
        sedi = sede_class.select()
        clienti = cliente_class.select()
        marche_auto = brand_class.select().order_by(brand_class.nome)

        matricola = session.get(app.config['ADMIN_SESSION_KEY'])      
        
        return render_template('ordini.html', preventivi_filtrati=preventivi_filtrati, ordini=ordini, sedi=sedi, clienti=clienti, marche_auto=marche_auto, matricola=matricola)
    
    
###################################################################### IMPIEGATI #################################################################################
    # Route che gestisce l'area riservata degli impiegati. Estra la matricola dell'impiegato dal database e oggetti come preventivi con e senza usato, ordini gestiti,
    # ordini totali e ordini consegnati.
    @app.route('/impiegati')
    @db_session
    def impiegati():
        preventivi = preventivo_class.select()
        matricola = session.get(app.config['ADMIN_SESSION_KEY'])   
        preventiviUsato = select(p for p in preventivo_class if p.auto_rottamata.valutatore.matricola == matricola)[:]
        ordini = ordine_class.select()
        ordiniImpiegato = select(o for o in ordine_class if o.gestore_ordine.matricola == matricola) [:]
        ordiniConsegnati = select(o for o in ordine_class if o.gestore_ordine == None and not exists(m for m in messaggio_class if m.ordine == o))[:]
        fotoUsato = fotoUsato_class.select()

        return render_template('impiegati.html', fotoUsato=fotoUsato, ordiniConsegnati=ordiniConsegnati, matricola=matricola, preventivi=preventivi, preventiviUsato=preventiviUsato, ordini=ordini, ordiniImpiegato=ordiniImpiegato)


# GESTIONE PREVENTIVI e ORDINI

    ################### Assegnamento sconto rottamazione e/o mensile ##############################
    # Route che gestisce la gestione dei preventivi con l'usato. Il sistema cerca, calcola e detrae dal prezzo totale l'eventuale sconto del mese associato al modello
    # e il valore inserito dall'impiegato per la decurtazione dell'usato.
    @app.route('/gestisci_preventivi', methods=['GET', 'POST'])
    @db_session
    def gestisci_preventivi():
        if request.method == 'POST':
            codice = request.form['codice']
            preventivo = preventivo_class.get(codice=codice)
            sconto = request.form['valore_sconto_rottamazione']
            
            if sconto == 'None':
                flash('Si prega di inserire un valore')
                return redirect(url_for('impiegati'))
            elif float(sconto) < 0:
                flash('Si prega di inserire un valore maggiore o uguale a 0')
                return redirect(url_for('impiegati'))
                
            valore_sconto = round(float(sconto))

            # Cerca lo sconto del mese valido
            if preventivo.auto_rottamata and valore_sconto != 0 and not preventivo.valore_sconto_rottamazione and not preventivo.valore_sconto:
                oggi = date.today()
                sconti_modello = scontoModello_class.select(modello=preventivo.auto.modello)
                preventivo.prezzo = preventivo.auto.prezzo_totale
                preventivo.valore_sconto_rottamazione = valore_sconto
                for sconto_modello in sconti_modello:
                    if sconto_modello.sconto.dal <= oggi <= sconto_modello.sconto.al:
                        preventivo.sconto_mese = sconto_modello.sconto
                    
                    # Calcola il prezzo scontato per la visualizzazione
                    if preventivo.sconto_mese:
                            prezzo_scontato = preventivo.prezzo * (preventivo.sconto_mese.percentuale / 100)
                            preventivo.valore_sconto = round(prezzo_scontato, 2)
                            preventivo.prezzo = preventivo.prezzo - preventivo.valore_sconto
            
                preventivo.prezzo = round(preventivo.prezzo - preventivo.valore_sconto_rottamazione, 2)
            elif preventivo.valore_sconto_rottamazione:
                flash('Sconto già assegnato')
                return redirect(url_for('impiegati'))
                
            db.commit()
        
        return redirect(url_for('impiegati'))


    ################### Aggiornamento e conferma data di consegna ##############################
    # Route che gestisce la gestione degli ordini. L'impiegato, per confermare l'ordine, inserisce la data di consegna definitiva. Il sistema controlla la data inserita
    # dall'impiegato e se tutto è corretto rimpiazza la data di consegna dell'ordine e mette il gestore a None (flag per capire che l'ordine è confermato)
    @app.route('/gestisci_ordini', methods=['GET', 'POST'])
    @db_session
    def gestisci_ordini():
        if request.method == 'POST':
            codice = request.form['codice']
            data_consegna_str = request.form['data_consegna']
            ordine = ordine_class.get(codice=codice)
            
            oggi = datetime.now().date()
            
            try:
                data_consegna = datetime.strptime(data_consegna_str, '%Y-%m-%d').date()
            except ValueError:
                flash('Formato della data non valido. Usa il formato YYYY-MM-DD.')
                return redirect(url_for('impiegati'))

            if not data_consegna:
                flash('Inserire la data di consegna per confermare l\'ordine')
                return redirect(url_for('impiegati'))
            elif data_consegna < oggi: 
                flash('La data di consegna deve essere postuma alla data odierna')
                return redirect(url_for('impiegati'))
            else:
                flash('Data di consegna aggiornata con successo')
                ordine.data_consegna = data_consegna
                ordine.gestore_ordine = None
            
            db.commit()
            return redirect(url_for('impiegati'))
        
        
    ################### Invio messaggio automatico x consegna auto ##############################
    # Route che gestisce l'invio di un messaggio automatico sulla pagina riservata del cliente, il quale viene avvisato che la sua auto è pronta per la consegna 
    # presso la sede selezionata.
    @app.route('/invia_messaggio', methods=['POST'])
    @db_session
    def invia_messaggio():
        oggi = date.today()

        codice_ordine = request.form['codice_ordine']
        ordine = ordine_class.get(codice=codice_ordine)
        
        messaggioEsistente = messaggio_class.get(ordine=ordine)
        if messaggioEsistente:
            flash('Il messaggio è già stato inviato')
            return redirect(url_for('impiegati'))
        
        testo = 'L\'ordine \'' + ordine.codice + '\' relativo all\'auto: ' + ordine.preventivo.auto.modello.nome + ' è stato consegnato nella sede ' + ordine.sede_ritiro.nome + ' in data: ' + str(oggi)

        messaggio = messaggio_class(ordine=ordine, testo=testo, lettura='no')
        db.commit()
        
        if messaggio:
            flash('Il messaggio è stato inviato correttamente')
            return redirect(url_for('impiegati'))
    
    
    ################### Visualizzazione documenti inseriti dall'utente ##############################
    # Queste due route permettono la visualizzazione dei documenti inseriti dal cliente (attestato pagamento dell'ordine e foto auto usata) in base all'estensione dei file
    @app.route('/view/<ordine_id>')
    @db_session
    def view_bollettino(ordine_id):
        ordine = ordine_class.get(codice=ordine_id)

        if ordine and ordine.bollettino:
            bollettino_bytes = ordine.bollettino
            return send_file(
                io.BytesIO(bollettino_bytes),
                mimetype='application/pdf',  # include estensione pdf
                as_attachment=False
            )

    @app.route('/view_photo/<foto_id>')
    @db_session
    def view_photo(foto_id):
        foto = fotoUsato_class.get(codice=foto_id)
        if foto and foto.file:
            return send_file(
                io.BytesIO(foto.file),
                mimetype='application/png', # include estensione png, jpg e jpeg
                as_attachment=False
            )
        return "File not found", 404
    
        
    if __name__ == '__main__':
        app.run(debug=True)
