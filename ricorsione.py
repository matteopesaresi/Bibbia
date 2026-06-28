import copy


class Model:
    def __init__(self):
        # ...
        self.best_cammino = []
        self.best_score = 0  # O 999999 se devi cercare il minimo

    def cerca_cammino_ottimo(self, partenza, arrivo):
        self.best_cammino = []
        self.best_score = 0

        parziale = [partenza]  # Il cammino inizia sempre dal nodo di partenza

        # Facciamo partire la ricorsione
        self._ricorsione(parziale, arrivo)

        return self.best_cammino, self.best_score

    def _ricorsione(self, parziale, arrivo):
        ultimo_nodo = parziale[-1]

        # 1. CONDIZIONE DI TERMINAZIONE (Es: siamo arrivati a destinazione)
        if ultimo_nodo == arrivo:
            # Calcoliamo lo score del cammino attuale
            score_attuale = self.calcola_score_cammino(parziale)

            # 2. VALUTAZIONE DEL RECORD
            if score_attuale > self.best_score:
                self.best_score = score_attuale
                self.best_cammino = copy.deepcopy(parziale)  # IMPORTANTE: DEEPCOPY!
            return  # Ferma l'esplorazione di questo ramo se sei arrivato

        # 3. ESPLORAZIONE DEI VICINI (Continuo a camminare)
        for vicino in self._graph.neighbors(ultimo_nodo):

            # FILTRO: Evitiamo di ripassare dove siamo già stati
            if vicino not in parziale:
                # FAI LA MOSSA
                parziale.append(vicino)

                # RICORSIONE (Lanciati nel livello successivo)
                self._ricorsione(parziale, arrivo)

                # DISFA LA MOSSA (Backtracking fondamentale!)
                parziale.pop()

    # Funzione di supporto per calcolare lo score totale di una lista di nodi
    def calcola_score_cammino(self, cammino):
        score = 0
        for i in range(len(cammino) - 1):
            nodo_A = cammino[i]
            nodo_B = cammino[i + 1]
            # Recupera il peso dell'arco tra A e B
            peso_arco = self._graph[nodo_A][nodo_B]['weight']
            score += peso_arco
        return score


#CONTROLLER
# 1. Recupero gli oggetti nodo dalle tendine
nodo_partenza = self._view._ddPartenza.value
nodo_arrivo = self._view._ddArrivo.value

# Controllo di sicurezza
if nodo_partenza is None or nodo_arrivo is None:
    self._view.txt_result.controls.append(ft.Text("Errore: Seleziona sia la partenza che l'arrivo!", color="red"))
    self._view.update_page()
    return

# (Opzionale ma utile) Pulisci i risultati precedenti prima di stampare quelli nuovi
self._view.txt_result.controls.clear()
self._view.txt_result.controls.append(
    ft.Text("Calcolo del percorso ottimale in corso... (potrebbe richiedere qualche secondo)"))
self._view.update_page()  # Aggiorna la schermata per mostrare il messaggio di attesa

# 2. Lanciamo la ricorsione!
# La funzione restituisce la tupla: (lista_del_percorso, punteggio_record)
cammino_ottimo, punteggio_max = self._model.cerca_cammino_ottimo(nodo_partenza, nodo_arrivo)

# 3. Analizziamo e stampiamo i risultati
if len(cammino_ottimo) == 0:
    self._view.txt_result.controls.append(
        ft.Text("Nessun cammino valido trovato tra questi due nodi.", color="red")
    )
else:
    self._view.txt_result.controls.append(
        ft.Text(f"Cammino Ottimo trovato!\nPunteggio totale (peso massimo): {punteggio_max}", color="green",
                weight="bold")
    )

    self._view.txt_result.controls.append(
        ft.Text(f"Il percorso è composto da {len(cammino_ottimo)} nodi:")
    )

    # Stampiamo ogni nodo del percorso, andando a capo
    for nodo in cammino_ottimo:
        self._view.txt_result.controls.append(ft.Text(f"- {nodo.Name}"))

    # (Metodo alternativo più compatto usando le freccette)
    # nomi_nodi = [nodo.Name for nodo in cammino_ottimo]
    # self._view.txt_result.controls.append(ft.Text(" -> ".join(nomi_nodi)))

self._view.update_page()




# =========================================================================
# FUNZIONE DI SUPPORTO UTILE PER TUTTE LE RICORSIONI (METTERE NEL MODEL)
# =========================================================================
# Obiettivo: Calcola la somma dei pesi degli archi di un determinato percorso.
# (Presuppone che il grafo sia già stato creato e che gli archi abbiano l'attributo 'weight')
def calcola_score_cammino(self, cammino):
    score = 0
    for i in range(len(cammino) - 1):
        nodo_A = cammino[i]
        nodo_B = cammino[i + 1]
        peso_arco = self._graph[nodo_A][nodo_B]['weight']
        score += peso_arco
    return score


# =========================================================================
# 1. IL CLASSICO: CAMMINO DI PESO MASSIMO (TRA A E B)
# =========================================================================
# Obiettivo: Trovare il percorso tra due artisti scelti (Partenza e Arrivo)
# che massimizza il punteggio totale (la somma dei pesi degli archi attraversati).

# ----------------- DA METTERE NEL MODEL -----------------
def get_cammino_peso_massimo(self, partenza, arrivo):
    self.best_cammino = []
    self.best_score = 0
    self._ric_peso_max([partenza], arrivo)
    return self.best_cammino, self.best_score


def _ric_peso_max(self, parziale, arrivo):
    ultimo = parziale[-1]

    # Terminazione: siamo arrivati a destinazione?
    if ultimo == arrivo:
        score = self.calcola_score_cammino(parziale)
        if score > self.best_score:
            self.best_score = score
            self.best_cammino = copy.deepcopy(parziale)
        return

        # Esplorazione
    for vicino in self._graph.neighbors(ultimo):
        if vicino not in parziale:
            parziale.append(vicino)
            self._ric_peso_max(parziale, arrivo)
            parziale.pop()

        # --------------- DA METTERE NEL CONTROLLER ---------------


def handle_ricorsione_1(self, e):
    nodo_partenza = self._view._ddPartenza.value
    nodo_arrivo = self._view._ddArrivo.value

    if nodo_partenza is None or nodo_arrivo is None:
        self._view.txt_result.controls.append(ft.Text("Seleziona partenza e arrivo!", color="red"))
        self._view.update_page()
        return

    self._view.txt_result.controls.clear()
    cammino, score = self._model.get_cammino_peso_massimo(nodo_partenza, nodo_arrivo)

    if len(cammino) == 0:
        self._view.txt_result.controls.append(ft.Text("Nessun percorso trovato."))
    else:
        self._view.txt_result.controls.append(ft.Text(f"Trovato! Peso massimo totale: {score}", weight="bold"))
        for n in cammino:
            self._view.txt_result.controls.append(ft.Text(f"-> {n.Name}"))
    self._view.update_page()


# =========================================================================
# 2. IL SENZA META: CAMMINO PIU' LUNGO CON VINCOLO CRESCENTE / # VINCOLO DECRESCENTE
# =========================================================================
# Obiettivo: Esplorare partendo da un nodo e trovare la catena più lunga
# (maggior numero di artisti).
# Vincolo: ci si può spostare solo se l'arco successivo ha un peso STRETTAMENTE MAGGIORE
# di quello dell'arco appena percorso.

# ----------------- DA METTERE NEL MODEL -----------------
def get_cammino_lungo_crescente(self, partenza):
    self.best_cammino = []
    self.best_score = 0
    self._ric_lungo_cresc([partenza])
    return self.best_cammino, self.best_score


def _ric_lungo_cresc(self, parziale):
    # Valutazione continua (non c'è destinazione fissa, ci fermiamo quando ci blocchiamo)
    if len(parziale) > self.best_score:
        self.best_score = len(parziale)
        self.best_cammino = copy.deepcopy(parziale)

    ultimo = parziale[-1]

    for vicino in self._graph.neighbors(ultimo):
        if vicino not in parziale:
            if len(parziale) == 1:
                parziale.append(vicino)
                self._ric_lungo_cresc(parziale)
                parziale.pop()
            else:
                penultimo = parziale[-2]
                peso_precedente = self._graph[penultimo][ultimo]['weight']
                peso_nuovo = self._graph[ultimo][vicino]['weight']

                if peso_nuovo > peso_precedente:  # VINCOLO CRESCENTE cambia se vuoi # VINCOLO DECRESCENTE
                    parziale.append(vicino)
                    self._ric_lungo_cresc(parziale)
                    parziale.pop()


# --------------- DA METTERE NEL CONTROLLER ---------------
def handle_ricorsione_2(self, e):
    nodo_partenza = self._view._ddPartenza.value

    if nodo_partenza is None:
        self._view.txt_result.controls.append(ft.Text("Seleziona il nodo di partenza!", color="red"))
        self._view.update_page()
        return

    self._view.txt_result.controls.clear()
    cammino, lunghezza = self._model.get_cammino_lungo_crescente(nodo_partenza)

    self._view.txt_result.controls.append(
        ft.Text(f"Cammino record trovato! E' lungo {lunghezza} nodi.", weight="bold")
    )
    for n in cammino:
        self._view.txt_result.controls.append(ft.Text(f"-> {n.Name}"))
    self._view.update_page()


# =========================================================================
# 3. IL "TARGET FISSO": CAMMINO DI LUNGHEZZA ESATTA N
# =========================================================================
# Obiettivo: Partendo da un artista, trovare il percorso formato esattamente da
# N artisti che ha il punteggio totale (somma pesi) più alto.

# ----------------- DA METTERE NEL MODEL -----------------
def get_cammino_lunghezza_N(self, partenza, N):
    self.best_cammino = []
    self.best_score = 0
    self._ric_lunghezza_fissa([partenza], N)
    return self.best_cammino, self.best_score


def _ric_lunghezza_fissa(self, parziale, N):
    # Terminazione esatta a N nodi
    if len(parziale) == N:
        score = self.calcola_score_cammino(parziale)
        if score > self.best_score:
            self.best_score = score
            self.best_cammino = copy.deepcopy(parziale)
        return

    ultimo = parziale[-1]

    for vicino in self._graph.neighbors(ultimo):
        if vicino not in parziale:
            parziale.append(vicino)
            self._ric_lunghezza_fissa(parziale, N)
            parziale.pop()


# --------------- DA METTERE NEL CONTROLLER ---------------
def handle_ricorsione_3(self, e):
    nodo_partenza = self._view._ddPartenza.value
    valore_n_str = self._view.txt_lunghezza_N.value

    if nodo_partenza is None or not valore_n_str:
        self._view.txt_result.controls.append(ft.Text("Inserisci partenza e lunghezza N!", color="red"))
        self._view.update_page()
        return

    N = int(valore_n_str)
    self._view.txt_result.controls.clear()

    cammino, score = self._model.get_cammino_lunghezza_N(nodo_partenza, N)

    if len(cammino) == 0:
        self._view.txt_result.controls.append(ft.Text(f"Impossibile trovare un cammino di esattamente {N} nodi."))
    else:
        self._view.txt_result.controls.append(
            ft.Text(f"Ottimo trovato (lunghezza {N})! Punteggio: {score}", weight="bold")
        )
        for n in cammino:
            self._view.txt_result.controls.append(ft.Text(f"-> {n.Name}"))
    self._view.update_page()


# =========================================================================
# 4. L'ECCEZIONE: RICERCA DI UN CICLO
# =========================================================================
# Obiettivo: Partire da un artista, farsi un giro nella rete esplorando almeno
# 4 nodi e ritornare ESATTAMENTE al punto di partenza massimizzando la somma dei pesi.

# ----------------- DA METTERE NEL MODEL -----------------
def cerca_ciclo_massimo(self, partenza):
    self.best_cammino = []
    self.best_score = 0
    self._ric_ciclo([partenza], partenza)
    return self.best_cammino, self.best_score


def _ric_ciclo(self, parziale, partenza):
    ultimo = parziale[-1]

    # Terminazione: siamo tornati e abbiamo fatto un giro largo (>3 nodi)
    if ultimo == partenza and len(parziale) > 3:
        score = self.calcola_score_cammino(parziale)
        if score > self.best_score:
            self.best_score = score
            self.best_cammino = copy.deepcopy(parziale)
        return

    for vicino in self._graph.neighbors(ultimo):
        # Condizione speciale per chiudere il ciclo: posso visitare il vicino SE non ci sono mai stato
        # OPPURE SE è proprio la partenza e sto cercando di chiudere il giro
        if vicino not in parziale or (vicino == partenza and len(parziale) > 2):
            parziale.append(vicino)
            self._ric_ciclo(parziale, partenza)
            parziale.pop()


# --------------- DA METTERE NEL CONTROLLER ---------------
def handle_ricorsione_4(self, e):
    nodo_partenza = self._view._ddPartenza.value

    if nodo_partenza is None:
        self._view.txt_result.controls.append(ft.Text("Seleziona il nodo da cui far partire il ciclo!", color="red"))
        self._view.update_page()
        return

    self._view.txt_result.controls.clear()
    cammino, score = self._model.cerca_ciclo_massimo(nodo_partenza)

    if len(cammino) == 0:
        self._view.txt_result.controls.append(
            ft.Text(f"Non esiste nessun ciclo utile partendo da {nodo_partenza.Name}."))
    else:
        self._view.txt_result.controls.append(
            ft.Text(f"Ciclo trovato! Punteggio totale: {score}", weight="bold")
        )
        for n in cammino:
            self._view.txt_result.controls.append(ft.Text(f"-> {n.Name}"))
    self._view.update_page()

    # =========================================================================
    # 5. IL BUDGET (Problema dello Zaino)
    # =========================================================================
    # Obiettivo: Partendo da un artista, visitare il MAGGIOR NUMERO DI NODI possibile
    # (la catena più lunga), ma la SOMMA DEI PESI (le vendite) non deve MAI superare
    # un certo Budget Massimo imposto dall'utente.

    # ----------------- DA METTERE NEL MODEL -----------------
    def get_cammino_con_budget(self, partenza, budget_max):
        self.best_cammino = []
        self.best_score = 0  # In questo caso lo score è il numero di nodi visitati
        self._ric_budget([partenza], budget_max)
        return self.best_cammino, self.best_score

    def _ric_budget(self, parziale, budget_residuo):
        # Valutazione continua: aggiorno il record se ho visitato più nodi
        if len(parziale) > self.best_score:
            self.best_score = len(parziale)
            self.best_cammino = copy.deepcopy(parziale)

        ultimo = parziale[-1]

        for vicino in self._graph.neighbors(ultimo):
            if vicino not in parziale:
                # Quanto mi costa fare questo salto?
                costo_arco = self._graph[ultimo][vicino]['weight']

                # VINCOLO BUDGET: Ci vado SOLO se mi rimangono abbastanza soldi/spazio
                if costo_arco <= budget_residuo:
                    parziale.append(vicino)
                    # Ricorsione scalando il budget!
                    self._ric_budget(parziale, budget_residuo - costo_arco)
                    parziale.pop()

    # --------------- DA METTERE NEL CONTROLLER ---------------
    def handle_ricorsione_budget(self, e):
        nodo_partenza = self._view._ddPartenza.value
        valore_budget_str = self._view.txt_budget.value  # Campo di testo inserito dall'utente

        if nodo_partenza is None or not valore_budget_str:
            self._view.txt_result.controls.append(ft.Text("Inserisci partenza e budget!", color="red"))
            self._view.update_page()
            return

        budget_max = float(valore_budget_str)  # o int() se il peso è senza virgola
        self._view.txt_result.controls.clear()

        cammino, numero_nodi = self._model.get_cammino_con_budget(nodo_partenza, budget_max)

        if len(cammino) == 0:
            self._view.txt_result.controls.append(ft.Text("Nessun percorso trovato entro il budget."))
        else:
            self._view.txt_result.controls.append(
                ft.Text(f"Trovato! Visitati {numero_nodi} artisti restando nel budget.", weight="bold")
            )
            for n in cammino:
                self._view.txt_result.controls.append(ft.Text(f"-> {n.Name}"))
        self._view.update_page()

    # =========================================================================
    # 6. L'ALTERNANZA (Incompatibilità consecutiva)
    # =========================================================================
    # Obiettivo: Trovare il percorso di peso massimo (partenza libera finché ci si blocca)
    # Vincolo: L'ID dell'artista precedente e successivo devono avere parità DIVERSA
    # (uno Pari e uno Dispari, rigorosamente alternati).

    # ----------------- DA METTERE NEL MODEL -----------------
    def get_cammino_alternato(self, partenza):
        self.best_cammino = []
        self.best_score = 0
        self._ric_alternato([partenza])
        return self.best_cammino, self.best_score

    def _ric_alternato(self, parziale):
        # Valutazione: in questo caso vogliamo massimizzare il peso totale
        score_attuale = self.calcola_score_cammino(parziale)
        if score_attuale > self.best_score:
            self.best_score = score_attuale
            self.best_cammino = copy.deepcopy(parziale)

        ultimo = parziale[-1]

        for vicino in self._graph.neighbors(ultimo):
            if vicino not in parziale:

                # VINCOLO ALTERNANZA: Controllo che le due parità siano DIVERSE
                parita_ultimo = ultimo.ArtistId % 2
                parita_vicino = vicino.ArtistId % 2

                if parita_ultimo != parita_vicino:
                    parziale.append(vicino)
                    self._ric_alternato(parziale)
                    parziale.pop()

    # --------------- DA METTERE NEL CONTROLLER ---------------
    def handle_ricorsione_alternanza(self, e):
        nodo_partenza = self._view._ddPartenza.value

        if nodo_partenza is None:
            self._view.txt_result.controls.append(ft.Text("Seleziona il nodo di partenza!", color="red"))
            self._view.update_page()
            return

        self._view.txt_result.controls.clear()

        cammino, score = self._model.get_cammino_alternato(nodo_partenza)

        if len(cammino) == 0:
            self._view.txt_result.controls.append(ft.Text("Nessun percorso alternato trovato."))
        else:
            self._view.txt_result.controls.append(
                ft.Text(f"Cammino record trovato! Punteggio (peso): {score}", weight="bold")
            )
            for n in cammino:
                # Stampiamo anche l'ID per mostrare l'alternanza Pari/Dispari all'utente
                self._view.txt_result.controls.append(ft.Text(f"-> {n.Name} (ID: {n.ArtistId})"))
        self._view.update_page()

    # =========================================================================
    # 7. I NODI "RADIOATTIVI" (Scartare un'intera categoria)
    # =========================================================================
    # Obiettivo: Andare dalla Partenza all'Arrivo massimizzando i pesi.
    # Vincolo: Il percorso NON DEVE MAI PASSARE per gli artisti il cui nome
    # contiene una certa parola vietata (es. "The" o "Orchestra").

    # ----------------- DA METTERE NEL MODEL -----------------
    def get_cammino_senza_radioattivi(self, partenza, arrivo, parola_vietata):
        self.best_cammino = []
        self.best_score = 0
        self._ric_senza_radioattivi([partenza], arrivo, parola_vietata.lower())
        return self.best_cammino, self.best_score

    def _ric_senza_radioattivi(self, parziale, arrivo, parola_vietata):
        ultimo = parziale[-1]

        if ultimo == arrivo:
            score = self.calcola_score_cammino(parziale)
            if score > self.best_score:
                self.best_score = score
                self.best_cammino = copy.deepcopy(parziale)
            return

        for vicino in self._graph.neighbors(ultimo):
            if vicino not in parziale:

                # VINCOLO RADIOATTIVO: Se il nome del vicino contiene la parola vietata...
                # usiamo 'continue' per ignorarlo e passare direttamente al prossimo vicino!
                if parola_vietata in vicino.Name.lower():
                    continue

                    # Se è "pulito", procediamo normalmente
                parziale.append(vicino)
                self._ric_senza_radioattivi(parziale, arrivo, parola_vietata)
                parziale.pop()

    # --------------- DA METTERE NEL CONTROLLER ---------------
    def handle_ricorsione_radioattivi(self, e):
        nodo_partenza = self._view._ddPartenza.value
        nodo_arrivo = self._view._ddArrivo.value
        parola_vietata = self._view.txt_parola_vietata.value  # Es. l'utente scrive "The"

        if nodo_partenza is None or nodo_arrivo is None or not parola_vietata:
            self._view.txt_result.controls.append(ft.Text("Inserisci partenza, arrivo e parola vietata!", color="red"))
            self._view.update_page()
            return

        self._view.txt_result.controls.clear()

        cammino, score = self._model.get_cammino_senza_radioattivi(nodo_partenza, nodo_arrivo, parola_vietata)

        if len(cammino) == 0:
            self._view.txt_result.controls.append(
                ft.Text(f"Impossibile raggiungere {nodo_arrivo.Name} senza passare per '{parola_vietata}'.",
                        color="red")
            )
        else:
            self._view.txt_result.controls.append(
                ft.Text(f"Cammino sicuro trovato! Punteggio totale: {score}", weight="bold", color="green")
            )
            for n in cammino:
                self._view.txt_result.controls.append(ft.Text(f"-> {n.Name}"))
        self._view.update_page()