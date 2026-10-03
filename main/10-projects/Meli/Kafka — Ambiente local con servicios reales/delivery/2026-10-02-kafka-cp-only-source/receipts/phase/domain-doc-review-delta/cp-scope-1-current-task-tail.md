## CP-SCOPE-1 — prioridad CP del owner (2026-10-02)

- [x] Agregar scope CP-only a lifecycle/provenance de Sandbox con regression controls y mantener defaults ecosystem/legacy.
- [x] Rechazar recibos CP-only en familias ecosystem y documentar comando CP independiente.
- [x] Revisión independiente de aislamiento, ownership/cleanup y regresiones; ejecutar controles y task discovery/preflight real sin falsificar negocio.
- [ ] Guardar checkpoint/knowledge/commits CP-only y recibos de revisión de fuente.
- [ ] Ejecutar la suite física CP completa y repetirla desde checkout limpio: primero renovar Fury (`SANDBOX_FURY_LOGIN_REQUIRED` actual), después revalidar el clone propio que históricamente devolvió403; resolver permiso si persiste. Fuente/controles no cierran esta aceptación.

- [x] Corregir P2 preexistente de contexto del EXIT trap CI en Bash3.2 y agregar regresión de funciones reales sin backend; conservar retención UNKNOWN e independencia del parent.

CP-SCOPE-1 source controls: coordinator `validateRealE2eHarness`72 PASS and CP compile PASS; independent source/metadata v2 PASS,0 drift/0 findings after preserving baseline and bare-variable REDs. These checkmarks certify only the named source/neutral controls. Full business run, current Toolkit server contract, clean repeated reproduction and actual corporate CI job remain NOT_EXECUTED. Current auth gate is Fury login required; the former clone403 must be rechecked after renewal.
