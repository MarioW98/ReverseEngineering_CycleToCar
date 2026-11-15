# Piano di acquisizione dati — BMW F20 2016

## Obiettivo

Chiudere i dati `PENDING` dell'audit mantenendo la tracciabilità per versione e per singolo esemplare. Lo stato iniziale dell'audit è: `ERROR=0`, `PENDING=19`, `WARNING=0`, `OK=0`.

Un campo passa da `PENDING` a disponibile solo quando sono registrati valore, unità, fonte/evidenza, applicabilità, data di acquisizione e livello di qualità. La mera presenza di un numero nel web non costituisce conferma.

## Elementi aperti

| ID | File/campo | Varianti | Evidenza preferita | Criterio di chiusura |
|---|---|---|---|---|
| D01 | `common/road_load.yaml`: `rolling_resistance_coefficient` | 116d/118d; verificare separatamente 114d | pneumatico esatto e relativo RRC da documentazione tecnica/etichetta energetica o misura al banco | valore adimensionale con marca/modello/misura pneumatico, classe e pressione di riferimento |
| D02 | `common/road_load.yaml`: `F0/F1/F2` | ciascuna configurazione o famiglia omologativa dimostrata | CoC/allegato omologativo, rapporto coastdown o scheda di prova dinamometro | tre coefficienti con unità, convenzione della velocità, massa, pneumatici e condizioni di prova |
| D03 | `114d/vehicle.yaml`: massa NEDC | 114d | CoC, documentazione di omologazione o scheda tecnica del banco a rulli | valore espressamente associato alla massa/inertia usata nel test, con norma/edizione identificata |
| D04 | `114d/vehicle.yaml`: raggio dinamico | 114d | misura circonferenza di rotolamento sotto carico o dato tecnico del pneumatico montato | raggio efficace `C_roll/(2π)` con carico e pressione riportati |
| D05 | `114d/engine.yaml`: codice motore | 114d | VIN e data produzione tramite BMW ETK/ISTA o documentazione BMW | codice completo e codice modello/type code associati allo stesso veicolo |
| D06 | `114d/engine.yaml`: curva coppia/rpm | 114d | banco prova motore/chassis dyno con protocollo e correzioni documentati | CSV coppia/regime, condizioni, unità, provenienza e dominio dichiarati |
| D07 | `114d/engine.yaml`: mappa BSFC | 114d | mappa banco prova o fonte ingegneristica verificabile | griglia regime/coppia/BSFC, unità g/kWh e condizioni; validazione indipendente |
| D08 | `114d/transmission.yaml`: rapporti 1–6 | 114d | codice cambio da VIN + scheda tecnica ricambi/trasmissione BMW | sei rapporti e codice cambio verificati sulla variante precisa |
| D09 | `114d/transmission.yaml`: rapporto al ponte | 114d | VIN + catalogo ricambi BMW o misura documentata | rapporto finale esatto e compatibilità con la trasmissione identificata |
| D10 | `116d/vehicle.yaml`: massa NEDC | 116d | CoC/dossier omologazione o verbale prova | valore NEDC/riferimento inerziale, non massa DIN/EU copiata |
| D11 | `116d/vehicle.yaml`: raggio dinamico | 116d | misura circonferenza di rotolamento sotto carico o dato tecnico | valore efficace con pneumatico, carico e pressione documentati |
| D12 | `116d/engine.yaml`: suffisso/codice esatto | 116d | VIN + data produzione + BMW ETK/ISTA | conferma del codice motore completo, non solo famiglia B37 |
| D13 | `116d/engine.yaml`: curva coppia/rpm | 116d | banco prova o documentazione tecnica affidabile | CSV validato con condizioni di prova |
| D14 | `116d/engine.yaml`: mappa BSFC | 116d | banco prova/mappe di consumo specifiche del motore | mappa completa in g/kWh e copertura del dominio operativo NEDC |
| D15 | `118d/vehicle.yaml`: massa NEDC | 118d | CoC/dossier omologazione o verbale prova | valore NEDC/riferimento inerziale, non massa DIN/EU copiata |
| D16 | `118d/vehicle.yaml`: raggio dinamico | 118d | misura circonferenza di rotolamento sotto carico o dato tecnico | valore efficace con pneumatico, carico e pressione documentati |
| D17 | `118d/engine.yaml`: suffisso/codice esatto | 118d | VIN + data produzione + BMW ETK/ISTA | codice completo (famiglia B47) confermato |
| D18 | `118d/engine.yaml`: curva coppia/rpm | 118d | banco prova o documentazione tecnica affidabile | CSV validato con condizioni di prova |
| D19 | `118d/engine.yaml`: mappa BSFC | 118d | banco prova/mappe di consumo specifiche del motore | mappa completa in g/kWh e copertura del dominio operativo NEDC |

## Dati già disponibili, ma da confermare sul veicolo

- 116d e 118d: rapporti I–VI, retromarcia e rapporto al ponte pubblicati da BMW nel 2015 per F20 5 porte RWD con cambio manuale.
- 116d e 118d: masse DIN/EU, `Cd × A` e pneumatico di riferimento pubblicati nelle schede tecniche BMW 01/2015.
- 114d: famiglia B37 indicata nel catalogo applicazioni F20N 2016; la codifica completa dipende da variante e data di produzione.
- 114d: BMW pubblica la configurazione RWD/manuale a 6 marce e i dati di gamma 70 kW/235 Nm/1.496 cm³ per la generazione aggiornata; non è stata documentata una coppia completa di rapporti cambio/ponte specifica e verificata per il 2016.

Questi dati non sono conteggiati come confermati VIN-specifici. I rapporti del cambio 116d/118d presenti nei file YAML hanno stato `published_reference_to_confirm_for_exact_2016_vehicle`.

## Sequenza operativa consigliata

### A. Identificazione della vettura

1. Raccogliere per ogni auto: data produzione, VIN (da conservare privatamente), codice tipo/variante/versione, mercato, carrozzeria, allestimento e codice cambio.
2. Consultare il catalogo BMW/ETK con il VIN, senza pubblicare il VIN in repository o documentazione condivisa.
3. Salvare in locale un estratto dei dati identificativi oscurando il VIN; nel repository usare un ID interno non identificante.

### B. Masse e pneumatici

1. Acquisire CoC o documentazione di omologazione del singolo esemplare.
2. Registrare separatamente massa DIN, massa EU/MRO, massa di prova NEDC o classe d'inerzia al banco.
3. Fotografare la targhetta pneumatici e rilevare marca, modello, dimensione, indice, pressione e usura.
4. Misurare la circonferenza di rotolamento sotto carico, in condizioni ripetibili; non utilizzare il raggio nominale statico come raggio dinamico.

### C. Motore e trasmissione

1. Identificare codice motore e codice cambio tramite VIN.
2. Acquisire curva coppia/regime da banco; annotare temperatura, carburante, correzioni, accessori attivi e protocollo.
3. Acquisire mappa BSFC o misurare portata massica combustibile e potenza al freno su una matrice di punti regime/carico.
4. Verificare i rapporti I–VI e il rapporto al ponte da documentazione BMW specifica per la trasmissione identificata.

### D. Road-load

1. Cercare l'allegato di omologazione/coastdown per il tipo approvato.
2. Registrare `F0`, `F1`, `F2`, unità, convenzione velocità, pneumatici, pressioni, massa, temperatura, vento, direzione e procedura di correzione.
3. Se non esiste documentazione, eseguire una prova coastdown secondo la procedura normativa pertinente e conservarne i dati grezzi.
4. In alternativa, acquisire `Cd`, area frontale e RRC dei pneumatici, marcando il risultato come modello fisico stimato e non come equivalente diretto dei coefficienti omologativi.

## Regole di accettazione

- Nessun dato VIN-specifico senza VIN e data di produzione verificati (il VIN non va committato in Git).
- Nessuna stima convertita automaticamente in `oem_published_reference`.
- Nessun valore ricavato da una versione xDrive o automatica attribuito alla manuale RWD.
- Nessuna curva coppia ricostruita dal solo picco di coppia.
- Nessuna mappa BSFC costruita dal consumo combinato di brochure senza una procedura di calibrazione esplicita.
- Le fonti secondarie possono corroborare, non sostituire documentazione OEM o misure.
