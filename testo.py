"""Si consideri il database "Chinook", contenente informazioni su clienti (Customer),
fatture (Invoice), righe di fattura (InvoiceLine), brani (Track) e artisti (Artist).
Il database è strutturato secondo il diagramma ER fornito nella pagina seguente.

Si intende costruire un’applicazione che permetta di analizzare le abitudini di acquisto
dei clienti in funzione del paese di provenienza e delle spese effettuate.

L’applicazione dovrà svolgere le seguenti funzioni:

PUNTO 1 a. L’utente seleziona dal corrispondente menù a tendina un paese (Country)
tra quelli associati ai clienti nella tabella Customer. b. Premendo il pulsante "Crea grafo",
l’applicazione costruisce un grafo orientato e pesato che rappresenta le relazioni tra clienti appartenenti
al paese selezionato. I vertici sono i clienti (Customer) che hanno effettuato almeno una fattura (Invoice)
e che risiedono nel paese scelto. Per ogni cliente C, si calcoli il fatturato totale come la somma dei campi
Total delle sue fatture. (Suggerimento. Potrebbe essere conveniente aggiungere un attributo alla classe Customer
per memorizzare il fatturato totale.) Esiste un arco da C1 a C2 se:

entrambi hanno effettuato almeno una fattura, e
almeno un artista compare in fatture di entrambi (cioè esiste almeno un artista che ha brani acquistati da C1
e anche da C2, utilizzando le tabelle customer, invoice, invoiceline, track, album, artist). Il verso dell’arco
è da C1 verso C2 se il fatturato totale di C1 è maggiore di quello di C2; in caso di parità si inseriscono due archi,
uno in ciascun verso. Il peso dell’arco (C1, C2) è la somma dei fatturati dei due clienti. c. Costruito il grafo,
l’applicazione visualizza immediatamente il numero di vertici e il numero di archi. d. Alla pressione del
tasto "Stampa Info", l’applicazione visualizza: i) il cliente più influente, dove l’influenza di un cliente è definita
come: influenza(C) = peso archi uscenti – peso archi entranti; ii) i 5 archi di peso massimo, in ordine decrescente di peso.
PUNTO 2 a. L’utente seleziona da un menù a tendina un cliente sorgente tra quelli presenti nel grafo creato al punto 1. b. Premendo
il pulsante "Trova sequenza clienti", l’applicazione deve trovare un cammino semplice nel grafo a partire dal cliente selezionato,
soggetto ai seguenti vincoli:

il cammino deve essere di lunghezza massima (numero di archi) tra quelli che rispettano i vincoli successivi;
il fatturato totale dei clienti visitati lungo il cammino deve essere decrescente: per ogni arco da C_i a C_{i+1},
il fatturato di C_{i+1} deve essere <= del fatturato di C_i; c. L’applicazione visualizza:
la lista ordinata di clienti che compongono il cammino;
per ciascun cliente, il fatturato totale;
il numero di archi del cammino e il fatturato complessivo (somma dei fatturati dei clienti nel cammino)."""