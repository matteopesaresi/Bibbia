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