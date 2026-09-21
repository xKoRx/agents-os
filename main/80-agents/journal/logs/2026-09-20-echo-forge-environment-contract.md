---
type: change_log
schema_version: 1
scope: session
created: "2026-09-20"
updated: "2026-09-21"
area: "[[Echo]]"
project: "[[Echo — Producto Integrado]]"
application:
entities:
  - "[[Echo + Echo Forge — Environment Contract]]"
  - "[[aranea-agent-dev]]"
related:
  - "[[Echo — Live Platform V1]]"
  - "[[Echo Forge — Factory V2 Completion]]"
aliases: []
confidence: verified
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-09-20 — Echo Forge environment contract

## Cambio

- **Tipo:** created / updated.
- **Archivos:**
  - `30-resources/aranea/07-integration/Echo + Echo Forge — Environment Contract.md` — created, source canónica de separación DEV/PROD y estado TARGET vs AS-BUILT.
  - `30-resources/agents/skills/aranea-agent-dev/SKILL.md` — updated para lectura obligatoria scoped en cold start/entity swap Echo/Forge, sin modificar bootstrap global.
  - `80-agents/journal/logs/2026-09-20-echo-forge-environment-contract.md` — este registro.

## Motivo

Evitar que coding agents confundan entornos, interpreten un clon Windows o workers compartidos como DEV aislado, o recurran a PROD porque no haya infraestructura DEV física certificada. Mantener mapa factual breve en Sistema 2 y procedimiento de carga en skill federada, sin duplicar runbooks.

## Fuentes usadas

- Decisiones owner 2026-09-20: Daedalus como DEV, `192.168.31.132` como Windows DEV clonado, workers actuales compartidos, infraestructura de datos DEV/PROD existente.
- `Echo — Producto Integrado`, `Echo — Access & Physical Capability Matrix`, `Daedalus — Development Agents MCP Access & Gaps` y `aranea-ssh-mcp` para semántica de estados y acceso.
- `agent-constitution`, `agents-os-bootstrap`, `schema-contract`, template `70-templates/doc.md`.

## Resolución aplicada

- Un contrato delgado con ambientes, aislamiento, hitos y enlaces; procedimientos exactos quedan en runbooks.
- DEV default, PROD nunca fallback; mutaciones ambiguas bloqueadas.
- Al crear el contrato (2026-09-20) no se declaró `dev-win`, SQX Daedalus ni Core/Gateway DEV físicamente verificados sin reporte AS-BUILT.
- Alcance de escritura únicamente `xKoRx/agents-os`. No editar `AGENTS.md` de Echo/Symphony ni actualizar datos runtime sin evidencia nueva.

## Validación

- Crear contrato y actualizar skill mediante GitHub Contents API con SHA existente.
- Verificar lectura de archivos resultantes y referencias cruzadas; no se ejecutaron smokes de infraestructura ni validador local de esquema desde el vault montado.

## Compartibilidad

- **Scope:** local.
- **Redacción revisada:** sin passwords, tokens, claves privadas o rutas absolutas personales; IP designada no es credencial.

## Rollback

- Revertir commits del contrato y la skill mediante Git, preservando modificaciones concurrentes y verificando sus SHAs. No revertir estado de infraestructura: no se ejecutaron mutaciones de hosts.

## Delta 2026-09-21 — Informe Hermes recibido y reconciliación concurrente

**Fuente:** informe final de Hermes del mandato Echo + Echo Forge DEV Environment, fechado 2026-09-20 y aportado por el owner en conversación el 2026-09-21. No se pudieron leer aquí sus logs primarios. **Resultado reportado:** `PARTIAL`, G0 PASS, G1 PASS, G2/G3 PARTIAL. La ruta de evidencia comunicada fue `~/aranea/work/echo-dev-20260920/G0-G1-informe.md`, descrita por Hermes como pendiente de completar con G2/G3; no declarar evidencia durable completa.

- **Windows:** VMID 125/hades, `192.168.31.132`, hostname nuevo `DEV-WIN`, clon MT4/MT5 contenido y terminales heredados detenidos según Hermes. SSH Windows por clave, profiles MCP `dev-win` viewer y `dev-win-operator` no-admin, host key propia, prueba negativa viewer y ciclo reversible operator reportados; perfiles anteriores sin drift. Firewall del informe permite `192.168.31.0/24`, no limitarlo verbalmente a `mcps`/management hasta endurecerlo. Segregación de credenciales heredadas y consumidor ZCode/Codex individual requieren comprobación separada; ningún secreto se copia al vault.
- **MT5:** portable `C:\MT5\DEV-Echo`, MetaEditor y compilación MQ5→EX5 0 errores con SHA prefijo registrado por Hermes. Tester/HTM PENDING porque el terminal bajo sesión SSH/servicio falla `MDI create failed`: requiere sesión interactiva autorizada; el EX5 compilado NO prueba backtest. `sqx-mt5-worker.exe` seguía en transferencia al cierre: no llamarlo worker operativo.
- **Forge/SQX:** Go y cuatro binarios compilados según Hermes; `sqx-worker` realizó arranque transitorio con Temporal namespace `sqx-dev`, luego salió con código 1 por ausencia de `sqcli` y necesidad de licencia comercial. No confundir build/conectividad con worker residente o queue aislada. Flota Zeus/Hera/Kronos se reporta intacta.
- **Echo:** informe Hermes más antiguo decía Core compilado pero pendiente de arranque; el propio contrato fue actualizado por otra sesión de fecha posterior, §5.1, con Core/Gateway `RUNNING/PHYSICALLY_VERIFIED`, fuente `5dd998f1…`. Conservar ese estado posterior, no solicitar `systemctl --user start echo-core-dev` sobre una unidad ya activa.
- **Integración:** al corte Hermes no hubo smoke E2E. El contrato más reciente §5.2 registró 503 del ingest y CERT-E04-01/F04-03 BLOCKED; otra edición concurrente añadió §5.3 con fixes en source Echo `2360369c…` / Symphony `a2321cc…`, ETCD DEV y migración parcial 061, **sin redeploy del Gateway**: 503 y golden/recertificación pendientes. Los seed tests peligrosos quedaron corregidos en la rama nueva según §5.3, pero los binarios residentes aún corren el baseline antiguo; no ejecutar suites peligrosas contra ETCD real del checkout viejo.

**Conflicto de escritura:** intento de actualizar el contrato principal usando blob SHA `bf634829…` fue rechazado por GitHub `409` porque otro agente lo actualizó a `2ce659e7…` durante la edición. **No se forzó overwrite, ni se publicó el reemplazo preparado.** Este change_log conserva las diferencias de Hermes sin adjudicarle certificación independiente. Reconciliar e integrar el delta en el contrato con un único editor y SHA fresco, preservando por completo §5.1–5.3 y cualquier cambio posterior; no restaurar estados obsoletos del reporte anterior.

**Estado de este delta:** informe recibido y preservado en change_log; **integración en la nota canónica pendiente de reconciliación**. Ninguna mutación de infraestructura ni de repositorios Echo/Symphony se ejecutó aquí.
