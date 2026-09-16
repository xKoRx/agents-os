# Session feedback — 2026-09-16 — E-02 CLOSED (sesión 2)

## Qué pidió el owner

Completar ACs pendientes de E-02 (AC-11, AC-12, AC-01, verifier) y obtener veredicto del lane, sin repetir los physical gates ya certificados, sin abrir GAP-ECHO-010 ni E-06.

## Qué se hizo

1. **Contrato recargado desde el branch** (`specs/FEAT-CONTROL-SAFETY-JOURNAL-RECOVERY-E2/` @ `f7ddea18` en repo de Daedalus): AC-11 = outage PG real ⇒ TRANSIENT ⇒ convergencia sin duplicado; AC-12 = kill -9 del core Go (compose StateFun develop + PG real) antes/después de persistir ⇒ cero pérdida, cero doble fila; AC-01 = vite build + grep de dist + doble-check con valor real.
2. **Corrección de target owner (importante):** el primer intento colocó `echo-core` en `.75` (infra DEV). El owner lo detuvo y fijó la runtime topology FROZEN: **Daedalus `.161` = runtime DEV de Echo; `.75` = infra soporte, nunca runtime Echo**. El intento en `.75` fue revertido completamente (proceso kill -9, hosts byte-identical, binarios/log borrados, 0 sesiones). Luego el owner actualizó el DNS canónico (Pi-hole): `dev.echo.core.lab.aranea → 192.168.31.161`. Regla durable registrada: "Application runtime follows declared topology; infrastructure proximity is never authority to colocate product components."
3. **Hallazgo técnico de targeting:** los containers de Flink en `.75` NO leen `/etc/hosts` del host (Docker DNS 127.0.0.11 → Pi-hole). Un hosts-fixture en el host no alcanza a los containers. Con el DNS canónico actualizado por el owner, la resolución fue natural (sin `extra_hosts`, sin tocar `urlPathTemplate`).
4. **AC-12 PASS:** kill -9 del binario core Go (compilado @ `f7ddea18`, sha `00240dd1…`) en Daedalus. Ventana post-persistencia (redelivery ⇒ 1 fila/1 id, sin doble fila) y ventana pre-persistencia del close (close publicado con core DOWN ~30s; Flink restart ×2; redelivery ⇒ close aplicado exactamente 1 vez). Replay tardío del OPEN → `OPEN_AFTER_CLOSED` → cuarentena durable (unique index verifica dedupe) → ACK → loop converge. 0 publishes a `echo.commands.*`.
5. **AC-11 PASS:** outage real en PG 17.6 de DEV vía ACCESS EXCLUSIVE lock sobre `echo.trade_journal` (~100s, blast radius = 1 tabla; NO se detuvo el PG compartido). Durante outage: 5× error transient retornado a StateFun (clasificación `persistence_error`, 0 quarantine, 0 fila parcial); tras liberar: convergencia a exactamente 1 fila, sin duplicado.
6. **AC-01 PASS:** vite build real (43 assets) + `check-frontend-bundle.sh` PASS + 4 greps independientes limpios + doble-check con el valor REAL del admin secret DEV (sha16 `8a36217243c11629` como evidencia; valor jamás impreso; transferencia stdin-only).
7. **Verifier independiente PASS (V1–V5):** superficie separada, read-only, sin secretos. Encontró 2 residuales: topics fixture `e02cert-gate2{,b}-20260915` de la sesión anterior (borrados) y un bug SQL en el propio verifier (corregido, documentado, no maquillado).
8. **KEEP:** 062 `journal_quarantine` aplicada a `.220/echo-develop` (additive, contractual del branch; rollback = down, hoy vacía). **REMOVE:** filas fixture (0 residuo), core detenido, bearers shredded.

## Qué salió mal / lecciones

- Colocar el runtime en `.75` fue un error de inferencia de topología ("proximidad de infra ≠ autoridad"): corregido por el owner antes de ampliar el daño; rollback completo y documentado.
- El intento de fixture DNS por hosts en `.75` no llega a containers (resolver embebido de Docker) — verificar el resolver efectivo del consumidor antes de elegir el mecanismo.
- Los ingresses journal de StateFun son `startupPosition: earliest`: core sin tabla 062 + replay conflictuado = retry-loop infinito (el ACK depende de InsertQuarantine). Orden PLAN §3 (migrar 062 antes del deploy) es crítico en PROD.

## Estado resultante

`E02 CLOSED` (software). Pendiente de closure formal: CONTROLLED INTEGRATION a master + AC-18 (rotación prod, owner). **E-06 desbloqueado** (no iniciado). GAP-ECHO-010 sigue P1 paralelo, no tocado.

## SoT

change_log `2026-09-16-e02-closed` · bitácora E-02 · [[Echo — Access & Physical Capability Matrix]] · [[ACCESS-CERTIFICATION]] (run 2026-09-16 (b), runtime topology FROZEN).
