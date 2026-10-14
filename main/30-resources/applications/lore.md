---
type: application
schema_version: 1
status: active
slug: lore
area: "[[Meli]]"
lang: TypeScript
github: https://github.com/melisource/fury_lore
path: ~/fuentes/lore
last_verified: "2026-10-14"
confidence: medium
sources:
  - "[[Source — Lore — Verificación local 2026-10-14]]"
aliases:
  - "lore"
  - "fury_lore"
tags:
  - kind/application
  - area/meli
  - app/lore
created: "2026-10-14"
updated: "2026-10-14"
---

# lore

> [!info]+ lore
> **Rol:** Regresión E2E agéntica — un agente LLM ejecuta escenarios escritos en Markdown sobre un navegador real y entrega veredictos con evidencia · **Área:** [[Meli]] · **Plataforma:** Fury
> **Repo:** [remote](https://github.com/melisource/fury_lore) · **Local:** `~/fuentes/lore` · **Lang:** TypeScript (Node 24)

## 🎯 Responsabilidad (estable)

- Responde si un ambiente o build es liberable: corre escenarios en Markdown con un agente que maneja Playwright y devuelve `passed` / `failed` / `blocked` / `skipped` con screenshots, URL y trace por paso.
- Release gate por proyecto (compliance mínimo y fallas críticas toleradas) consultable con un `GET` desde CI.
- Límite de dominio: no es la app bajo prueba ni reemplaza los tests del repo; verifica comportamiento observable en el navegador.

## 🔌 Contratos e interacciones (semi-estable)

- **Expone:** Web UI, REST `/api/v1` y servidor MCP `/api/mcp` con la misma funcionalidad que la UI.
- **Consume / produce:** modelos del GenAI gateway de MELI (Claude, GPT, Gemini; seleccionable por proyecto, schedule o run); notificaciones a Slack.
- **Llama a / lo llaman:** apps bajo prueba vía navegador; Fury (proyectos por team, ambientes mapeados a scopes, runs disparados por deploy de una versión).

## 🧩 Implementación (volátil · last_verified: 2026-10-14)

- **Stack:** Nordic (frontend + REST + MCP en un proceso web) más un runner que reclama runs encolados y ejecuta agente + Playwright.
- **Librerías / infra clave:** Playwright (Chromium); Fury registry para `npm install` (requiere VPN).
- **Patrón notable:** local con `npm run dev:all` levanta web (`https://localhost:8443`), runner y una app de ejemplo (`http://127.0.0.1:4010`) con su proyecto `example`. Staging en `https://lore-staging.nonprod.adminml.com` (SSO MELI, acceso por usuario).

## Operación local verificada (last_verified: 2026-10-14)

- `npm run dev:all` imprime su token local en stdout desde scripts/dev-all.mjs; filtrar esa línea antes de mostrar/guardar logs cuando el contrato de la sesión prohíba exponer tokens. Propuesta de eliminación de esa línea pendiente, no aplicada.
- `LORE_SQLITE_PATH` y `LORE_EVIDENCE_DIR` permiten ubicar estado/evidencia fuera del repo. `NODE_CONFIG` permite configurar ragnar.server.securePort para convivir con otro Nordic en 8443; el banner de dev-all conserva la URL fija 8443, por lo que manda el puerto real del log.
- La API exige crear dependencias de escenarios antes de sus dependientes (422 unknown_dependency). Un error del agente produce blocked, sus dependencias skipped; run completed no significa journeys passed. En la prueba RIO: 0 passed/0 failed/3 blocked/9 skipped, compliance 0%, gate false; trazas sin page.goto.
- Claude Agent SDK 0.3.280 depende de binarios nativos opcionales: una instalación parcial puede permitir arrancar web/runner y aun así fallar al ejecutar con Native CLI binary for darwin-arm64 not found. No se verificó login de Claude ni GenAI gateway.
- Confiar la CA en macOS no acredita vigencia: comprobar fechas de toda la cadena. `NODE_EXTRA_CA_CERTS` resuelve confianza de Node, pero no una CA vencida.
- Fuente: [[Source — Lore — Verificación local 2026-10-14]]; ejecución y límites en [[RIO E2E local]].

## 🔗 Relaciones

- Candidata para las pruebas E2E desde el front de [[RIO E2E local]], verificación intentada el 2026-10-14 y bloqueada por ambiente local; journeys todavía no certificados.

## 📌 Provenance

- **Repo:** https://github.com/melisource/fury_lore · **Local:** `~/fuentes/lore` (HEAD `e906b95`, release 0.1.0)
- **Fuentes leídas:** `README.md` (secciones de presentación y Quick start).
- `last_verified: 2026-10-14` · `confidence: medium`

## ✅ Tareas relacionadas

```tasks
sort by priority
not done
description includes lore
short mode
hide task count
```
