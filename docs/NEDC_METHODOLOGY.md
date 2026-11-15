# Metodo NEDC — requisiti per P3

## 1. Definizione del ciclo

Il NEDC classico comprende:

- quattro ripetizioni del ciclo urbano ECE-15: `4 × 195 s = 780 s`;
- ciclo extraurbano EUDC: `400 s`;
- durata totale: `1.180 s`;
- distanza nominale: `11,007 km`;
- velocità massima: `120 km/h`;
- velocità media nominale: circa `33,6 km/h`.

Il tracciato numerico deve essere acquisito da una fonte normativa/tecnica affidabile. Il file `data/cycles/nedc_template.csv` è soltanto un modello di intestazione, non il ciclo NEDC. Una curva ricostruita visivamente da un grafico non è un tracciato ufficiale e deve essere marcata come approssimazione.

Formato CSV atteso dal loader attuale:

```csv
time_s,speed_kmh
0,0
1,0
...
```

Il loader corrente verifica la validità strutturale del profilo, ma non certifica la conformità al ciclo normativo.

## 2. Masse e classi d'inerzia

Non usare intercambiabilmente:

- massa DIN a vuoto;
- massa EU / massa in ordine di marcia (MRO);
- massa di prova del veicolo;
- massa di riferimento e classe d'inerzia assegnata al banco prova.

Per P3 occorre la massa o la classe d'inerzia derivata secondo la versione normativa applicabile all'omologazione del veicolo. Il Regolamento UNECE n. 83 disciplina la prova Type I e l'impostazione del banco; il Regolamento (CE) n. 692/2008 contiene campi di prova relativi a pneumatici, pressioni, massa del veicolo con conducente e dati coastdown. Regolamenti successivi, come UE 2017/1153 e successive modifiche, includono procedure di ricalcolo NEDC nel contesto WLTP: non applicare le loro formule a un veicolo 2016 senza prima stabilire che siano pertinenti al caso analizzato.

**Azione richiesta:** reperire CoC, numero di omologazione e allegato tecnico del tipo/variante/versione; registrare quale definizione di massa viene utilizzata e quale tabella di inerzia viene applicata.

## 3. Resistenza all'avanzamento

La forza longitudinale richiesta è, nel modello fisico semplificato:

`F_req = F_acc + F_aero + F_roll + F_grade`

con:

- `F_acc = m_eff · a`;
- `F_aero = 0,5 · ρ · Cd · A · v_rel · |v_rel|`;
- `F_roll = Crr · m · g · cos(θ)` in marcia;
- `F_grade = m · g · sin(θ)`.

Per la prova d'omologazione è preferibile usare la curva road-load/coastdown specifica del veicolo, se disponibile:

`F_road(v) = F0 + F1·v + F2·v²`

Attenzione alle unità della velocità. Nei moduli di prova la variabile può essere in km/h, mentre nel nucleo fisico THERMOSIM la velocità è in m/s. Conversione e provenienza vanno sempre dichiarate.

I coefficienti `F0/F1/F2` sono il risultato di una procedura di prova/correzione; non sono sinonimi di `Crr`, `Cd` e area frontale. Se si dispone di entrambi, conservarli come due rappresentazioni con fonti differenti.

## 4. Simulazione backward: catena di calcolo prevista

1. Importare tempo e velocità del ciclo.
2. Derivare l'accelerazione e controllare il tracciato.
3. Calcolare la forza e la potenza richieste alle ruote, includendo le resistenze.
4. Applicare una strategia di marcia/cambiata esplicita e coerente con il test del cambio manuale.
5. Convertire velocità veicolo in regime motore usando raggio dinamico, rapporto marcia e rapporto al ponte.
6. Convertire forza alla ruota in coppia richiesta al motore considerando rendimento trasmissione.
7. Verificare che ogni punto sia nel dominio della curva coppia e dei limiti motore.
8. Interrogare la mappa BSFC e calcolare la portata combustibile.
9. Modellare minimo, avviamento, cut-off in rilascio, cambio marcia, frizione, accessori e condizioni di cold-start in base al livello di accuratezza richiesto.
10. Integrare la portata sul tempo e normalizzare per la distanza percorsa.

Per una mappa BSFC in `g/kWh`, il consumo istantaneo può essere calcolato da `ṁ_fuel = BSFC · P_brake`, dopo conversione coerente delle unità. La potenza da usare è quella al freno al motore, non la potenza alle ruote. In condizioni di potenza nulla/negativa il semplice prodotto non descrive minimo, fuel cut o trascinamento: serve una logica separata.

## 5. Cambio manuale e strategia di cambiata

Non esiste una sola strategia di cambiata universale applicabile automaticamente a tutte le varianti manuali e a ogni procedura di prova. Per un confronto rigoroso registrare:

- tabella/istruzioni di cambiata previste dal protocollo applicabile;
- marcia usata in ogni intervallo del ciclo;
- regime minimo, regime massimo e limiti di coppia;
- tempi di cambiata e interruzione di coppia, se modellati;
- gestione frizione e riavviamento dopo spegnimento Start/Stop, se presente nel test;
- trattamento del rilascio e della decelerazione.

Una cambiata ottimizzata per ridurre i consumi non equivale necessariamente alla procedura di omologazione.

## 6. Cosa manca nella v0.1.0

La release attuale:

- carica un ciclo e calcola accelerazione;
- calcola la domanda meccanica alle ruote con un modello semplificato basato su massa, `Cd`, area, `Crr`, densità e pendenza;
- gestisce le relazioni cinematiche elementari del cambio manuale;
- importa una curva di coppia CSV.

Non implementa ancora la catena completa di cui ai punti 4–5: strategia NEDC di cambiata, selezione marcia automatica, matching motore-punto operativo, mappa BSFC, fuel cut, minimo, accessori, consumi integrati e calibrazione rispetto a misure ufficiali.

Pertanto la v0.1.0 **non deve esporre un risultato di consumo NEDC in l/100 km come valido**. Il consumo dichiarato da BMW nella brochure può essere riportato solo come dato di confronto di gamma, indicando ruote, optional e procedura di misura; non va utilizzato come dato per riempire la mappa BSFC.

## 7. Validazione P3

Prima di dichiarare validata una simulazione:

1. verificare durata, distanza, velocità massima e punti/tempi del ciclo importato;
2. confrontare massa/inertia e road-load con documenti omologativi;
3. verificare la velocità veicolo simulata rispetto al tracciato prescritto;
4. verificare regime/coppia motore e rapporti trasmissione su punti noti;
5. integrare carburante con mappa BSFC specifica e modello minimo/overrun;
6. confrontare il risultato con un valore misurato o di omologazione compatibile con identica variante, pneumatici e allestimento;
7. riportare errore, incertezza e parametri calibrati separatamente da quelli misurati.
