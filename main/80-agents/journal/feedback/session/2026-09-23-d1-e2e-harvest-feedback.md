---
type: session_feedback
schema_version: 1
created: "2026-09-23"
updated: "2026-09-23"
area: "[[Aranea]]"
project: "[[The Lab]]"
entities:
  - "[[Echo]]"
related:
  - "[[M — Reusable Verification and E2E Harvest D1]]"
severity: low
category: environment
load_policy: manual
indexable: false
tags:
  - kind/feedback
  - scope/session
---

# Feedback — D1 E2E Harvest (2026-09-23)

## Observaciones

1. **Puertos 154xx contaminados por instancias postgres huérfanas.** La máquina arrastra decenas de postmasters de sesiones anteriores escuchando en 15433–15499; un harness que fija un puerto y silencia el error de `pg_ctl start` (o arranca sin `-w`) termina con `createdb`/`psql` conectándose a una instancia AJENA, con síntomas engañosos (`FATAL: role "echo_user" is not permitted to log in` en vez de connection refused). Costó una corrida completa de gates malgastada. Regla extraída: sondear puerto libre (`/dev/tcp` probe) antes de arrancar, `pg_ctl -w` sin silenciar stderr, y tratar un FATAL de autenticación tras un arranque local como señal de "instancia equivocada", no de credenciales. El `run.sh` de la suite E2E D1 ya incorpora el patrón; los otros harnesses de la máquina no.
2. **La convención E2E por SPEC ya tiene primer adoptante.** `v3/e2e/specs/THE-LAB-D1-ECHO-FOUNDATION/` demuestra el patrón end-to-end (paquete Go aislado dentro del módulo `v3/e2e`, manifest README con "qué NO prueba", run.sh con PG desechable, skip limpio sin DATABASE_URL, enlazar en vez de duplicar cuando la regresión del paquete owner es más fuerte). Si la próxima SPEC (D2) adopta la misma carpeta, merecería promoverse de convención a patrón documentado en el Environment Contract del repo echo.
3. **`go test ./...` en `v3/e2e` pisa ~14 tests rojos preexistentes** (framework copy-flow V2, fallback probable de drift del producto). Cualquier gate o CI que use ese comando como aserción dura fallará por ruido ajeno; los gates deben apuntar a `./specs/...` o clasificar la preexistencia (higiene owner pendiente, ya registrada en doc M).

## Lo que funcionó bien

- La matriz de disposition contra cobertura permanente ANTES de escribir código evitó mover los 30 tests mecánicamente: 15 funciones nuevas retuvieron todo el valor, y las equivalencias quedaron demostradas por enlace (test permanente → invariante), no por fe.
- Reutilizar el harness canónico `d1_foundation/run.sh` desde el run.sh de la E2E (en vez de re-implementar la orquestación de migraciones) dejó una sola fuente de verdad para aplicar 064.
