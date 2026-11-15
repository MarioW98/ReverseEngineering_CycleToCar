# Modello fisico — versione 0.1.0

## Convenzioni

Le grandezze interne sono SI: m, s, kg, N, Nm, Pa, W, rad/s. I file CSV possono esporre km/h e rpm per leggibilità; la conversione avviene all'ingresso/uscita dei moduli.

## Dinamica longitudinale attualmente implementata

La forza richiesta alle ruote è la somma di:

`F_total = F_acc + F_aero + F_roll + F_grade`

### Forza inerziale

`F_acc = m · k_rot · a`

Dove `m` è la massa del veicolo, `a` l'accelerazione longitudinale e `k_rot` il fattore inerziale configurato. Nella versione attuale il fattore rotazionale moltiplica la massa del termine inerziale; non rappresenta un modello dettagliato delle inerzie di ogni componente rotante.

### Resistenza aerodinamica

`F_aero = 1/2 · ρ · Cd · A · (v + v_wind) · |v + v_wind|`

`v_wind` positivo significa vento contrario all'avanzamento, secondo la convenzione del codice.

### Resistenza al rotolamento

`F_roll = Crr · m · g · cos(θ)` quando la velocità è positiva. Il codice iniziale pone a zero il termine a veicolo fermo; non modella deformazioni statiche, avviamento o soglia di distacco.

### Pendenza

`F_grade = m · g · sin(θ)`

### Potenza alle ruote

`P_wheel = F_total · v`

La potenza può essere negativa durante una decelerazione; la release attuale non converte automaticamente la potenza negativa in recupero energetico o in consumo di carburante negativo.

## Cinematica della trasmissione

Per una marcia `j`, rapporto `i_j`, rapporto finale `i_0`, raggio dinamico ruota `r_w` e velocità veicolo `v`:

`n_wheel = v / (2π r_w) · 60`

`n_engine = n_wheel · i_j · i_0`

Per ottenere una forza alle ruote `F_w`:

`T_engine = F_w · r_w / (i_j · i_0 · η_trans)`

Il rendimento `η_trans` è un parametro di modello, non un numero universale. Deve essere assunto o misurato e sottoposto ad analisi di sensibilità.

## Potenza motore

`P_engine = T_engine · 2π · n_engine / 60`

con coppia in Nm, regime in rpm e potenza in W. La curva coppia deve coprire il regime richiesto; l'interpolazione fuori dal dominio misurato non è ammessa in modo implicito.

## Limiti della versione attuale

- Non c'è selezione automatica della marcia né logica di cambiata.
- Non sono inclusi inerzie individuali di albero, volano, ruote e differenziale.
- Non c'è slittamento pneumatico, deformazione transitoria o modello di trazione.
- Non c'è modellazione del motore a carico parziale né controllo turbo/EGR/iniezione.
- Non c'è BSFC, fuel cut, minimo, riscaldamento, accessori o Start/Stop.
- Non è ancora implementato il passaggio automatico da `F0/F1/F2` alla forza road-load.

La documentazione delle equazioni descrive il comportamento del codice attuale, non una simulazione termodinamica completa del motore.
