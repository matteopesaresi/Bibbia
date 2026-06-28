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