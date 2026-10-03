# P5 — DISPOSICIÓN DEL ADVERSARIAL

`REMEDIATION_ADVERSARIAL = FINDINGS` (reporte: `P5-ADVERSARIAL.md`). Adjudicación Primary Manager:

## F-1 (MAJOR, R-B02) — FALLA; corregida; verificación física aplicada
La regresión era real: config legacy sin `composition_timeout_seconds` pasaba de 120s a 60s (DefaultTimeout CLI). El defecto estaba en la premisa del diseño P3 (fallback a `opts.Timeout`); el comentario del commit que lo justificaba era factualmente falso.
**Fix @ `19b44c1`:** el fallback devuelve `reviewTimeoutSecondsV2()` verbatim (comportamiento legacy exacto, incluido DefaultReviewTimeout=60s aguas arriba cuando ambos campos están ausentes); comentario honesto; `TestV2CompositionTimeoutSelection` extendido con los 3 casos (600s explícito / 120s legacy / 60s doble-fallback) y comentarios corregidos. `go build`+`go vet` limpios, suite de pipeline completa verde (98.8s). Incidencia de higiene durante el fix: `git add -A` incluyó brevemente el gitlink `wt/`; corregido por amend antes de cualquier push — el commit final `19b44c1` contiene sólo los 2 archivos intended, `wt/` permanece untracked.

## F-2 (MINOR, pre-existente) — deuda documentada, sin fix esta campaña
Content como array de partes sigue fatal. Pre-existente @ ef53530, no observado en P1 (sólo empty y invalid-JSON reales), arreglarlo expande blast radius sin evidencia de necesidad. Deuda.

## F-3 (MINOR) — desviación documentada del gate de coverage
El gate "coverage ≥95% en paquetes tocados" no se cumple a nivel paquete (shortfall pre-existente: openrouter 86.6%, claims 68.0%). Los caminos NUEVOS sí están cubiertos (tests red-green de R-B01/R-B02/R-MI04). Subir coverage de paquetes legados queda fuera de la remediación acotada; se registra como desviación consciente del gate P3, no como defecto del producto.

## F-4..F-8 (NOTEs) — tomados como notas
Presupuesto por-invocación (semántica pre-existente); asimetría de fingerprint de timeouts (defensible); preservación de categoría limitada a claims-reconstruction (el resto se preserva por replay del ladder; reviews en resume mantienen placeholder — cosmetivo, durable en journal); guía kind observation-vs-claim aún ambigua (ladder frozen actúa de guardia); peor caso wall-clock 3×600s por invocación de composition (aceptable: 1 invocación por run).

## Veredicto
`P5_DISPOSITION = ACCEPTED_WITH_FIXES` · F-1 cerrado con verificación física · `READY_FOR_LIVE_GATES = YES` · **Candidato para gates y rerun: `19b44c1`** (binario `e5e4fcbe8295fd90…`).
