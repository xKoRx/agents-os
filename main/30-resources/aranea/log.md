# Aranea — Bitácora (Resource Wiki)

Append-only, cronológico. Formato: `## [YYYY-MM-DD] <op> | <detalle>` con `<op>` ∈ `ingest | query | lint`.

## [2026-08-08] lint | Activación explícita bajo el contrato Resource Wiki

- Se agregó la bitácora raíz requerida por el dominio activo.
- El historial anterior permanece en las páginas, tickets y change logs originales; no se fabricaron entradas retroactivas.
- El subíndice legacy de Backup/DR se normalizó al casing canónico `03-storage/backup-dr/00-index.md` y sus referencias vivas fueron ajustadas.

## [2026-08-10] ingest | migración T6.3 de legado Aranea → schemas vigentes

- Se clasificaron las páginas canónicas: documentación de inventario a `doc`, runbooks operacionales a `runbook` y tickets históricos a `action`.
- Se preservó el contenido histórico y se agregó metadata/routing contractual; las afirmaciones volátiles permanecen sujetas a verificación.

## [2026-08-11] lint | Auditoría base de AGENTS OS Fase 4

- El runbook transversal de migración HTTPS quedó cubierto por el índice raíz; `backup-dr/` se conserva como subíndice que comparte esta bitácora; Graphify quedó limpio y actualizado.

## [2026-09-11] ingest | Capability plane MCP Aranea

- Se actualizó `02-servicios/ml-ia.md` con el contrato operativo MCP verificado: PostgreSQL Echo PROD RO (`echo`/`mcp_echo_prod_ro`), DEV RW (`echo-develop`/`mcp_echo_dev_rw`), SSH certificado y routing Mongo Forge PROD RO / DEV RW; Mongo queda pendiente de smoke funcional posterior al restart del cliente después de corregir sus bearer env vars.

## [2026-09-13] ingest | Kafka/Flink DEV MCP y runtime Echo DEV

- `02-servicios/data-streaming.md` quedó actualizado con Kafka DEV certificado y con Flink/StateFun DEV vigente en `docker-echo-dev`; el antiguo `docker-flink` se conserva sólo como snapshot histórico.
- `02-servicios/ml-ia.md` quedó alineado con el capability plane `:3000`–`:3008`, nueve capabilities certificadas, `aranea-flink-dev-admin` y el profile host/runtime `docker-echo-dev-operator`.
- Flink DEV se cerró con source-of-truth Portainer stack `1`, config persistente bajo `/root/statefun`, control plane MCP separado del host/runtime plane y PROD explícitamente diferido.

## [2026-09-21] ingest | Cierre documental Backup/DR — mecanismos vigentes y preflight evergreen

- `03-storage/backup-dr/BACKUP-DR-RUNBOOK.md`: warning de estado actualizado al 21sep (certificados: R1/R1.5 + MP-01 A0/A1/A5 + G1A/G1B + piloto R2); §0.1 nuevo con los 6 mecanismos vigentes, su última verificación y notas de operación (timers Persistent vs trigger absoluto — el run R2 del 21sep se perdió por apagado de hermes; tar-race de second-brain con corrección gated T-21b).
- `03-storage/backup-dr/BACKUP-DR-CHECKLIST.md`: §1.1 nuevo — preflight evergreen de intervención en ventana (query sin filtro temporal, conservación previa verificada, failure domains, timers armados, canal de validación independiente, ABORT escritos, duraciones medidas), derivado de las lecciones 19-21sep.
- Contenido del proyecto (bitácora, continuidad y erratas de las notas técnicas) no se duplica aquí: ver [[ARANEA-CONTINUIDAD-Y-VENTANA-25-26-SEP]] y change log `80-agents/journal/change-logs/2026-09-21-cierre-documental-integral.md`.

## [2026-09-21 noche-3] hardening | RÉPLICA pool0→pool2: mecanismo nativo zettarepl LOCAL (errata 404→401)

- `03-storage/zfs-replication-runbook.md`: reescrito al **stack NATIVO de replicación TrueNAS 25.04.1** (plugin `replication` → motor `zettarepl`, transporte LOCAL). La afirmación "/replication 404" de la noche-2 quedó refutada: la ruta existe (401 sin auth = auth requerida) y el código instalado declara `transport ∈ {SSH, SSH+NETCAT, LOCAL}`. El plan cron+script zfs queda DESCARTADO.
- Números corregidos en la SPEC del proyecto (fuente canónica): envío inicial 2,35T base `refer` (ledger auditado; apps 14,1G, iscsi 381G); histéresis `usedbychildren` explica el gap 4,08T zpool vs 2,15T datasets (442 snapshots legacy de `pool2/backup`); CAPACITY_GO con margen post-full ≥1,71T; horario 04:45/04:50 fundado en dependencias reales (timers hermes); gates ampliados a **G-REP-0..5** (fixture efímero + canal de alertas; `smtp=false` medido).
- Detalle de decisiones/aritmética en [[POOL0-TO-POOL2-REPLICATION-SPEC]] y change log `80-agents/journal/logs/2026-09-21-redireccion-storage-backup-dr.md` (addendum noche-3). No se duplica aquí.

## [2026-09-21] ingest | Front DEV (echo-backoffice) en Daedalus

- [[Echo + Echo Forge — Environment Contract]] ganó §5.7: `echo-front-dev.service` (systemd --user, `vite preview :4173`) sirviendo el build del backoffice con endpoints DEV inyectados por proceso (Gateway `.161:8090`, Hasura DEV `.75:8080`); allowlist CORS DEV agregada en ETCD y Gateway DEV reiniciado de forma controlada (`forge_ingest_misconfigured=false`, Core intacto).
- Gap declarado: Hasura DEV sin auth webhook hacia `/api/v1/auth/hasura` ⇒ front sirve shell con datos en cero hasta cableo owner. Run attributable en `80-agents/journal/agent-runs/2026-09-21-zcode-glm53flash-echo-front-dev.md`.
