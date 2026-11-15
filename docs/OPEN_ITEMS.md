# Registro sintetico degli elementi aperti

Stato iniziale rilevato sulla v0.1.0: **19 PENDING, 0 ERROR, 0 WARNING, 0 OK**. Questa pagina integra l'output del comando `thermosim audit`; non modifica le regole di audit né nasconde gli elementi mancanti.

## Elementi PENDING nel comando audit

| File | Elementi segnalati | Quantità |
|---|---|---:|
| `common/road_load.yaml` | `rolling_resistance_coefficient`; coefficienti `F0/F1/F2` | 2 |
| `114d/vehicle.yaml` | massa di prova NEDC; raggio dinamico pneumatico | 2 |
| `114d/engine.yaml` | codice motore; curva coppia/rpm; mappa BSFC | 3 |
| `114d/transmission.yaml` | 6 rapporti; rapporto al ponte | 2 |
| `116d/vehicle.yaml` | massa di prova NEDC; raggio dinamico pneumatico | 2 |
| `116d/engine.yaml` | suffisso/codice motore da confermare; curva coppia/rpm; mappa BSFC | 3 |
| `118d/vehicle.yaml` | massa di prova NEDC; raggio dinamico pneumatico | 2 |
| `118d/engine.yaml` | suffisso/codice motore da confermare; curva coppia/rpm; mappa BSFC | 3 |
| **Totale** |  | **19** |

## Riferimenti già documentati, non ancora VIN-specifici

- 116d e 118d: rapporti cambio e rapporto al ponte pubblicati da BMW per F20 5 porte RWD/manuale nel 2015; già inseriti in YAML ma da confermare su codice cambio/VIN.
- 116d e 118d: massa a vuoto DIN/EU, `Cd × A` e pneumatico riferimento riportati nelle schede BMW 01/2015.
- 114d: dati di gamma aggiornati (1.496 cm³, tre cilindri, 70 kW, 235 Nm) e famiglia B37 riscontrata in catalogo applicazioni 2016; codice completo e trasmissione esatta da verificare.

## Non confondere

- `PENDING` non significa errore software: è un dato identificato come necessario ma non acquisito.
- `0 OK` è coerente con la versione corrente: l'audit non marca come `OK` i singoli dati presenti, ma stampa `OK` solo quando non trova alcun elemento aperto.
- Un numero inserito senza fonte potrebbe far diminuire il conteggio `PENDING` ma peggiorare la qualità scientifica del simulatore. Non farlo.

Per la procedura di chiusura vedere [`DATA_ACQUISITION_PLAN.md`](DATA_ACQUISITION_PLAN.md).
