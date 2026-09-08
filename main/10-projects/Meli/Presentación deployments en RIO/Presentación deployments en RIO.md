---
type: project
schema_version: 1
owner: me
root: true
status: active
priority: P1
area: "[[Meli]]"
parent:
sprint:
start: 2026-09-01
due: 2026-09-08
progress: 90
repo: ads-signals-knowledge-library
jira:
prs:
aliases:
  - Presentación RIO deployments
  - Deployments en RIO
tags:
  - kind/project
  - area/meli
  - project/presentacion-deployments-rio
created: "2026-09-01"
updated: "2026-09-07"
---

# Presentación deployments en RIO

> [!info]+ Presentación deployments en RIO
> **Área:** [[Meli]] · **Estado:** active · **Prioridad:** P1 · **Entrega:** 2026-09-08
> **Knowledge vigente:** [[ads-signals-knowledge-library]] · **Plataforma:** [[RIO]]

## 🎯 Objetivo

- Preparar una explicación corta, precisa y completa del flujo de deployments en RIO: intención, orquestación, modelo de datos, mensajes, routing por control plane, materialización, resultados, avance de batches y fallas de diseño.
- Dejar un guion técnico verificable para explicar primero el flujo vigente y luego profundizar en sus puntos críticos, mecanismos de recuperación y deuda técnica.

## 📊 Estado actual

- Knowledge del vault reemplazada: `ads-signals-knowledge-library` es el puntero canónico y `signals-knowledge` quedó deprecada.
- Flujo revalidado contra los `origin/master` locales de Playmaker, SDK Events, Materializer y los control planes Kafka, Flink, ClickHouse, Fury, Signals y Observability.
- Documento principal reestructurado en tres partes: funcionamiento vigente y tecnologías; zoom causal sobre nueve puntos críticos; backlog priorizado de deuda técnica.
- Pendiente ensayar el relato y confirmar configuración viva de producción para las afirmaciones de routing que dependan de scopes u overrides.

## 🧱 Entrega de desarrollo

_No aplica — proyecto de comprensión y presentación; no modifica código ni configuración ejecutable de RIO._

## 🧩 Subproyectos

_Sin subproyectos._

## ✅ Tareas

- [x] Reemplazar `signals-knowledge` por [[ads-signals-knowledge-library]] en el vault #owner/me #type/admin #area/meli
- [x] Revisar estructura, contratos, flujos, servicios, troubleshooting, catálogo, gobierno y evaluaciones de la knowledge library #owner/me #type/research #area/meli
- [x] Contrastar las afirmaciones materiales con `origin/master` de los repos RIO #owner/me #type/research #area/meli
- [x] Crear [[Deployments en RIO — flujo completo]] #owner/me #type/research #area/meli
- [x] Crear [[Revisión de ads-signals-knowledge-library]] #owner/me #type/research #area/meli
- [x] Reestructurar [[Deployments en RIO — flujo completo]] como guion técnico con tecnologías, puntos críticos, recuperación y deuda #owner/me #type/research #area/meli
- [ ] Ensayar el relato final y ajustar profundidad al tiempo disponible #owner/me #type/research #area/meli
- [ ] Confirmar configuración viva de routing y suscripciones para distinguir código base de tráfico real #owner/me #type/research #area/meli #waiting

## 📆 Bitácora

- **2026-09-07** — Se revalidó el flujo con refs locales más recientes y se reestructuró la guía para presentar en dos pasadas. Se corrigió la lectura de Materializer: es owner explícito de `s3-bucket` y `gcs-bucket`, pero el catch-all de Playmaker también absorbe tipos no migrados; `gcp-kafka-topic` es el caso verificado. Se documentaron nueve puntos críticos y nueve deudas técnicas con criterio de aceptación.
- **2026-09-01** — Proyecto creado. Se reemplazó la knowledge anterior, se auditó íntegramente la librería nueva y se contrastó el deployment flow con el código actual de los repos. La librería es estructuralmente buena, pero su validación falla con 17 errores y varias afirmaciones materiales quedaron atrás de `master`; la documentación para mañana usa el código como autoridad.

## 🧭 Decisiones

- Para comportamiento vigente, `origin/master` del servicio dueño prevalece sobre la knowledge library; la librería sirve como mapa y provenance, no como sustituto de verificación.
- La guía principal contiene el modelo mínimo necesario para presentar; la evidencia de drift y el detalle forense viven separados en [[Revisión de ads-signals-knowledge-library]].
- Actions y runtime status se explican como protocolos adyacentes, no como estados del deployment, para no mezclar máquinas de estado distintas.
- La presentación separa el camino feliz del análisis de fallas: en la primera pasada sólo marca `PC-1` a `PC-9`; en la segunda explica causa, recuperación actual, solución y deuda.
- Materializer se presenta como owner explícito de storages y catch-all legacy, no como camino exclusivo de storage mientras `gcp-kafka-topic` siga fuera de la allowlist BigQueue de Playmaker.

## 🔗 Docs / Links

- [[Deployments en RIO — flujo completo]] — documento principal para la presentación.
- [[Revisión de ads-signals-knowledge-library]] — auditoría de cobertura, integridad y frescura.
- [[ads-signals-knowledge-library]] · [[RIO]] · [[rio-playmaker]] · [[rio-sdk-events]]

## 💡 Ideas

- Usar el futuro Grid para contrastar visualmente el camino feliz con las ventanas de pérdida: `commit → evento en memoria`, `ACK → trabajo en background` y `estado terminal → publicación best effort`.
