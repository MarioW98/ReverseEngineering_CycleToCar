# Riferimento tecnico — BMW Serie 1 F20 LCI (2016)

## 1. Campo di applicazione

La configurazione iniziale di THERMOSIM rappresenta la BMW Serie 1 **F20 LCI, carrozzeria a 5 porte, mercato europeo**, con motore diesel anteriore longitudinale, **trazione posteriore (RWD)** e cambio manuale a 6 rapporti.

L'anno 2016 è un riferimento di modello, non un identificatore tecnico sufficiente. Per una vettura reale servono almeno data di produzione, codice modello/tipo e VIN. La denominazione commerciale non identifica da sola ogni variante di motore, cambio, pneumatico e massa.

## 2. Dati di gamma documentati

| Versione | Cilindrata | Cilindri/valvole | Potenza massima | Coppia massima | Famiglia motore di riferimento |
|---|---:|---:|---:|---:|---|
| 114d | 1.496 cm³ | 3/4 | 70 kW a 4.000 rpm | 235 Nm, 1.750–2.250 rpm | B37, da confermare sul VIN |
| 116d | 1.496 cm³ | 3/4 | 85 kW a 4.000 rpm | 270 Nm, 1.750–2.250 rpm | B37D15U0, suffisso da confermare |
| 118d | 1.995 cm³ | 4/4 | 110 kW a 4.000 rpm | 320 Nm, 1.500–3.000 rpm | B47U / famiglia B47D20, codice esatto da confermare |

**114d — cautela storica.** La scheda BMW 2018 riporta la versione 114d da 1.496 cm³, 3 cilindri, 70 kW e 235 Nm. Il catalogo applicazioni ricambi consultato per BMW Serie 1 2016, variante F20N/ECE a 5 porte, identifica la famiglia motore B37. L'archivio dei codici modello F20 LCI riporta anche 114d B37K (codice modello 1V51/1V52) e una variante storica 114d N47D16U1 (2R51). Perciò in THERMOSIM è corretto mantenere `engine_code: null` fino alla verifica VIN/data di produzione; non va assegnato un suffisso per deduzione.

**116d e 118d.** Le schede tecniche BMW 01/2015 per F20 5 porte costituiscono riferimenti OEM pubblicati per motore, masse a vuoto, resistenza aerodinamica e pneumatici. Sono vicine temporalmente al MY2016, ma l'applicabilità al singolo esemplare resta subordinata a VIN, equipaggiamento e omologazione.

## 3. Cambio manuale

BMW pubblica per 116d e 118d RWD con cambio manuale a 6 marce questi rapporti:

| Marcia | Rapporto |
|---|---:|
| I | 4,002 |
| II | 2,130 |
| III | 1,396 |
| IV | 1,000 |
| V | 0,781 |
| VI | 0,668 |
| Retromarcia | 3,647 |
| Rapporto al ponte | 3,077 |

I rapporti sono riportati nelle schede BMW 01/2015 per 116d e 118d a 5 porte. La configurazione YAML li conserva come **riferimento OEM pubblicato**, non come conferma VIN-specifica. In particolare, il dato 2018 relativo alla sola esistenza del manuale a 6 marce sulla 114d non dimostra che i suoi rapporti siano identici a quelli di 116d/118d: per la 114d i valori restano non compilati.

La trasmissione 118d xDrive non è applicabile a questa release. Non usare i rapporti della versione xDrive o Steptronic nella configurazione RWD manuale.

## 4. Masse a vuoto BMW pubblicate

| Versione | DIN | EU | Riferimento | Stato in THERMOSIM |
|---|---:|---:|---|---|
| 116d 5 porte | 1.320 kg | 1.395 kg | BMW Media Information 01/2015 | riferimento pubblicato; confermare variante/allestimento |
| 118d 5 porte | 1.350 kg | 1.425 kg | BMW Media Information 01/2015 | riferimento pubblicato; confermare variante/allestimento |
| 114d 5 porte | non acquisita in forma DIN/EU verificata | non acquisita | fonti secondarie riportano valori non sufficientemente qualificati | non importare come dato validato |

La massa DIN, la massa EU e la massa/inertia di prova NEDC non sono sinonimi. La massa a vuoto EU include convenzioni diverse da quella DIN; optional, ruote e allestimento possono cambiare la massa effettiva. Non calcolare il campo `nedc_test_mass_kg` copiando una delle colonne sopra.

## 5. Pneumatici e raggio dinamico

Le schede BMW 01/2015 riportano pneumatici di riferimento 195/55 R16 per le versioni 116d e 118d, con indici di velocità diversi nelle rispettive schede (116d 87H, 118d 87W). Le matrici BMW di approvazione ruote/pneumatici mostrano più combinazioni ammesse per F20/F21 e per singole motorizzazioni.

La misura sul fianco del pneumatico non basta a determinare il raggio dinamico da usare nella cinematica. Il raggio geometrico nominale si ricava da:

`r_nom = [diametro cerchio + 2 × larghezza × rapporto d'aspetto] / 2`

Per 195/55 R16 il raggio nominale geometrico è circa **0,310 m**. Non è il raggio dinamico/di rotolamento sotto carico e **non va inserito** in `wheel_dynamic_radius_m` come se fosse misurato. Il valore da simulazione va ricavato dalla circonferenza di rotolamento effettiva con pneumatico, pressione e carico definiti, oppure da una fonte tecnica equivalente.

Per la 114d le combinazioni pneumatico dipendono da anno, allestimento e omologazione: non si assegna una misura singola senza riscontro sulla vettura.

## 6. Aerodinamica e resistenza al rotolamento

BMW pubblica per 116d e 118d F20 a 5 porte `Cd = 0,30` e area frontale `A = 2,14 m²` (prodotto `Cd × A = 0,642 m²`). Sono valori di riferimento OEM, non automaticamente estendibili alla 114d, ad altri allestimenti o a configurazioni ruota/aerodinamica diverse.

Non sono stati reperiti coefficienti di rotolamento pneumatico (`Crr`) e coefficienti di coastdown/omologazione `F0`, `F1`, `F2` riferibili alle tre configurazioni precise. Restano quindi `null`.

Le due rappresentazioni della resistenza non sono intercambiabili:

- Modello fisico semplificato: aerodinamica da `Cd`, `A`, densità aria; rotolamento da `Crr`, massa e gravità.
- Modello coastdown: forza `F(v) = F0 + F1·v + F2·v²`, usando la convenzione di unità della specifica fonte (spesso velocità in km/h nei documenti di omologazione).

Conservare entrambe le serie se disponibili; non stimare una terna `F0/F1/F2` dai soli `Cd/A/Crr` senza dichiarare un modello e le relative ipotesi.

## 7. Curve coppia e consumo specifico

I valori di coppia massima e potenza massima sono punti/plateau nominali, non una curva completa. Non sono stati trovati grafici OEM pubblici sufficientemente dettagliati da trasformare in mappe calibrate per le tre varianti.

Per una simulazione energetica servono almeno:

- curva a pieno carico `torque(rpm)` con passo di regime e condizioni di misura;
- preferibilmente limiti di coppia a carico parziale o un modello di controllo;
- mappa BSFC `g/kWh` in funzione di regime e coppia (o dati di consumo equivalente sufficienti a calibrare una mappa);
- comportamento in rilascio, fuel cut/overrun, minimo e carichi ausiliari.

I consumi NEDC di brochure non sostituiscono una mappa BSFC: sono risultati aggregati del ciclo e non identificano il consumo di ogni punto operativo.

## 8. Livelli di affidabilità

| Livello | Significato | Uso ammesso |
|---|---|---|
| `oem_published_reference` | dato pubblicato da BMW per una variante di gamma | base iniziale, con applicabilità dichiarata |
| `secondary_reference` | catalogo tecnico/archivio terzo | corroborazione, non prova VIN-specifica |
| `measured` | misura sperimentale con procedura, strumento e condizioni registrati | calibrazione, se qualità adeguata |
| `derived` | valore calcolato da dati di origine espliciti | solo con equazione e propagazione incertezza documentate |
| `assumption` | ipotesi temporanea esplicita | test di sensibilità, mai risultato presentato come OEM |
| `pending` | dato non disponibile o non sufficientemente tracciato | non usare in simulazioni che lo richiedono |

## 9. Fonti principali

Vedere [`SOURCES.md`](SOURCES.md) per identificativi, URL, contenuto e limiti di ciascuna fonte. Vedere [`DATA_ACQUISITION_PLAN.md`](DATA_ACQUISITION_PLAN.md) per il piano di chiusura dei 19 elementi `PENDING` dell'audit.
