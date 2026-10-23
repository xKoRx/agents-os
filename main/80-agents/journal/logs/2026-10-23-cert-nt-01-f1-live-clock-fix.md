# Change log 2026-10-23 — CERT-NT-01-F1 ejecutado (fix reloj LIVE + deploy DEV)

## Cambio

Delta en `10-projects/Echo Futures/agentes/Echo Futures — Runtime Pools.md`: nueva sección «CERT-NT-01-F1 EJECUTADO (2026-10-23)» tras la decisión del Primary Manager y actualización de la línea STATUS del ledger CERT-NT-01. Contenido: LIVE_DOMAIN_CLOCK_FROZEN corregido (BASE `2ee61791` → FINAL `ac0621a1917a9ecbed50b3daed4add1518ffc71d`, commit único rebaseado sobre la punta lab-v4-shot2 `3b3ae81e` y pusheado FF), verificación independiente VERIFIED_WITH_FINDINGS (V1–V10 PASS), despliegue DEV de la unidad única `echo-core-dev` (release `~/opt/echo-dev/releases/ac0621a1…/` con gateway+relay verbatim), medición en vivo (0 falsos future-dated sobre 4.000+ eventos, timer de silencio disparando, veredicto de frescura real), incidente deploy-correlacionado del job StateFun (re-submit sin restore: reset del sequencer futures + replay FX finito absorbido por write-once) y frontera física Owner sin cambios. Evidencia durable en `~/aranea/work/cert-nt-01-f1/` (fuera del vault).

## Validación

Tarea A (one-shot): rojo en base, verde en fix con -race, coverage 100% del código nuevo, suites con 0 regresiones nuevas vs baseline. Tarea B (one-shot, clon scratch): VERIFIED_WITH_FINDINGS. Runtime: preflight ETCD byte-idéntico (revs 61253/61254), armado ausente por lectura cruda, salud 7/7 owners, identidad del binario vivo por `/proc/PID/exe`, egress de frescura con veredicto verdadero, armado ausente re-verificado al cierre, cero órdenes en todo el tramo.

## Rollback

Documental: revertir el delta de esta entrada en el planner (las secciones quedan como historia si se prefiere marcar SUPERSEDED). Operacional: repoint `~/opt/echo-dev/current` a `releases/2ee61791…` + restart `echo-core-dev` (documentado en el BUILD.md del release). No revertir commits de terceros (lab-v4-shot2) ni claves ETCD.
