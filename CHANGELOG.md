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


## Documentation revision — 2026-11-15

- Added technical reference for BMW F20 LCI 114d/116d/118d and explicit applicability limits.
- Added source register with OEM, secondary and normative references.
- Added acquisition procedure and a field-by-field closure plan for all 19 audit `PENDING` items.
- Added NEDC methodology, physics model notes, open-items register and YAML data templates.
- Clarified 114d engine-family evidence (B37 on 2016 F20N application catalogue) while leaving exact engine code VIN-dependent.
- No unverified mass, dynamic wheel radius, rolling resistance, road-load coefficients, 114d gear ratios, torque curves or BSFC maps were fabricated.
- Runtime package version remains 0.1.0; this is a documentation-only update.
