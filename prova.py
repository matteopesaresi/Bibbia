# =========================================================================
# 1. CLASSE CUSTOMER (model/customer.py)
# =========================================================================
from dataclasses import dataclass


@dataclass
class Customer:
    CustomerId: int
    FirstName: str
    LastName: str
    Fatturato: float  # Attributo calcolato dalla query SQL!

    def __hash__(self):
        return hash(self.CustomerId)

    def __eq__(self, other):
        return self.CustomerId == other.CustomerId

    def __str__(self):
        return f"{self.FirstName} {self.LastName}"


# =========================================================================
# 2. DAO (database/DAO.py)
# =========================================================================
# NOTA: Ricordati di importare la tua libreria per la connessione (es. mysql.connector)
# e la classe Customer appena creata.

class DAO:

    @staticmethod
    def get_nodi_clienti(state):
        """
        Estrae i clienti di un certo stato calcolando direttamente la somma
        dei loro acquisti (il fatturato totale) tramite JOIN e GROUP BY.
        """
        # CONNESSIONE DB (Esempio generico)
        # conn = DBConnect.get_connection()
        # cursor = conn.cursor(dictionary=True)

        query = """
            SELECT c.CustomerId, c.FirstName, c.LastName, SUM(i.Total) as Fatturato
            FROM Customer c
            JOIN Invoice i ON c.CustomerId = i.CustomerId
            WHERE c.State = %s
            GROUP BY c.CustomerId
        """
        # cursor.execute(query, (state,))
        # result = []
        # for row in cursor:
        #     # Creiamo l'oggetto Customer passando anche il fatturato calcolato!
        #     result.append(Customer(row["CustomerId"], row["FirstName"], row["LastName"], row["Fatturato"]))
        # return result

    @staticmethod
    def get_artisti_per_cliente(state):
        """
        Restituisce una semplice lista di coppie (CustomerId, ArtistId).
        Usa DISTINCT per sapere se un cliente ha comprato almeno un brano di quell'artista,
        senza contare 10 volte se ha comprato 10 brani dello stesso artista.
        """
        # conn = DBConnect.get_connection()
        # cursor = conn.cursor(dictionary=True)

        query = """
            SELECT DISTINCT c.CustomerId, al.ArtistId
            FROM Customer c
            JOIN Invoice i ON c.CustomerId = i.CustomerId
            JOIN InvoiceLine il ON i.InvoiceId = il.InvoiceId
            JOIN Track t ON il.TrackId = t.TrackId
            JOIN Album al ON t.AlbumId = al.AlbumId
            WHERE c.State = %s
        """
        # cursor.execute(query, (state,))
        # result = []
        # for row in cursor:
        #     result.append((row["CustomerId"], row["ArtistId"]))
        # return result


# =========================================================================
# 3. MODEL (model/model.py)
# =========================================================================
import networkx as nx


class Model:
    def __init__(self):
        # IL TESTO CHIEDE UN GRAFO ORIENTATO! Usiamo DiGraph()
        self._graph = nx.DiGraph()
        self._nodi = []
        self._idMap = {}

    def build_graph(self, stato):
        self._graph.clear()

        # 1. RECUPERO E AGGIUNGO I NODI
        self._nodi = DAO.get_nodi_clienti(stato)
        self._graph.add_nodes_from(self._nodi)

        # idMap per trovare un Customer partendo dal suo ID
        self._idMap = {n.CustomerId: n for n in self._nodi}

        # 2. PREPARO I DATI PER GLI ARCHI (Mappa: id_cliente -> set di artisti)
        artisti_acquistati = DAO.get_artisti_per_cliente(stato)

        # Creo un dizionario dove ad ogni cliente associo un SET (insieme) vuoto
        mappa_artisti = {n.CustomerId: set() for n in self._nodi}

        # Riempio i SET con gli ID degli artisti
        for id_cliente, id_artista in artisti_acquistati:
            if id_cliente in mappa_artisti:
                mappa_artisti[id_cliente].add(id_artista)

        # 3. CREO GLI ARCHI (Doppio ciclo sui nodi)
        for u in self._nodi:
            for v in self._nodi:
                if u.CustomerId != v.CustomerId:  # Mai collegare un nodo a se stesso

                    # Troviamo quanti artisti hanno in comune usando l'intersezione dei Set
                    artisti_in_comune = mappa_artisti[u.CustomerId].intersection(mappa_artisti[v.CustomerId])

                    # CONDIZIONE 1: Hanno almeno un artista in comune?
                    if len(artisti_in_comune) > 0:

                        # CONDIZIONE 2 (ORIENTAMENTO E PESO):
                        # Da chi ha fatturato MINORE a chi ha fatturato MAGGIORE
                        if u.Fatturato < v.Fatturato:
                            # Definisci il peso a seconda di cosa intende l'esame:
                            peso = len(artisti_in_comune)  # Peso = artisti in comune
                            # peso = v.Fatturato - u.Fatturato   # Peso = differenza di fatturato

                            self._graph.add_edge(u, v, weight=peso)

    def get_archi_massimi(self):
        """
        Cerca il peso massimo nel grafo e restituisce tutti gli archi che hanno quel peso.
        Ritorna una lista di tuple: (nodo_partenza, nodo_arrivo, peso)
        """
        if len(self._graph.edges) == 0:
            return []

        # 1. Trovo il valore massimo assoluto
        peso_max = 0
        for u, v, dati in self._graph.edges(data=True):
            if dati['weight'] > peso_max:
                peso_max = dati['weight']

        # 2. Salvo tutti gli archi che corrispondono al valore record
        archi_vincitori = []
        for u, v, dati in self._graph.edges(data=True):
            if dati['weight'] == peso_max:
                archi_vincitori.append((u, v, dati['weight']))

        return archi_vincitori


# =========================================================================
# 4. CONTROLLER (UI/controller.py)
# =========================================================================
import flet as ft


class Controller:
    # ... costruttore e inizializzazione view/model ...

    def handle_crea_grafo(self, e):
        # 1. Leggo il dato inserito/scelto dall'utente
        stato = self._view._ddStato.value

        # Controllo errori
        if not stato:
            self._view.txt_result.controls.append(ft.Text("Errore: Seleziona uno stato dalla tendina!", color="red"))
            self._view.update_page()
            return

        # 2. Faccio lavorare il model
        self._model.build_graph(stato)

        # 3. Stampo le informazioni base (Nodi e Archi)
        n_nodi = len(self._model._graph.nodes)
        n_archi = len(self._model._graph.edges)

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Grafo creato con successo!\nNumero di nodi: {n_nodi}\nNumero di archi: {n_archi}", color="green")
        )

        # 4. Uso il metodo per gli archi massimi e li stampo
        self._view.txt_result.controls.append(ft.Text("\nElenco degli archi di peso massimo:", weight="bold"))
        archi_max = self._model.get_archi_massimi()

        if not archi_max:
            self._view.txt_result.controls.append(ft.Text("Nessun arco presente nel grafo."))
        else:
            for u, v, peso in archi_max:
                self._view.txt_result.controls.append(
                    ft.Text(f"Da {u} a {v} | Peso arco: {peso}")
                )

        self._view.update_page()