---
id: 2026-07-02-022
title: "DEFERRED — Documentar servicios individuales en Second Brain"
type: action
schema_version: 1
status: todo
status_detail: "PAUSADO 2026-07-02 por owner (prioridad única = Backup/DR). Material previo persiste en disco (proyecto + agente + 3 notas tier 0a); no se avanza hasta nueva orden."
severity: medium
icon: ⏸️
slug: 2026-07-02-022-deferred-service-docs
area: "[[Aranea]]"
project: "[[AGENTS OS]]"
created: 2026-07-02
updated: 2026-08-10
owner: me
aliases:
  - ticket 022
  - DEFERRED-SERVICE-DOCS
  - Service docs deferred
tags:
  - kind/action
  - area/aranea
  - project/agents-os
  - action/owner
related:
  - "[[SERVICIOS-DOCS-OWNER-PROJECT]]"
  - "[[agent-project-09-service-docs-rollout]]"
  - "[[30-resources/aranea/02-servicios/README]]"
  - "[[BACKUP-DR-OWNER-PROJECT]]"
---

# 2026-07-02-022 — DEFERRED-SERVICE-DOCS

## Descripción

Documentar los servicios individuales en Second Brain cuando el owner reactive esta acción diferida.

## Checklist

- [ ] Reactivar sólo por decisión del owner y completar la tarea documentada.

> [!warning] Status: **DEFERRED**
> **Trigger**: owner dijo el 2026-07-02 en sesión Backup/DR — "ojo con los servicios como argus, etcd, bases de datos, etcetc. anótalas por ahí como servicios disponibles. quizás estaría bueno documentar cada uno en el second brain, para tener el acceso a todo ahí bien enlazado. qué dices? (déjalo como tarea para más adelante)"

## Contexto

> [!danger] Verdad de fondo (definida por owner 2026-07-02)
> **Aranea NO es un homelab hobby. Es un datacenter para el sistema de trading algorítmico "echo".** Sin esto no hay homelab. Esta verdad define el scope del proyecto: documentar los servicios fundamentales que sostienen el sistema echo.

El catálogo actual de servicios en `30-resources/aranea/02-servicios/` agrupa por **categoría** (red, observabilidad, trading, ml-ia, bases-de-datos, etc.) pero **no tiene una nota individual por servicio**. Gap analysis inicial del owner el 2026-07-02 identifica **21 servicios tier 0** que sostienen el sistema echo:

- **Tier 0a — Infraestructura base** (3): opnsense (130), pi-hole (149), traefik (115). Sin estos NADA funciona.
- **Tier 0b — Storage** (1): truenas (145). Storage para TODOS los servicios.
- **Tier 0c — Cluster quorum crítico** (9): etcd cluster 5 nodos (101/147/154/155/156) + etcd-keeper UI (148) + kafka cluster 3 brokers (136/138/139). **etcd NUNCA menos de 3 nodos, idealmente 5.**
- **Tier 0d — Sistema echo** (10): mt4-real (124) + mt4-ftmo (133) + mt4-ttp (134) + mt4-demo (144) + echo (140) + postgresql (152) + mongodb (153) + argus (160, observabilidad) + docker-flink (126, stream processing consumer kafka) + docker-hasura (129, capa GraphQL sobre postgres).

Servicios fuera de scope (NO se documentan en este proyecto sin orden explícita): mcps, obsidian-sync, hasura, docker-observability, flink, emqx, frigate, homeassistant, ubuntu-dev, temporal, sqx-ulab-*, win-*, docker-kafka, etc.

## Tarea del owner (cuando se active)

1. **Aprobar inicio** del proyecto [[SERVICIOS-DOCS-OWNER-PROJECT]].
2. **Confirmar los 21 servicios tier 0** (o ajustar si alguno sobra/falta).
3. **Resolver secretos**: para servicios con secrets_refs, confirmar acceso vía Secret Zero.
4. **Definir plazo estimado** para el rollout (sugerencia: tier 0a en 1 sesión, tier 0b-c en 1-2 sesiones, tier 0d en 2-3 sesiones).

## Outputs esperados (cuando se active)

- 23 notas de servicio canónicas (tier 0a + 0b + 0c + 0d) en `30-resources/aranea/02-servicios/<servicio>.md` (o ubicación a definir).
- Template `70-templates/service-operational.md` validado.
- Cross-refs bidireccionales con `BACKUP-DR-DESIGN` y `02-servicios/README`.
- 0 secrets en plaintext en las notas.

## Acceptance criteria

- Las 23 notas siguen el template uniforme.
- Cada nota tiene: propósito, acceso, storage, secrets-refs, operación, observabilidad, incidentes, cross-refs.
- Las notas están enlazadas desde `02-servicios/README.md`.
- Validación: 0 secrets detectados por grep antes de commit.
- etcd cluster documentado explícitamente como "5 nodos mínimo, 3 nodos mínimo absoluto" (warning feo si baja).

## Bloquea

- **NADA operacionalmente crítico**. Es documentación, no ejecución.
- Cierra un gap de visibilidad pero no bloquea ningún proyecto activo.

## Riesgos si no se resuelve

- Servicios "huérfanos" sin procedure conocido (ej. argus, echo) quedan como cajas negras.
- Si el owner cae o se ausenta por tiempo prolongado, nadie (humano o agente) puede operar Aranea efectivamente.
- El sistema Backup/DR (F-08 segregación cloud, secrets_refs) no puede auditar qué servicios tocan qué secrets sin docs por servicio.

## Notas

- **NO consumir tiempo del owner ahora**. El proyecto está deferred por instrucción explícita.
- Las decisiones de diseño (template, ubicación, política de secretos) ya están en [[SERVICIOS-DOCS-OWNER-PROJECT]] — solo falta trigger.
- El catálogo existente `02-servicios/README.md` sigue siendo truth-of-record hasta que se active este proyecto.

## Referencias

- [[SERVICIOS-DOCS-OWNER-PROJECT]] — proyecto deferred
- [[agent-project-09-service-docs-rollout]] — subproyecto agente
- [[30-resources/aranea/02-servicios/README]] — catálogo actual por categoría
- [[30-resources/aranea/02-servicios/ml-ia]] — ejemplo de doc por categoría (con gaps visibles: argus, echo "no documentado")
- [[30-resources/aranea/02-servicios/bases-de-datos]] — ejemplo de doc por categoría

## Source files

- `/home/hermes/aranea/topology/services.md` — fuente original del catálogo
- `/home/hermes/aranea/topology/inventory_2026-07-02.json` — fuente fresca de VMIDs/nodos/status

## Captured

Ticket creado 2026-07-02 como materialización formal del comentario del owner en sesión de formulario Backup/DR. Deferred por instrucción explícita — no se ejecuta hasta nueva orden.
