Nel caso in cui si compri il biglietto (Giornaliero, Pass 2 giorni)
Il campo giorno_riferimento dell'entità biglietto viene impostato, altrimenti non viene impostato.
Ai fini del calcolo del numero di biglietti in un giorno (<= 200), la logica si occuperà
di contare il biglietto "pass 2 giorni" conteggiando a partire dal "giorno_riferimento".

`flask. g ` is a global object provided by Flask which can be used to store data and it will be available throughout the lifespan of a single request.


Commento in navbar.html
Affinché session.get('utente_id') funzioni nei template Jinja2 (come in navbar.html incluso da base.html), non devi passare nulla di particolare:
la variabile session è già disponibile di default nei template Flask, perché Flask la rende accessibile automaticamente.


profili:    Utente | Password
alebellu@gmail.com | PinaSupina
rasca@gmail.com    | PinaSupina

Palette di colori
Sabbia chiara   |#FDF6EC | Sfondo principale (base chiara)
Blu oceano | #2C8C99 | Pulsanti, link, titoli
Corallo acceso | #FF6B6B | Call to action, hover effetti
Giallo sole | #FFD93D | Accenti, badge, bottoni chiari
Arancio tramonto | #FF924C | Elementi decorativi caldi
Indaco profondo | #3D348B | Testi forti, contrasto


Commento in navbar.html
        {% elif utente.ruolo == 'PARTECIPANTE' %}
        <a class="nav-link" href="{{ url_for('profilo') }}">Profilo</a>
        <a class="nav-link" href="{{ url_for('acquista_biglietto') }}">Acquista</a>
        <a class="nav-link" href="{{ url_for('logout') }}">Logout</a>
        {% elif utente.ruolo == 'ORGANIZZATORE' %}
        <a class="nav-link" href="{{ url_for('gestione_performance') }}">Gestione</a>
        <a class="nav-link" href="{{ url_for('nuova_performance') }}">Nuova Performance</a>
        <a class="nav-link" href="{{ url_for('statistiche') }}">Statistiche</a>
        <a class="nav-link" href="{{ url_for('logout') }}">Logout</a>
        -->

Pagina "login.html"

ORGANIZZAZIONE Profili
Profili -> PARTECIPANTE
        - Sulla sinistra un riassunto delle proprie informazioni : 30% viewport
        - Sulla destra la possibilità di acquistare un biglietto : 70% viewport 
        - In basso una sezione con i biglietti acquistati

Profili -> ORGANIZZATORE
3 sezioni:
        - Nella prima sezione un riassunto delle proprie informazioni : 100% viewport
        - Nella seconda sezione una serie di bozze di performance formate da due colonne:
                * La copertina della bozza nella prima colonna;
                * Un form con le informazioni non modificabili nella seconda colonna.
        - Nella terza sezione una serie di bozze di performace formate da due colonne:
                * La copertina della bozza nella prima colonna;
                * Un form con le informazioni modificabili nella seconda colonna.

ORGANIZZAZIONE Home
Simile a questa: https://getbootstrap.com/docs/5.3/examples/album/#
- Prima sezione con una foto del lungomare di Trapani (dove si terrà l'evento) con le date in sovraimpressione
- Seconda sezione con un album di 3 colonne per riga in cui si ha:
        * In ogni colonna una card contenente la tumbnail, qualche info e un pulsante per accedere alle informazioni complete

Modidiche al DB
L'Artista adesso ha il nome unique 