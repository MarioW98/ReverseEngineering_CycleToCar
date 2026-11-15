# ReverseEngineering_CycleToCar

Software per il reverse engineering dei consumi e delle prestazioni automobilistiche a partire dai cicli di omologazione (NEDC, EUDC, WLTP).

## 🎯 Obiettivo

Dati:
- Geometria e specifiche del veicolo (peso, Cx, cambio, ecc.)
- Curva di coppia/potenza del motore
- Risultati dei cicli di omologazione (consumi dichiarati)

Il software **ricostruisce la mappa di efficienza (BSFC) del motore** e la utilizza per stimare:
- Consumi reali in diversi scenari di guida
- Prestazioni pure (0-100, velocità massima, ripresa)
- Punti di funzionamento del motore in condizioni reali

## 📁 Struttura del Progetto

ReverseEngineering_CycleToCar/
├── data/ # Dati di input (YAML, CSV)
│ ├── cars/ # Specifiche veicoli
│ └── cycles/ # Cicli di omologazione
├── src/ # Codice sorgente modulare
│ ├── models.py # Dataclass (Vehicle, Engine, Cycle...)
│ ├── loaders.py # Caricamento dati
│ ├── dynamics.py # Fisica longitudinale
│ ├── engine.py # Modelli BSFC
│ ├── simulator.py # Orchestratore
│ ├── optimizer.py # Reverse engineering
│ └── visualization.py # Grafici e report
├── experiments/ # Script di esperimenti specifici
├── output/ # Grafici generati
├── main.py # Entry point
└── requirements.txt


## 🚀 Installazione

```bash
# Crea un ambiente virtuale (consigliato)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Installa le dipendenze
pip install -r requirements.txt
```

## 💻 Utilizzo

## Esecuzione completa

```bash
python main.py
```

Esegue il workflow standard:
1. Carica BMW 116d F20
2. Calibra BSFC su NEDC (target: 4.3 L/100km)
3. Valida su EUDC (target: 4.0 L/100km)
4. Genera report in `output/`

## Esperimenti specifici

```bash
python experiments/01_calibrate_nedc.py
python experiments/02_validate_eudc.py
```

## 🔬 Metodologia

Il reverse engineering si basa sulla risoluzione di un problema inverso:
1. **Forward model**: dato un BSFC, calcola il consumo del ciclo
2. **Ottimizzazione**: trova il BSFC che minimizza l'errore rispetto al consumo dichiarato
3. **Validazione cross**: testa il BSFC calibrato su un ciclo diverso (EUDC)

Se il modello è accurato su entrambi i cicli, la mappa BSFC ricostruita è affidabile per simulazioni reali.

## 📊 Output
- `output/nedc_analysis.png` - Analisi dettagliata del ciclo NEDC
- `output/comparison_report.png` - Confronto NEDC vs EUDC

## 📝 Licenza

Progetto personale di reverse engineering a scopo "didattico".



## 📄 `.gitignore` (bonus utile)

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# Output generati
output/*.png
output/*.pdf
*.log

# IDE
.vscode/
.idea/
*.swp
.DS_Store

# Jupyter
.ipynb_checkpoints/
```