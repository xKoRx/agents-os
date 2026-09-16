---
type: session_feedback
schema_version: 1
date: "2026-09-16"
project: "[[HERMES — Agent Access Operations]]"
area: "[[Aranea]]"
tags:
  - kind/session-feedback
  - area/aranea
  - system-1
---

# 2026-09-16 — Tri-client consumer cert session feedback

- **Fricción: heredoc Python con comandos bash anidados se rompe por comillas** (`SyntaxError: unterminated string literal` al pasar un script con `$val`/comillas dobles dentro de un heredoc vía ssh). Fix inmediato: correr la lógica directamente en bash remoto (sin wrapper Python) cuando el contenido es shell. Regla: si un step necesita shell+Python a la vez, scp el .py y ejecutarlo como archivo — jamás heredoc con anidación de comillas (3ª variante del anti-patrón stdin/heredoc ya registrado en B4/B3.3).
- **Fricción de plataforma: un turno se abortó por tool_use malformado (claves duplicadas `multi_select`/`question` en un JSON de clarify) — no por contenido.** El estado quedó vivo sólo en workspace local hasta el recovery. Mitigación aplicada y a recordar: con briefs one-shot largos, materializar change-log/checkpoint en vault al completar cada gate, no sólo al cierre.
- **Reconfirmación de regla de skill (ya documentada, volvió a costar un ciclo):** derivar los argumentos de `tools/call` del `tools/list` REAL antes de congelar aserciones — `list-databases` de mongo-mcp exige `connectionId` y una sonda con `{}` lo clasifica `CAPABILITY_GAP` siendo bug de sonda. Lo mismo para falsos `NOT_SET` del chain si el probe corre con `HOME` equivocado.
