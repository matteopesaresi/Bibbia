
#COPY.DEEPCOPY
import copy  # Da mettere sempre in cima al file!
# Esempio: hai una lista di nodi/oggetti
lista_originale = [nodo1, nodo2, nodo3]
# Crei un VERO clone indipendente
copia_sicura = copy.deepcopy(lista_originale)
# Ora puoi modificare la copia senza toccare la lista originale!
#-------------------------------------------------------------------
import copy
def ricorsione(self, parziale, ...):
    # ... faccio controlli vari ...

    # Se trovo un cammino migliore di quello salvato finora:
    if len(parziale) > len(self.best_cammino):
        # SALVATAGGIO CORRETTO E SICURO:
        self.best_cammino = copy.deepcopy(parziale)
    # ... continuo la ricorsione ...
# ---------------------------------------------------------
# 2. CALCOLO DISTANZE GEOGRAFICHE (Spesso nei testi)
from geopy.distance import geodesic
def calcola_distanza_km(self, nodo1, nodo2):
    # Se ti chiedono di unire due città che distano meno di X km
    coords_1 = (nodo1.Lat, nodo1.Lng)
    coords_2 = (nodo2.Lat, nodo2.Lng)

    distanza = geodesic(coords_1, coords_2).km
    return distanza
#---------------------------------------------------------
# 3.1 Ordinamento con "Doppio Criterio" (Pari Merito)
# Es: "Ordina per score decrescente, in caso di parità in ordine alfabetico"
lista.sort(key=lambda x: (-x[1], x[0].name))

#---------------------------------------------------------
#on_change
#view
self.ddyear = ft.Dropdown(label="Anno",
                                  hint_text="Anno da analizzare per gli avvistamenti.",
                                  on_change=self._controller.handleShapes)
#controller
def handleShapes(self, e):
    anno = self._view.ddyear.value
    shapes = self._model.getShapes(anno)
    for shape in shapes:
        self._view.ddshape.options.append(ft.dropdown.Option(key=str(shape), text=str(shape)))
    self._view.update_page()