# THERMOSIM — v0.1.0

Framework Python iniziale per il reverse engineering e la simulazione longitudinale dei
powertrain. La prima configurazione di riferimento è la BMW Serie 1 F20 LCI 5 porte,
anno modello 2016, diesel, trazione posteriore e cambio manuale a 6 marce.

Questa release è una **base tecnica eseguibile**, non ancora un simulatore di consumi
NEDC validato. Gestisce l'audit dei dati, l'importazione di curve coppia, le relazioni
cinematiche del cambio e il calcolo della domanda di forza/potenza alle ruote su un
profilo velocità-tempo. Non stima il carburante finché non sono disponibili mappe BSFC
e parametri veicolo sufficienti.

## Configurazioni incluse

| Versione | Motore nominale | Dati motore inclusi | Cambio manuale |
|---|---:|---|---|
| 114d | 70 kW, 235 Nm | 1.496 cm³, 3 cilindri; codice da confermare | 6 marce, rapporti da acquisire |
| 116d | 85 kW, 270 Nm | 1.496 cm³, 3 cilindri; famiglia B37 | 6 marce, rapporti BMW di riferimento inseriti |
| 118d | 110 kW, 320 Nm | 1.995 cm³, 4 cilindri; famiglia B47 | 6 marce, rapporti BMW di riferimento inseriti |

I valori 116d/118d e i rapporti cambio sono tratti dalla documentazione tecnica BMW
01/2015 per le versioni F20 a 5 porte. Sono riferimenti OEM utili per iniziare, ma vanno
confermati sul VIN e sulla data di produzione dell'esemplare 2016. I dati di gamma 114d provengono da un catalogo europeo BMW 2018; il catalogo applicazioni F20N 2016 consultato indica la famiglia B37. Gli archivi distinguono più codici modello e varianti storiche, quindi il codice motore completo resta da confermare su VIN/data produzione. Queste fonti non sostituiscono la scheda di omologazione del singolo veicolo.


## Documentazione tecnica aggiunta

La documentazione dettagliata è in `docs/`:

- `TECHNICAL_REFERENCE.md`: dati BMW già pubblicati, applicabilità e cautele per le tre motorizzazioni.
- `SOURCES.md`: registro delle fonti OEM, normative e secondarie, con URL e limiti di utilizzo.
- `DATA_ACQUISITION_PLAN.md`: procedura per acquisire e validare i 19 elementi `PENDING`.
- `OPEN_ITEMS.md`: corrispondenza tra l'output dell'audit e le informazioni mancanti.
- `NEDC_METHODOLOGY.md`: definizione del ciclo, massa di prova, road-load e flusso di calcolo previsto per P3.
- `PHYSICS_MODEL.md`: equazioni effettivamente implementate e limitazioni della v0.1.0.
- `templates/`: modelli YAML per registrare identità veicolo e provenienza dei parametri.

I documenti chiariscono i dati disponibili e come acquisire quelli assenti; non riempiono i campi `PENDING` con stime non verificate.

## Installazione

Richiede Python 3.10 o superiore.

```bash
python -m venv .venv
# Windows PowerShell:
.venv\\Scripts\\Activate.ps1
# macOS/Linux:
source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Controllo iniziale dei dati

Dalla cartella principale del progetto:

```bash
thermosim audit --config-dir config/BMW_F20_2016
```

In alternativa:

```bash
python -m thermosim audit --config-dir config/BMW_F20_2016
```

L'audit separa gli errori bloccanti dai dati ancora da acquisire (`PENDING`). Non
riempie i parametri mancanti con valori predefiniti non dichiarati.

## Controllo di un ciclo guida

Il file `data/cycles/nedc_template.csv` contiene solo l'intestazione. Dopo aver inserito
il tracciato ufficiale nel formato `time_s,speed_kmh`:

```bash
thermosim cycle-check data/cycles/nedc.csv
```

Il controllo verifica almeno due campioni, tempo iniziale pari a zero, tempi strettamente
crescenti e velocità non negative. Non verifica che il contenuto sia effettivamente il
ciclo NEDC ufficiale: la provenienza del tracciato deve essere documentata dall'utente.

## Esempio di calcolo della domanda alle ruote

L'API utilizza esclusivamente unità SI internamente. Questo esempio usa parametri
illustrativi per mostrare l'interfaccia: **non sono dati BMW e non vanno usati per
confrontare le tre versioni**.

```python
from thermosim.cycle import DrivingCycle
from thermosim.simulation import simulate_wheel_demand
from thermosim.vehicle import VehicleParameters

cycle = DrivingCycle(
    time_s=(0.0, 1.0, 2.0, 3.0),
    speed_kmh=(0.0, 10.0, 20.0, 20.0),
    name="mini_example",
)

vehicle = VehicleParameters(
    mass_kg=1500.0,
    drag_coefficient=0.30,
    frontal_area_m2=2.14,
    rolling_resistance_coefficient=0.012,
)

samples = simulate_wheel_demand(cycle, vehicle)
for sample in samples:
    print(sample.time_s, sample.force_wheel_n, sample.power_wheel_kw)
```

La funzione restituisce la forza e la potenza richieste alle ruote. Non calcola ancora
il punto operativo motore, la cambiata automatica o il consumo di carburante.

## Importare una curva di coppia

CSV richiesto: `rpm,torque_nm`.

```python
from thermosim.engine import TorqueCurve

curve = TorqueCurve.from_csv("data/engine_maps/116d_torque.csv")
torque = curve.torque_at(2000.0)
power = curve.power_kw_at(2000.0)
```

L'interpolazione è lineare e non estrapola al di fuori del dominio dei dati. La sola
coppia massima nominale presente nei file YAML non viene trasformata artificialmente
in una curva completa.

## Struttura del progetto

```text
config/BMW_F20_2016/
  common/                 # dati comuni carrozzeria e road-load
  114d/                   # motore, cambio e dati veicolo specifici
  116d/
  118d/
data/
  cycles/                 # profili velocità-tempo
  engine_maps/            # curve coppia e mappe BSFC
src/thermosim/
  config.py               # caricamento YAML e audit
  cycle.py                # importazione profili di guida
  engine.py               # curve coppia
  transmission.py         # cambio manuale a 6 marce
  vehicle.py              # dinamica longitudinale
  simulation.py           # domanda alle ruote su ciclo imposto
  cli.py                  # comandi console
tests/                    # test automatici
```

## Dati ancora necessari prima di una simulazione NEDC attendibile

1. VIN e data di produzione per fissare senza ambiguità variante motore/cambio.
2. Rapporti cambio e rapporto al ponte della 114d; conferma dei rapporti 116d/118d sul
   veicolo preciso.
3. Massa di prova NEDC per ogni variante. La massa EU a vuoto riportata in una brochure
   non viene automaticamente assunta come massa di prova.
4. Pneumatico effettivo e raggio dinamico della ruota.
5. Coefficienti di resistenza all'avanzamento F0/F1/F2 da fonte di omologazione/coastdown,
   oppure Cd, area frontale e coefficiente di rotolamento verificati.
6. Profilo NEDC ufficiale campionato e documentato.
7. Curve complete coppia/rpm e mappe BSFC per ogni motore, con condizioni di misura.
8. Strategia di cambiata e regole di gestione rilascio/overrun coerenti con il protocollo.

Senza mappa BSFC o modello di consumo calibrato, THERMOSIM può stimare la domanda
meccanica alle ruote, ma non può produrre un consumo carburante attendibile.

## Test

```bash
pytest
```

## Stato e prossimi incrementi

- **P1 — parzialmente avviata:** configurazioni delle tre motorizzazioni e tracciabilità
  iniziale delle fonti; completare VIN, curve motore e parametri omologativi.
- **P2 — parzialmente avviata:** relazioni cinematiche del manuale a 6 marce; manca la
  conferma dei codici e dei rapporti specifici della 114d.
- **P3 — non ancora completata:** loader NEDC e domanda alle ruote sono presenti, ma non
  è ancora implementato il calcolo completo del consumo NEDC.
- **P4:** da definire insieme in una fase successiva.

## Fonti tecniche di partenza

- BMW Group PressClub, *The new BMW 1 Series model range*, Media Information 01/2015,
  schede tecniche F20 5 porte 116d e 118d (masse, motore, Cd·A e trasmissione):
  <https://www.press.bmwgroup.com/global/article/attachment/T0200199EN/302714>
- BMW Media Information 01/2015, scheda tecnica 116d F20 5 porte:
  <https://www.press.bmwgroup.com/czech/article/attachment/T0200862CS/291892>
- Catalogo europeo BMW Serie 1 2018 (dati di gamma 114d/116d/118d):
  <https://autocatalogarchive.com/wp-content/uploads/2024/09/BMW-Serie-1-2018-EU.pdf>
- Archivio varianti BMW F20 LCI, utile per distinguere le varianti motore ma non
  sostitutivo della verifica VIN:
  <https://www.bimmerarchive.org/e-code/f20-lci.html>
- Catalogo ricambi BMW 2016, utile come riscontro della famiglia motore per il modello:
  <https://www.bmw-spare-parts.com/bmw-cars/1-Series/2016>

---

**THERMOSIM v0.1.0 — stato sperimentale.** Ogni parametro deve mantenere unità, fonte,
variante di applicabilità e qualità del dato. Non usare questa release come strumento di
omologazione o validazione ufficiale dei consumi.
