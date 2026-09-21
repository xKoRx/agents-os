---
type: change_log
schema_version: 1
scope: session
created: 2026-09-21
updated: 2026-09-21
area: "[[Personal]]"
project: "[[Echo — Producto Integrado]]"
application:
entities:
  - "[[Echo]]"
  - "[[Aranea]]"
related:
  - "[[Echo + Echo Forge — Environment Contract]]"
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

# 2026-09-21 — Echo DEV en Daedalus: gate systemd Core/Gateway (PARTIAL) + AS-BUILT delta

## Cambio

- **Tipo:** updated (Environment Contract §2/§5.1/§7) + created (agent-run) + updated (bitácora de `10-projects/Echo/Echo — Producto Integrado.md`).
- **Archivo(s):** `main/30-resources/aranea/07-integration/Echo + Echo Forge — Environment Contract.md`; `main/10-projects/Echo/Echo — Producto Integrado.md`; `main/80-agents/journal/agent-runs/2026-09-21-zcode-glm-5.3-flash-echo-dev-daedalus.md`; este change_log.
- **Fuera del vault (runtime Daedalus):** build de `xKoRx/echo` origin/master `5dd998f16aea7b2821f460188718d7a6d279829c` (worktree desechable en `/tmp/echo-dev-build/`), release instalada en `/home/kor/opt/echo-dev/releases/<sha>/` con `BUILD.md`, env files sin secretos en `/home/kor/opt/echo-dev/etc/`, unidades `~/.config/systemd/user/echo-core-dev.service` y `echo-gateway-dev.service` habilitadas.

## Motivo

- Mandato owner 2026-09-20: dejar Echo DEV (y componentes Forge aplicables) ejecutándose de forma persistente en Daedalus con gate `ECHO_CORE_GATEWAY_DEV_SYSTEMD_PASS`, sin tocar PROD, workers compartidos ni infraestructura Kafka/Flink, y documentando AS-BUILT por delta en el Environment Contract.

## Contenido

- Gateway DEV `RUNNING/PHYSICALLY_VERIFIED`: health 200, restart controlado y recuperación ante SIGKILL verificadas, degradación sin PG por diseño, boundary Forge ingest en fail-closed 503 (`forge_ingest_misconfigured=true`).
- Core DEV `BLOCKED` con causa precisa: credencial `echo_user` de PG DEV `.220` rechaza tanto el valor de ETCD como el fixture canónico del repo ⇒ drift server-side; owner action de rotación/alineación. Unidad queda enabled+inactive (stop intencional, sin restart loop).
- Aislamiento demostrado: namespace ETCD `/echo/development/` apunta al clúster Kafka DEV certificado (`.44:19091-19096`), PROD apunta a `.247-249:9092`, grupo `echo-core-v3` DEAD/0 miembros pre-arranque; wiring Flink DEV (`dev.echo.core.lab.aranea` → 192.168.31.161) documentado.
- Persistencia vía `systemd --user` + `Linger=yes` (sin sudo interactivo para unidades de sistema); reboot físico no ejecutado; `ROLLBACK_DOCUMENTED`.
- Forge: inventario sin mutación (`cmd/symphony`, `sqx/cmd`, `deployer/cmd`; namespaces `/symphony/development/` sin `echo/ingest/*`); `FORGE_RUNTIME_SCOPE_BLOCKED` para watcher/worker/workers compartidos; screen `deployer` pre-existente (ENV=production, 2026-09-17) intacto.

## Impacto

- Ningún acceso a PROD, sin reinicios de servicios ajenos, sin creación de VMs, sin duplicación de infraestructura ni de workers; ETCD/Flink/Kafka sólo lecturas RO. El gate es de ambiente: no certifica producto ni el join funcional Forge→Echo (backlog de certificación intacto).
