#DOMANDA:
#Il testo dice:"si scelga l’algoritmo di visita del grafo più opportuno fra visita in ampiezza ed in profondità per visualizzare il cammino più lungo".
#Quale algoritmo scegliere?
#La risposta giusta è la visita in profondità (DFS). Perché? La visita in ampiezza (BFS) esplora il grafo "a cerchi concentrici", trovando sempre i cammini
# più corti (con meno salti). La visita in profondità, invece, viaggia il più lontano possibile prima di tornare indietro quindi l'albero che genera conterrà
# naturalmente dei cammini molto più lunghi!


#-------------------------------------------------------------------
#CAMMINO MAX NON PESATO (algoritmo di visita)
def get_cammino_massimo_non_pesato(self, nodo_partenza):
    """
    Calcola il cammino non pesato più lungo possibile partendo da un nodo specifico,
    senza ripassare per gli stessi nodi (utilizzando l'albero di esplorazione DFS).

    Ritorna: Una lista di nodi [nodo_partenza, nodo_B, nodo_C, ..., nodo_arrivo]
    quando usarlo?
"Trova il cammino più lungo in termini di numero di archi partendo da un nodo"
"Trova la sequenza col maggior numero di nodi raggiungibili usando l'algoritmo di visita in profondità (DFS)"
"Calcola il cammino non pesato di lunghezza massima"

quando nnon usarlo?
"La somma dei pesi degli archi deve essere massima" (Qui contano i pesi, non si può usare l'albero DFS puro).
"Il cammino deve avere una lunghezza esatta pari a Lun" (Qui hai un vincolo di lunghezza imposto dall'utente).
    """

    # 1. Creiamo l'albero di visita in profondità (DFS) partendo dal nodo dato.
    # Questo elimina i cicli (i "giri a vuoto") e ci dà tutte le strade dritte verso i rami più profondi.
    albero_dfs = nx.dfs_tree(self._graph, nodo_partenza)

    # 2. Calcoliamo i percorsi dalla radice (nodo_partenza) verso TUTTI gli altri nodi dell'albero.
    # Visto che ora è un albero senza cicli, shortest_path ci darà semplicemente
    # l'UNICA strada possibile per raggiungere ogni punto esplorato.
    tutti_i_cammini = nx.shortest_path(albero_dfs, nodo_partenza)

    # 3. Prepariamo una lista vuota per salvare il record del percorso più lungo
    cammino_massimo = []

    # 4. Scorriamo tutti i percorsi estratti dal cassetto 'tutti_i_cammini'
    for nodo_arrivo, cammino in tutti_i_cammini.items():

        # Se la lunghezza di questo percorso è maggiore del nostro record attuale...
        if len(cammino) > len(cammino_massimo):
            # ...abbiamo un nuovo record!
            cammino_massimo = cammino

    # Alla fine del ciclo, restituiamo il percorso vincitore
    return cammino_massimo

#Controller
    # (Ovviamente prima recuperi l'id o l'oggetto del nodo di partenza dalla tendina)
nodo_partenza = self._model._idMapNodi.get(id_scelto)

    # Chiami la funzione che ti restituisce la lista
percorso_lungo = self._model.get_cammino_massimo_non_pesato(nodo_partenza)

    # E poi stampi il risultato
print(f"Il cammino più lungo attraversa {len(percorso_lungo)} nodi!")
for nodo in percorso_lungo:
    print(nodo)
#-------------------------------------------------------------------
#CAMMINO MINIMO NON PESATO (meno salti possibili)
def getCamminoMinimo(self, id_partenza, id_arrivo):
    # 1. Recupera gli "oggetti" nodo veri e propri partendo dal loro ID numerico
    nodo_partenza = self._idMap[int(id_partenza)]
    nodo_arrivo = self._idMap[int(id_arrivo)]

    # 2. La magia di NetworkX
    cammino = nx.shortest_path(self._graph, source=nodo_partenza, target=nodo_arrivo)

    return cammino
#-------------------------------------------------------------------
# Cammino MINIMO Pesato (Usa Dijkstra!)
def get_cammino_minimo_costo(self, partenza, arrivo):
    try:
        cammino = nx.dijkstra_path(self._graph, source=partenza, target=arrivo, weight='weight')
        costo_totale = nx.dijkstra_path_length(self._graph, source=partenza, target=arrivo, weight='weight')
        return cammino, costo_totale
    except nx.NetworkXNoPath:
        return [], 0