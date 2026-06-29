# =========================================================================
# 1. CLASSE CUSTOMER (model/customer.py)
# =========================================================================
from dataclasses import dataclass


@dataclass
class Customer:
    CustomerId: int
    FirstName: str
    LastName: str
    Fatturato: float  # Attributo calcolato dalla query SQL

    def __hash__(self):
        return hash(self.CustomerId)

    def __eq__(self, other):
        return self.CustomerId == other.CustomerId

    def __str__(self):
        return f"{self.FirstName} {self.LastName}"


# =========================================================================
# 2. DAO (database/DAO.py)
# =========================================================================
class DAO:

    @staticmethod
    def get_nodi_clienti(country):
        """
        Estrae i clienti di un certo PAESE calcolando direttamente la somma
        dei loro acquisti (il fatturato totale). La JOIN con Invoice garantisce
        in automatico che vengano presi "clienti che hanno effettuato almeno una fattura".
        """
        # conn = DBConnect.get_connection()
        # cursor = conn.cursor(dictionary=True)

        query = """
            SELECT c.CustomerId, c.FirstName, c.LastName, SUM(i.Total) as Fatturato
            FROM Customer c
            JOIN Invoice i ON c.CustomerId = i.CustomerId
            WHERE c.Country = %s
            GROUP BY c.CustomerId
        """
        # cursor.execute(query, (country,))
        # result = [Customer(row["CustomerId"], row["FirstName"], row["LastName"], row["Fatturato"]) for row in cursor]
        # return result

    @staticmethod
    def getEdges(country):
        """
        Coppie di clienti che hanno almeno un artista in comune.
        """
        # conn = DBConnect.get_connection()
        # cursor = conn.cursor(dictionary=True)

        query = """
        SELECT DISTINCT q1.CustomerId as id1, q2.CustomerId as id2
        FROM (
            SELECT DISTINCT c.CustomerId, ar.ArtistId
            FROM customer c, invoice i, invoiceline il, track t, album al, artist ar
            WHERE c.CustomerId = i.CustomerId
              AND i.InvoiceId = il.InvoiceId
              AND il.TrackId = t.TrackId
              AND t.AlbumId = al.AlbumId
              AND al.ArtistId = ar.ArtistId
              AND c.Country = %s
        ) q1,
        (
            SELECT DISTINCT c.CustomerId, ar.ArtistId
            FROM customer c, invoice i, invoiceline il, track t, album al, artist ar
            WHERE c.CustomerId = i.CustomerId
              AND i.InvoiceId = il.InvoiceId
              AND il.TrackId = t.TrackId
              AND t.AlbumId = al.AlbumId
              AND al.ArtistId = ar.ArtistId
              AND c.Country = %s
        ) q2
        WHERE q1.ArtistId = q2.ArtistId
          AND q1.CustomerId < q2.CustomerId
        """
        # cursor.execute(query, (country, country))
        # result = [(row["id1"], row["id2"]) for row in cursor]
        # return result


# =========================================================================
# 3. MODEL (model/model.py)
# =========================================================================
import networkx as nx
import copy


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._nodi = []
        self._idMap = {}

        # Variabili per ricorsione
        self.best_cammino = []
        self.best_score = 0

    def build_graph(self, country):
        self._graph.clear()

        self._nodi = DAO.get_nodi_clienti(country)
        self._graph.add_nodes_from(self._nodi)
        self._idMap = {n.CustomerId: n for n in self._nodi}

        coppie_dao = DAO.getEdges(country)

        for id1, id2 in coppie_dao:
            u = self._idMap.get(id1)
            v = self._idMap.get(id2)

            if u is not None and v is not None:
                # Il peso è la somma dei fatturati dei due clienti
                peso_arco = u.Fatturato + v.Fatturato

                # Il verso va da chi ha FATTURATO MAGGIORE a chi ha FATTURATO MINORE
                if u.Fatturato > v.Fatturato:
                    self._graph.add_edge(u, v, weight=peso_arco)
                elif v.Fatturato > u.Fatturato:
                    self._graph.add_edge(v, u, weight=peso_arco)
                else:
                    # In caso di parità, inserisco due archi (uno in ciascun verso)
                    self._graph.add_edge(u, v, weight=peso_arco)
                    self._graph.add_edge(v, u, weight=peso_arco)

    def get_most_influential(self):
        """Restituisce il SINGOLO cliente con influenza maggiore."""
        if len(self._graph.nodes) == 0:
            return None, 0

        best_node = None
        max_inf = -999999999

        for n in self._graph.nodes:
            peso_uscente = self._graph.out_degree(n, weight='weight')
            peso_entrante = self._graph.in_degree(n, weight='weight')
            influenza = peso_uscente - peso_entrante

            if influenza > max_inf:
                max_inf = influenza
                best_node = n

        return best_node, max_inf

    def get_top5_archi(self):
        """Restituisce i 5 archi di peso massimo in ordine decrescente."""
        archi = []
        for u, v, dati in self._graph.edges(data=True):
            archi.append((u, v, dati['weight']))

        archi.sort(key=lambda x: x[2], reverse=True)
        return archi[:5]

    # ==================== RICORSIONE (PUNTO 2) ====================
    def get_cammino_lunghezza_massima(self, partenza):
        self.best_cammino = []
        self.best_score = 0  # In questo caso è il NUMERO DI ARCHI (cioè nodi - 1)

        self._ricorsione([partenza])

        # Calcolo finale del fatturato complessivo richiesto dal testo
        fatturato_totale = sum(nodo.Fatturato for nodo in self.best_cammino)

        return self.best_cammino, self.best_score, fatturato_totale

    def _ricorsione(self, parziale):
        # Il punteggio è la lunghezza del cammino in termini di ARCHI
        numero_archi_attuali = len(parziale) - 1

        if numero_archi_attuali > self.best_score:
            self.best_score = numero_archi_attuali
            self.best_cammino = copy.deepcopy(parziale)

        ultimo = parziale[-1]

        for vicino in self._graph.neighbors(ultimo):
            if vicino not in parziale:
                # VINCOLO: Il fatturato deve essere decrescente (C_i+1 <= C_i)
                if vicino.Fatturato <= ultimo.Fatturato:
                    parziale.append(vicino)
                    self._ricorsione(parziale)
                    parziale.pop()


# =========================================================================
# 4. CONTROLLER (UI/controller.py)
# =========================================================================
import flet as ft


class Controller:

    def handle_crea_grafo(self, e):
        country = self._view._ddPaese.value
        if not country:
            self._view.txt_result.controls.append(ft.Text("Errore: Seleziona un paese!", color="red"))
            self._view.update_page()
            return

        self._model.build_graph(country)

        n_nodi = len(self._model._graph.nodes)
        n_archi = len(self._model._graph.edges)

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Grafo creato!\nNumero di vertici: {n_nodi}\nNumero di archi: {n_archi}", color="green",
                    weight="bold")
        )
        self._view.update_page()

    def handle_stampa_info(self, e):
        if len(self._model._graph.nodes) == 0:
            self._view.txt_result.controls.append(ft.Text("Crea prima il grafo!", color="red"))
            self._view.update_page()
            return

        # 1. Cliente più influente
        miglior_nodo, influenza = self._model.get_most_influential()

        self._view.txt_result.controls.append(ft.Text("\n--- INFO GRAFO ---", weight="bold"))
        self._view.txt_result.controls.append(
            ft.Text(f"Cliente più influente: {miglior_nodo.FirstName} {miglior_nodo.LastName} (Influenza: {influenza})",
                    color="blue")
        )

        # 2. I 5 archi di peso massimo
        top_5_archi = self._model.get_top5_archi()
        self._view.txt_result.controls.append(ft.Text("I 5 archi di peso massimo:"))
        for u, v, peso in top_5_archi:
            self._view.txt_result.controls.append(
                ft.Text(f"  {u.FirstName} {u.LastName} -> {v.FirstName} {v.LastName} | Peso: {peso}")
            )

        self._view.update_page()

    def handle_trova_sequenza(self, e):
        nodo_partenza = self._view._ddCliente.value

        if nodo_partenza is None:
            self._view.txt_result.controls.append(ft.Text("Seleziona il cliente di partenza!", color="red"))
            self._view.update_page()
            return

        cammino, numero_archi, fatturato_totale = self._model.get_cammino_lunghezza_massima(nodo_partenza)

        if len(cammino) <= 1:
            self._view.txt_result.controls.append(
                ft.Text(f"Non è possibile iniziare un cammino valido da {nodo_partenza.FirstName}.", color="red")
            )
        else:
            self._view.txt_result.controls.append(ft.Text("\n--- CAMMINO TROVATO ---", weight="bold"))
            self._view.txt_result.controls.append(
                ft.Text(f"Numero di archi del cammino: {numero_archi}")
            )
            self._view.txt_result.controls.append(
                ft.Text(f"Fatturato complessivo del cammino: {fatturato_totale}")
            )

            self._view.txt_result.controls.append(ft.Text("Lista ordinata dei clienti:", weight="bold"))

            for n in cammino:
                self._view.txt_result.controls.append(
                    ft.Text(f"  - {n.FirstName} {n.LastName} | Fatturato: {n.Fatturato}")
                )

        self._view.update_page()