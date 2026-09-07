---
type: project
schema_version: 1
owner: agent
root: false
status: active
cssclasses:
  - wide
priority: P1
area: "[[Personal]]"
parent: "[[AGENTS OS]]"
sprint:
start: 2026-08-11
due:
progress: 0
repo:
jira:
prs:
aliases:
  - AGENTS OS Fase 4
  - AGENTS OS Audit Backlog
related:
  - "[[Economía de Tokens]]"
  - "[[token-economy-indexing-architecture]]"
tags:
  - area/personal
  - kind/project
  - project/agents-os
created: 2026-08-11
updated: 2026-08-11
---

# AGENTS OS - Fase 4

> [!info]+ Backlog de evolución
> **Padre:** [[AGENTS OS]] · **Owner:** agent · **Estado:** active · **Prioridad:** P1 · **Progreso:** 0%
>
> Esta fase nace deliberadamente como contenedor de backlog. No hay ejecución iniciada, gates activos, tareas WIP/Review ni compromiso de implementar todo el listado; cada ítem debe priorizarse con evidencia antes de pasar a WIP.

## 🎯 Objetivo

- Mantener un backlog canónico, auditable y extensible para la siguiente evolución de AGENTS OS sin reabrir trabajo ya aceptado de Fases 2 y 3.
- Preservar la ideología vigente: bootstrap único, autoridad separada, define == implement, economía de tokens sufficiency-first, una fuente por hecho, Markdown como verdad y Graphify como índice derivado.

## 📊 Estado actual

- **Baseline 2026-08-11:** auditoría completa de ideología, componentes, skills core, memoria pública, Resource Wiki, schema, índices, Graphify, Doctor y Context Router.
- **Correcciones inmediatas aplicadas:** lifecycle `deprecating` incorporado al schema de aplicaciones; acceso de workers centralizado por instrucción del owner en un único `credentials.env` plaintext, excluido de Graphify, con wrapper común `echo-forge-worker`; artefacto `*.md</path>` recuperado como Markdown canónico; locators `file:///` removidos; índices/logs activos reconciliados; perfiles de Codex, Claude Code y Cursor corregidos; Graphify reindexado.
- **Salud mecánica de entrada:** schema `45 tipos / 44 templates / 5 fixtures / 0 errores`; strict y gate global `0/0`; Doctor `HIGH=0 / MEDIUM=0 / LOW=0`, startup≈6000; Context Router `14/14`, 0 misses y precision proxy 100%; Graphify `5267 nodes / 6355 edges`, con `trash=0 / archive=0 / json=0`; el clustering de comunidades es variable y no es gate; el backlog comienza con 0 tareas ejecutadas.
- **Principio de operación:** agregar libremente nuevos ítems como To Do; mover sólo uno a WIP cuando exista prioridad y alcance verificable.

## ✅ Tareas

> [!note]+ Fuente única del backlog
> Todas las tareas internas son `#owner/agent` y viven sólo aquí. El cockpit padre mantiene una única tarea puente `#owner/me #type/supervision`, que el agente no marca Done.

### P0 — Seguridad y autoridad

- [ ] Reemplazar el `credentials.env` plaintext por un secret manager y rotar la credencial de workers cuando el owner lo autorice; hasta entonces no cambiar la solución ni duplicar el secreto #owner/agent #type/admin #area/personal #waiting ⏫
- [ ] Agregar un gate que detecte secretos literales y patrones de credenciales en memoria pública sin imprimir valores sensibles #owner/agent #type/dev #area/personal ⏫
- [ ] Reconciliar [[token-economy-indexing-architecture]] con el Context Router vigente: entrada por intención, sin waterfall obligatorio y sin verbos tipados del body como contrato actual #owner/agent #type/dev #area/personal ⏫

### P1 — Runtime y multisuperficie

- [ ] Convertir `agents-os-session-close` en orquestador puro que invoque distillation, feedback, registro de run y Graphify sin duplicar sus procedimientos #owner/agent #type/dev #area/personal 🔼
- [ ] Extender instalación y validación desde el registro canónico a Codex, Claude Code, Cursor y Antigravity mediante adaptadores y capability checks explícitos #owner/agent #type/dev #area/personal 🔼
- [ ] Ejecutar un forward-test real de `agent_run` por cada superficie y modelo expuesto; no crear evidencia ficticia #owner/agent #type/testing #area/personal 🔼
- [ ] Definir una metodología de comparación superficie×modelo que controle tamaño de muestra, complejidad, evaluator, rework y sesgo de autoevaluación #owner/agent #type/research #area/personal 🔼
- [ ] Sincronizar `80-agents/skills/INDEX.md` y `public-vs-internal-memory` con carga scoped/lazy y feedback event-driven #owner/agent #type/dev #area/personal 🔼

### P1 — Observabilidad, Doctor y Resource Wiki

- [ ] Ampliar Doctor para detectar nombres anómalos fuera de `*.md`, locators client-owned, secretos y divergencia entre checks documentados y automatizados #owner/agent #type/dev #area/personal 🔼
- [ ] Derivar o validar desde disco el registro de dominios activos de Resource Wiki para evitar una lista manual paralela #owner/agent #type/dev #area/personal 🔼
- [ ] Compactar `30-resources/aranea/00-index.md` como raíz de subíndices y extraer handover, decisiones, métricas y comandos a artefactos canónicos #owner/agent #type/dev #area/personal 🔼
- [ ] Resolver contractualmente si un subíndice `status: active` comparte el log raíz o declara dominio independiente, alineando Doctor y Resource Wiki #owner/agent #type/dev #area/personal 🔼
- [ ] Agregar métricas de salud del grafo que distingan huérfanos reales, archivos raíz, headings y supernodos sin confundir volumen con defecto #owner/agent #type/research #area/personal 🔼

### P2 — Deuda estructural y compacción

- [ ] Migrar incrementalmente las 13 skills legacy a schema v1 al tocarlas; no hacer una reescritura masiva sin valor operativo #owner/agent #type/dev #area/personal 🔽
- [ ] Alinear `agents-os-tagging-system` y `operational-healthcheck-policy` con secciones, scope, tags y metadata del skill contract #owner/agent #type/dev #area/personal 🔽
- [ ] Compactar `agents-os-entity-update` y `agents-os-hygiene-review`, moviendo ejemplos/rationale a referencias cuando reduzca costo de carga #owner/agent #type/dev #area/personal 🔽
- [ ] Resolver la semántica de logging de `entity-update`: obligatorio para cambio canónico S2 y opcional sólo para progreso no material #owner/agent #type/dev #area/personal 🔽
- [ ] Reclasificar y compactar `design-frozen-pattern-for-homelab-refactor`, `source-order-count-zero` y `memory-tool-format-drift-recovery` según frontera learning/known_error/runbook/skill #owner/agent #type/dev #area/personal 🔽
- [ ] Barrer las 76 memorias públicas legacy sólo al tocarlas, agregando schema_version y routing vigente sin inventar provenance retroactiva #owner/agent #type/dev #area/personal 🔽

## 📆 Bitácora

- **2026-08-11** — El owner descartó explícitamente la solución Keychain/iCloud y ordenó una fuente simple en texto plano. Se creó `80-agents/tools/echo-forge-worker-access/credentials.env` con warnings/TODO, modo `0600` y exclusión de Graphify; `~/bin/echo-forge-worker` enlaza el wrapper canónico para Codex/Claude Code/Cursor/Antigravity y el contrato vive en [[echo-forge-workers-shared-access]]. El smoke SSH previo sigue bloqueado por timeout de red en los tres hosts.
- **2026-08-11** — Fase 4 creada como backlog-only desde auditoría completa. Se aplicaron únicamente correcciones deterministas y urgentes; los cambios estructurales quedaron como To Do, sin WIP ni gates abiertos.

## 🧭 Decisiones

- Esta fase no usa un plan secuencial ni replica los gates de fases anteriores; su primera función es conservar backlog verificable.
- Un hallazgo no se implementa por existir: seguridad y corrupción de autoridad se corrigen de inmediato; refactors y cambios de diseño se priorizan antes de ejecutarse.
- La tarea puente del padre permanece To Do hasta que el owner decida iniciar una mejora concreta.

## 🔗 Docs / Links

- [[AGENTS OS]] — cockpit humano y tarea puente.
- [[agents-os]] — mapa conceptual del sistema.
- [[agent-constitution]] — invariantes runtime.
- `80-agents/journal/hygiene/2026-08-11-full-system-hygiene-review.md` — evidencia y alcance de la auditoría base.
- `80-agents/crew/INDEX.md` — registro y dashboard superficie×modelo.

## 💡 Ideas

### Backlog de ideas

- Agregar aquí nuevos hallazgos como tareas To Do con evidencia y prioridad; no crear planes paralelos.

### Motivos / principios

- Reducir drift entre ideología declarada, implementación ejecutable y observabilidad real.

### Memoria pública / interna

- **Memoria pública:** contratos, decisiones, learnings, known errors y runbooks reusables que sesgan comportamiento futuro.
- **Memoria interna:** continuidad operacional compacta y estado episódico que no debe contaminar el canon público.
- **Motivo:** mantener startup liviano y hacer que cada afirmación durable tenga autoridad y trigger explícitos.
