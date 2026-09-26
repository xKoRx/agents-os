---
type: skill
schema_version: 1
name: echo-prod-deploy
description: Despliegue autorizado de Echo a PROD (binarios .71 vía deploy-prod.sh canónico, BD .220/echo, Hasura .48, ETCD production, front nginx) con orden validado, verificación física y rollback. SOLO se carga y ejecuta cuando el owner pide explícitamente usar esta skill; nunca proactiva, nunca para DEV ni Forge.
scope: area
created: "2026-09-25"
updated: "2026-09-25"
entities:
  - "[[Echo]]"
  - "[[Aranea]]"
related:
  - "[[Echo + Echo Forge — Environment Contract]]"
  - "[[30-resources/agents/skills/aranea-agent-dev/SKILL.md|aranea-agent-dev]]"
  - "[[30-resources/agents/skills/echo-production-operational-audit/SKILL.md|echo-production-operational-audit]]"
  - "xKoRx/echo:deploy-prod.sh"
  - "xKoRx/echo:build_v3.sh"
aliases:
  - echo prod deploy
  - despliegue echo produccion
  - rollout echo prod
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/skill
  - scope/area
  - area/aranea
  - area/echo
  - action/deploy
---

# echo-prod-deploy

## Purpose

Ejecutar el paso a producción de Echo (D1+/Lab V3 en adelante): delta de BD en `echo` @ .220, seed ETCD `/echo/production/`, metadata Hasura PROD, builds desde un SHA de `origin/master` y despliegue físico en `.71` mediante `deploy-prod.sh`, con verificación física y rollback. Skill owner-gated: es la ÚNICA vía autorizada para mutar PROD Echo desde el agente.

## Trigger Guard (obligatorio, antes de cualquier lectura o acción)

- **Carga/ejecución SOLO cuando el owner pide explícitamente usar esta skill** (por nombre `echo-prod-deploy` o referencia inequívoca tipo "usa la skill de deploy a prod de Echo"). Ante ambigüedad, preguntar y esperar; no inferir.
- **NO habilitan la skill:** "pasa esto a prod" sin nombrarla, trabajo DEV, actualizaciones de config, propuestas proactivas del agente, continuidad de un rollout previo sin nueva autorización.
- Cada **corrida** exige además: (1) autorización owner vigente para esa ventana, (2) secretos de la corrida entregados por el owner (admin secret Hasura PROD, password/acceso SSH `.71`, acceso escritura BD), (3) SHA objetivo explícito. Leer esta skill no concede poderes ni reutiliza autorizaciones anteriores.

## Minimal Read

1. Esta skill.
2. [[Echo + Echo Forge — Environment Contract]] (modelo DEV/PROD, gates, §1).
3. Estado vigente del último rollout: entidad [[Echo — Producto Integrado]] (§Estado y realidad) y memoria interna del agente (delta aplicado, SHAs, backups).
4. Los scripts canónicos del repo al SHA objetivo: `xKoRx/echo:deploy-prod.sh`, `xKoRx/echo:build_v3.sh` — leerlos antes de ejecutarlos; nunca asumir su contenido.

## Procedure

1. **Gates de corrida.** Confirmar Trigger Guard, secretos y acceso (SSH `.71`, escritura PG, admin secret Hasura). Resolver SHA objetivo (`origin/master`, builds `vcs.modified=false`). Ejecutar pre-vuelo RO: healths, units en `.71`, snapshot de puertos (esperado: core :9090, gateway :8090, functions legacy :8080), y detección de idempotencia (qué delta ya está aplicado: objetos BD, keys ETCD, tracking Hasura).
2. **Delta BD** (`echo` @ .220, como `echo_user`): extraer migraciones **verbatim** del SHA objetivo; precheck fail-closed (si el estado difiere del esperado: STOP de la mutación y reportar); backup completo previo; aplicar una transacción por migración en orden; **suplementos certificados** (ver Hard Rules 6-7); postcheck + contraste de contenidos contra backup. Si `4aad647b` sigue sin fusionar a master, los suplementos CHECK plataforma (`MetaTrader5/4`) y GRANT UPDATE (4 tablas identity) son obligatorios.
3. **Seed ETCD** `/echo/production/`: tokens `gateway/auth/{front_read,config_operator,control_operator,service_hasura_webhook}_token` (aleatorios, archivo canónico local mode 600 fuera del vault) + `gateway/cors_allowed_origins`. Verificar con lecturas sin valor (PRESENT/bytes). **Converger ETCD desde el archivo canónico** si hay copias rsync de por medio; tras re-seed, restart del gateway (lee tokens al boot).
4. **Metadata Hasura PROD**: export CLI (exige `config.yaml` en cwd; el export es formato v3 con **2 sources** — tocar SOLO `echo_prod`); merge **aditivo** repo+export (jamás `metadata apply` directo: el repo no contiene event_triggers); strip de permisos `role: admin` (v2.38 los rechaza); aplicar por HTTP `replace_metadata` con wrapper `version: 2`; post: `is_consistent=true`, los 6 event_triggers intactos, tablas nuevas expuestas como `echo_*` en GraphQL.
5. **Builds** (worktree limpio al SHA): `build_v3.sh` o equivalente directo → `v3/bin/echo-{core,gateway,lab-worker}-v3`; front `npm run build` con `VITE_HASURA_ENDPOINT`, `VITE_GATEWAY_ENDPOINT` PROD y secretos owner horneados (`VITE_HASURA_ADMIN_SECRET`, `VITE_GATEWAY_CONTROL_TOKEN`) — secretos jamás en vault ni logs.
6. **Despliegue `.71`**: `deploy-prod.sh` por scopes en orden **core → gateway → lab-worker → front** (requiere `DEPLOY_PASS`; reemplazo atómico `.new`→`mv` + restart systemd). Backup previo de binarios (`/home/kor/echo-backup-*`) y del dist (`tar` de `/var/www/echo`). **El scope `echo-functions` NO existe y NUNCA se despliega** (Hard Rule 5).
7. **Verificación física**: puertos idénticos al snapshot pre (9090/8090/8080), units activas, healths 200, journals con `env=production` y `etcd_prefix /echo/production/`, republish `200` con Bearer `control_operator` y `401` sin token, GraphQL expone `echo_lab_curves`/`echo_canonical_operations`, lab-worker timer activo (su corrida `SUCCEEDED` con `lab_curves=0` es correcto mientras no haya historia importada).
8. **Cierre**: registrar en entidad y memoria (SHAs, backups, estado, pendientes); watch 72 h (recencia `lab_job_runs`, bridges ≥17/18, próxima señal de estrategias con mapping); recordatorio owner de **rotar secretos usados** en la corrida.

## Output

```text
Deploy:              <SHA> → PROD | BLOQUEADO — <motivo>
Scopes:              <core|gateway|lab-worker|front aplicados>
Verificación:        puertos/healths/auth/Hasura/lab — PASS|FAIL por ítem
Rollbacks usados:    <ninguno | binarios/front/BD/metadata + path>
Backups:             <rutas>
Pendientes owner:    <rotación, watch 72h, deuda>
```

## Hard Rules

- Sin pedido explícito del owner (Trigger Guard) no se carga ni se ejecuta; la skill no delega ni auto-invoca.
- `go test ./...` PROHIBIDO contra ETCD real mientras `4aad647b` no esté en master (los seed tests sobrescriben `/echo/production/postgres/password`).
- PROD nunca es fallback de DEV; todo delta se prueba en DEV antes.
- NUNCA desplegar `echo-functions`: su unidad no define `ENV` ⇒ el binario nuevo resuelve `development` y bind `:9090` (crash-loop); la arquitectura vigente aloja StateFun **en el proceso core**; el binario legacy queda en `:8080` intacto.
- NUNCA `hasura metadata apply` directo del repo (borraría los 6 event_triggers de config-propagación); sólo merge aditivo sobre `echo_prod`; las tablas internas 061–063 no se exponen por diseño.
- CHECK plataforma sin el suplemento rechaza `MetaTrader5` ⇒ handoff Forge muere; sin GRANT UPDATE en las 4 tablas identity, los FK por `KEY SHARE` fallan. Ambos son obligatorios mientras no vengan en master.
- Ningún secreto en vault, logs ni salida de comandos; verificar tokens por presencia/bytes, jamás por valor.
- Ante cualquier desvío del estado esperado: detener la mutación afectada, reportar y esperar decisión; rollback documentado antes de reintentar.
