---
type: resource
schema_version: 1
status: active
confidence: provisional
area: "[[Personal]]"
project: "[[Polymarket Engine — MVP]]"
created: 2026-09-17
updated: 2026-09-17
tags:
  - tech/polymarket
  - topic/protocol
  - status/research-gaps
---

# Polymarket — Technical Platform Map — Intake 2026-09-17

> [!warning] INGESTA PENDIENTE EN GITHUB — ESTA FICHA NO ES EL DOCUMENTO TÉCNICO ÍNTEGRO
> El archivo original completo está preservado como Markdown en la Biblioteca de ChatGPT: `/Polymarket Engine/Resources/Polymarket — Technical Platform Map — synced 2026-09-17.md`. Debe incorporarse **íntegro y byte a byte** en este repositorio, bajo `main/30-resources/polymarket/Polymarket — Technical Platform Map — synced 2026-09-17.md`, antes de trabajar sobre él. El conector GitHub utilizado para este registro no admite recibir directamente archivos locales de 160 KB; por eso NO se declara subida completa ni se sustituye el contenido por un resumen. Facilitar al agente el Markdown original mediante su entorno o attachment si no puede acceder a la Biblioteca. Si no obtiene el archivo, STOP sin fabricar contenido.

## Identidad e integridad del original

- Título del documento: `Polymarket — Technical Platform Map — synced 2026-09-17`.
- Sincronización declarada por el investigador: `2026-09-17 02:34:53 UTC`.
- Tamaño original: `160165` bytes, UTF-8; `1177` líneas de texto.
- SHA-256 original: `78e6506fa67aa12843ba4acb0e4c8271a83c1841432a4a53777c73c4c723c11f`.
- Ubicación persistente del original completo: Biblioteca `/Polymarket Engine/Resources/Polymarket — Technical Platform Map — synced 2026-09-17.md`.
- Estado declarado en el documento: `DOCUMENTO CORREGIDO; CERTIFICACIÓN CONTRACTUAL INTEGRAL PENDIENTE`.
- **NO LIVE CONVERSION UNTIL ROUTE VERIFIED** para NegRisk Protocol-v2.

## Lectura ejecutiva para el proyecto

El original contiene 26 secciones de hosts y superficies, entidades e IDs, inventario de endpoints, autenticación, EIP-712, precisión, órdenes, recovery WS, positions/CTF, contratos, NegRisk, Combos, fees/rewards, resolución, histórico, rate limits, SDKs y source registry. Sirve como input técnico provisional para la discusión; **no constituye un contrato de implementación de toda la API ni habilita trading live**. Preservar las afirmaciones verificadas y los límites explícitos de cobertura.

## Brechas abiertas declaradas por el documento original (§24)

- `RG-01` — descargar y parsear de verdad OpenAPI Gamma/CLOB/Data legacy/Data v2/Relayer/Combos/Bridge; reconciliar operación por operación con el catálogo.
- `RG-02` — extraer RFQ AsyncAPI y todas las direcciones, messages y recovery semantics.
- `RG-03` — cerrar contrato y límites de `/orderbook-history`; no confundir mera referencia con archivo L2 determinista garantizado.
- `RG-04` — documentar DTO, enums y timestamps exactos de `/v2/resolutions`.
- `RG-05` — verificar versión→ABI→contrato→autorizaciones y call exacta para NegRisk Protocol-v2; mantener live deshabilitado hasta verificación.
- `RG-06` — auditar todos los URLs del source registry, incluidos permalinks SHA/path.
- `RG-07` — cerrar `deferExec=true`, contratos de notificaciones/webhooks y gateways secundarios, o etiquetar explícitamente fuera de scope con justificación.

## Workflow incremental obligatorio

1. Ingestar el Markdown **íntegro**, comprobar SHA-256 y commit de importación sin edición del contenido.
2. Trabajar directamente sobre ese archivo en repo mediante cambios pequeños, sin devolver un documento entero en el chat.
3. Cada pasada: un `RG` o un conjunto mínimo de contratos vinculados → evidencia official URL/commit → edit in-place → tests/checks automáticos → commit → actualizar estado del mismo archivo y log.
4. No inventar `NOT DOCUMENTED` para un spec que simplemente no se pudo descargar; no falsificar `RESEARCH GAPS = 0`.
5. No reescribir el proyecto root ni crear documentos de diseño adicionales por una corrección de protocolo.
6. No consumir Astra/Fable para lookup repetitivo; M0 queda en progreso hasta cerrar sólo los blockers materiales del engine. Después diseño Astra → challenge Fable → reconciliación → revisión conjunta → TOP plan → NORMAL implementación.

## Enlaces

- Proyecto: [[Polymarket Engine — MVP]].
- Índice: [[00-index]].
- Research: [[Polymarket — Edge Research Consolidado 2026-09-16]].
- **Destino del original completo en GitHub (aún NO creado):** `main/30-resources/polymarket/Polymarket — Technical Platform Map — synced 2026-09-17.md`.
