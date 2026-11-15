# Dati in ingresso

## Ciclo di guida

`cycles/nedc_template.csv` è soltanto uno schema. Inserire il profilo NEDC ufficiale con
campionamento temporale coerente, senza inventare o ricostruire i punti mancanti.
Colonne obbligatorie: `time_s,speed_kmh`. Il primo timestamp deve essere 0 e i tempi
successivi strettamente crescenti.

## Curve motore

`engine_maps/torque_curve_template.csv`: punti della curva a pieno carico, con colonne
`rpm,torque_nm`.

`engine_maps/bsfc_map_template.csv`: punti della mappa di consumo specifico, con colonne
`rpm,torque_nm,bsfc_g_kwh`. Usare dati della variante esatta e annotare fonte, condizioni
di prova e unità. La mappa BSFC non è ancora interpolata dal motore di simulazione v0.1.0.
