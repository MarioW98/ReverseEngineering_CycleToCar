# Politica di gestione dei dati

## Principi generali

1. Tutti i calcoli interni usano unità SI. Le conversioni da km/h, rpm, bar, litri e altre unità avvengono ai confini dei moduli e sono testate.
2. Ogni dato specifico del veicolo deve riportare fonte, unità e campo di applicabilità (modello, carrozzeria, mercato, trazione, cambio, pneumatici e, quando disponibile, VIN/data produzione).
3. Separare sempre dati OEM pubblicati, misure sperimentali, stime/derivazioni e assunzioni.
4. Non convertire un dato di gamma in un dato VIN-specifico senza verifica.
5. Non usare una curva piatta o una coppia massima nominale come sostituto di una curva motore completa.
6. Non interpolare o estrapolare mappe oltre il dominio misurato senza una scelta esplicita e registrata.
7. Coefficienti coastdown `F0/F1/F2` e parametri fisici `Cd/A/Crr` sono rappresentazioni diverse della resistenza all'avanzamento: conservarle separatamente.
8. Massa EU a vuoto, massa DIN, massa in ordine di marcia, massa di prova e classe d'inerzia non sono sinonimi.
9. Pneumatico nominale e raggio dinamico/di rotolamento non sono sinonimi.
10. Un consumo carburante può essere dichiarato solo dopo aver definito una mappa BSFC o un modello energetico calibrato e validato, compresi minimo, rilascio/overrun e carichi ausiliari pertinenti.
11. Nessun rapporto di trasmissione deve essere copiato da un modello xDrive o automatico a una variante RWD manuale.
12. Il VIN è un dato identificante: non va committato nel repository. Usare identificativi interni e conservare localmente gli estratti identificativi oscurati.

## Livelli di qualità ammessi

- `oem_published_reference`: dato BMW pubblicato per una variante di gamma.
- `secondary_reference`: dato di catalogo/archivio terzo.
- `measured`: misura con procedura, strumenti, condizioni e incertezza documentati.
- `derived`: valore ottenuto da equazione esplicita e dati sorgente tracciati.
- `assumption`: ipotesi per test o analisi di sensibilità; non è un dato veicolo.
- `pending`: valore mancante o non sufficientemente verificato.

## Regole di compilazione

- Un valore `null` è preferibile a un numero non verificato.
- Per i valori derivati, registrare equazione, ingressi e propagazione dell'incertezza.
- Per le curve motore, indicare se sono a pieno carico, a carico parziale, corrette SAE/DIN o non corrette, e le condizioni di misura.
- Per BSFC, indicare unità `g/kWh`, regime, coppia/potenza, temperatura e carburante.
- Per pneumatici, registrare marca, modello, misura, indice, pressione, carico, usura e circonferenza di rotolamento.
- Per road-load, registrare unità e convenzione di velocità dei coefficienti, oltre a condizioni ambientali e massa di prova.

## Stato release

La v0.1.0 è un framework sperimentale di dinamica longitudinale e controllo dei dati. Non è uno strumento di omologazione. Il piano specifico delle 19 voci aperte è in [`DATA_ACQUISITION_PLAN.md`](DATA_ACQUISITION_PLAN.md); il riferimento dei dati BMW è in [`TECHNICAL_REFERENCE.md`](TECHNICAL_REFERENCE.md).
