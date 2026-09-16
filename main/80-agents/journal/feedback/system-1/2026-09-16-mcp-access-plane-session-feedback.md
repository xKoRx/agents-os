# 2026-09-16 — MCP Access Plane session feedback

## Fricción / degradación

- El estado vigente del plane quedó >24h sin reflejarse en las fuentes canónicas tras los remediation runs (H1/g010): skill y runbooks seguían diciendo "4 tools" después de que ACCESS-CERTIFICATION ya registrara 3; los change logs de la mañana decían "Codex PENDING" mientras el disco ya estaba normalizado (verificado por mtime + backup). El brief owner fue la única fuente que integraba todo.
- El índice de runbooks (`30-resources/runbooks/00-index.md`) no recibió la fila de `aranea-observability-mcp` cuando el runbook se creó (09-15): el índice no forma parte del checklist de cierre de ningún workstream.

## Gap de Sistema 1

- No existe un checklist mínimo de "actualización canónica post-intervención" (skill + runbook de familia + proyecto + Architecture + índice + change log) que se exija al cerrar un repair/deploy del plane. Hoy cada sesión reconcilió lo que recordaba; esta pasada encontró drift en 11 documentos.
- Los change logs de sesión pueden quedar detrás del estado real del disco cuando un patcher queda stageado y el owner lo ejecuta después: el closure de esos workloads debería verificar contra disco (stat/sha, jamás contenido) antes de declarar PENDING.

## Sugerencia

- Añadir a `mcp-access-plane-operations` / golden repair smoke un paso final explícito: "canon sync" con la lista de los 6 artefactos a tocar, y cerrar el change log sólo con verificación de disco de los configs consumer tocados.

## POST-GATE (mismo día, corrección posterior)

- La pasada original declaró "cero contradicciones materiales" y un gate independiente encontró 4 residuales (HIGH sin resolver en veredicto, Codex PENDING sin cierre, snapshot 09-13 sin etiqueta, UNKNOWN sin supersede + bullet duplicado). Lección: en reconciliación documental, la auto-validación del mismo agente que editó no alcanza como gate — la pasada de verificación debe hacerla una superficie distinta (gate/segundo agente) o con checklist mecánico de términos por documento, no por memoria. Corregido en el mismo change log.
