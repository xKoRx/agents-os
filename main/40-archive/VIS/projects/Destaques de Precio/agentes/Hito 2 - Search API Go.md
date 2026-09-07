---
type: project
owner: agent
root: false
status: active
priority: P1
area: "[[Meli]]"
parent: "[[Implementación Hito 2 - Destaques de Precio]]"
sprint: "[[A26Q2S7]]"
start: 2026-07-03
due:
progress: 0
repo:
jira:
prs:
aliases:
  - Implementación Hito 2 Search API Go
tags:
  - project
  - area/meli
  - app/search-api-go
  - feature/destaques-de-precio
created: "2026-07-03"
updated: "2026-07-03"
---

# Hito 2 - Search API Go

> [!info]+ Hito 2 - Search API Go
> **Parent:** [[Implementación Hito 2 - Destaques de Precio]]

## 🎯 Objetivo

- Incorporar los atributos mínimos de Destaques de Precio a la caché/contrato de Search API Go y habilitar su exposición/filtrabilidad según definición de Search.

## 📊 Estado actual

- Bloqueado por definición de atributos de item y conversación con Search.

## ✅ Tareas

> [!example]- Fuente de tareas
> - [ ] Resolver repo/path local correcto de Search API Go #owner/agent #type/research #area/meli #app/search-api-go
> - [ ] Relevar cómo se cachean atributos de item para Search #owner/agent #type/dev #area/meli #app/search-api-go
> - [ ] Proponer cambio para cachear atributos mínimos de Destaques #owner/agent #type/dev #area/meli #app/search-api-go #blocked
> - [ ] Validar si los atributos pueden ser filtrables en Search #owner/agent #type/research #area/meli #app/search-api-go #blocked
> - [ ] Definir contrato hacia search-middleware: highlight/float-highlight u otro #owner/agent #type/dev #area/meli #app/search-api-go #blocked
> - [ ] Agregar tests de cache/propagación cuando exista contrato #owner/agent #type/dev #area/meli #app/search-api-go #blocked

## 📆 Bitácora

- **2026-07-03** — Proyecto de agente creado. Pendiente resolver repo exacto.

## 🔗 Docs / Links

- RFC: `file:///Users/rjara/fuentes/second-brain/sb-main/01_Projects/previous-price-motors/RFC%20Destaque%20de%20precio%20%E2%80%94%20Hito%202.md`
