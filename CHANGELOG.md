# Changelog

## 0.1.0 — prima release

- Struttura modulare del package Python `thermosim`.
- Configurazioni iniziali BMW F20 LCI 2016 per 114d, 116d e 118d.
- Provenienza e stato di verifica dei parametri tecnici.
- Audit CLI della completezza dei dati.
- Importazione e validazione CSV di cicli velocità-tempo.
- Importazione e interpolazione lineare di curve coppia/rpm, senza estrapolazione.
- Modello base delle resistenze all'avanzamento e della dinamica longitudinale.
- Cinematica del cambio manuale a 6 marce.
- Calcolo backward della domanda di forza/potenza alle ruote.
- Test automatici per componenti e configurazioni.

Limitazioni note: nessuna interpolazione della mappa BSFC, nessun modello di consumo
carburante, nessuna strategia automatica di cambiata e nessun profilo NEDC ufficiale
incluso nella release.
