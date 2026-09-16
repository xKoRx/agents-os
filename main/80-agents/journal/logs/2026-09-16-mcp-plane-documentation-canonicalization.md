# change_log 2026-09-16 — Reconciliación documental canónica del MCP Access Plane

Sesión Ariadna (Hermes, desktop). Workload owner: one-shot de documentación/reconciliación. **Cero cambios runtime** (sin deploy, sin restart, sin grants/ACL/tokens); única consulta read-only externa: `stat` de configs kor en Daedalus para resolver la contradicción documental Codex.

## Objetivo

Que Agents-OS quede como source of truth correcto, consistente y utilizable: 10 capabilities canónicas documentadas, skill ↔ runbooks ↔ proyectos ↔ certificación contando la misma historia vigente, historia etiquetada, deuda abierta registrada sin resolverla.

## Autoridad aplicada

Orden: evidencia runtime/certificación fechada (remediation runs 09-15/09-16, change logs GAP-ECHO-010 y tri-client) > ACCESS-CERTIFICATION > proyectos > runbooks > `aranea-mcps-expert` > change logs > notas históricas. Ante contradicción no se mezclaron estados: se corrigió el documento stale y la historia quedó etiquetada (`HISTORICAL`, `RESOLVED`, `SUPERSEDED`).

## Verificación física mínima (read-only)

`ssh daedalus-ops` → `stat` de `/home/kor/.codex/config.toml` (mtime **2026-09-16 18:49**, 4285 B) + backup `config.toml.bak-tri-20260916-181245` presente. Esto demostró que el patcher stageado fue ejecutado como kor después del change log tri-client de la mañana: el estado "Codex PENDING" es histórico y el brief owner ("Codex: smoke nativo 2026-09-16 10/10 PASS, CONSUMER_ACCESS_READY: PASS") es la evidencia vigente. Contenido no leído (600 kor por diseño).

## Documentos modificados (11)

| Documento | Estado previo → accion | Drift encontrado |
|---|---|---|
| `30-resources/agents/skills/aranea-mcps-expert/SKILL.md` | corregido | Hasura PROD-RO "exactamente 4 tools" y bloque de superficie con `export_metadata` como vigente → 3 tools post-H1 (superficie 4 tools = HISTORICAL 09-12); añadido mapeo de sesión vigente familia mcp-proxy (`-32603`/`-32001`/`-32000`/202 id-less) al paso 6; `updated: 2026-09-16` |
| `30-resources/runbooks/aranea-hasura-mcp.md` | corregido | 3 menciones "4 tools"/"las 4 tools" → 3 tools vigentes (HISTORICAL etiquetado); artefactos pre-H1 pre-g010 → imágenes vigentes `-g010fix` + tags rollback retenidos; patcher `fix-shared-child.mjs` documentado; nueva sección § Failure modes con mapeo de errores y estado HISTORICAL/SUPERSEDED del diagnóstico async-202; updated |
| `30-resources/runbooks/aranea-mcp-capability-plane.md` | corregido | Caso Hasura PROD 09-12 marcado HISTORICAL con nota de superficie vigente 3 tools; nuevo caso conocido "GAP-ECHO-010 (familia hasura) 2026-09-16"; updated |
| `30-resources/runbooks/aranea-mongodb-mcp.md` | corregido | "Certificación end-to-end pendiente… no inventar PASS" (stale desde 09-14) → certificación CUBIERTA por run 09-14 (RO + RW round-trip), nota original HISTORICAL; añadida nota I9 (RO/RW = mismo mongod, separación de autoridad no de ambiente); updated |
| `30-resources/runbooks/00-index.md` + `log.md` | completado | Fila faltante de `aranea-observability-mcp` (runbook certificado 09-15 sin fila en índice); entrada en log.md |
| `10-projects/Aranea/AGENT-PLATFORM/agentes/AGENT-PLATFORM - MCP Access Plane.md` | corregido | Perfiles SSH stale (SQX viewer → operator desde 09-13; viewer boundary post-H2 tool-level); identidades PG RO/RW stale (`mcp_echo_ro`/`mcp_echo_rw` → `mcp_echo_prod_ro`/`mcp_echo_dev_rw`, drift M6 cerrado) con deuda M3 explícita; Hasura 4→3 tools; "nueve capabilities" → diez (observability certificada 09-15; `aranea-jaeger-ro` = DEFERRED/NEEDS_SOURCE_PROOF); incidente ssh 09-13 re-clasificado RESUELTO (pool-64, causa identificada 09-15; diagnóstico async-202 que lo agrupaba con ssh/flink = SUPERSEDED); lista de runbooks sin observability → 8 runbooks; D24 4→3; semántica de `progress: 85` aclarada (se conserva conservadoramente, sin recálculo objetivo); bitácora 2026-09-16b; updated |
| `10-projects/Aranea/AGENT-PLATFORM/agentes/AGENT-PLATFORM - MCP Access Plane - Architecture.md` | corregido | Superficie PROD "exactamente 4" + `export_metadata` → 3 tools post-H1; artefactos de imagen → `-h1fix`/`-g010fix` + rollback; updated |
| `10-projects/Aranea/AGENT-PLATFORM/agentes/workstreams/HASURA-MCP.md` | corregido | 2 menciones "4 tools" → 3 tools vigentes con etiqueta HISTORICAL; updated implícito vía contenido (nota status: done, histórica) |
| `10-projects/Aranea/AGENT-PLATFORM/agentes/workstreams/ACCESS-CERTIFICATION.md | etiquetado | Fila Hasura PROD-RO de la matriz del run 09-14: 4 tools marcado HISTORICAL pre-H1, veredicto "H1 RESOLVED 2026-09-15"; sin más cambios (la nota ya estaba vigente) |
| `10-projects/Aranea/agentes/HERMES — Agent Access Operations.md` | corregido | A1.1–A1.4 marcados [x] con evidencia GAP-ECHO-010 (golden repair ejecutado 09-16); Estado actual: A0 gate demostrado, A1 gate demostrado, A2 precedentes sin gate formal, A3–A5 abiertos; boundary precisado (config/capabilities/certificación, no desarrollo de aplicaciones); bitácora 2026-09-16d; updated |
| `80-agents/journal/logs/` (change log) | creado | Este documento |

## Contradicciones resueltas y cómo

- **Hasura PROD-RO surface (4 vs 3 tools):** vigente = exactamente 3 (`get_inconsistent_metadata`, `get_schema`, `get_version`) desde H1 2026-09-15; `export_metadata` eliminado por exponer `database_url` con credenciales upstream. Los textos de 09-12 que decían 4 tools quedaron etiquetados HISTORICAL, no borrados.
- **GAP-ECHO-010:** vigente = `REPAIRED_AND_CERTIFIED` (causa: hijo stdio compartido de mcp-proxy 6.7.16, exclusiva de la familia hasura; fix g010; cert 50/50 + 30/30 server y consumer PASS). El diagnóstico intermedio "async-202 tras churn" que agrupaba a ssh-mcp y flink-mcp quedó SUPERSEDED; `202` sin sid es respuesta a notificaciones id-less, no initialize inválido; `-32001`/`-32000` mapeados. ssh-mcp = quirk propio pool-64; flink-mcp = SDK Java.
- **Codex consumer:** vigente = config normalizada en disco 18:49 (`bearer_token_env_var`, backup `bak-tri-20260916-181245`) + smoke nativo 10/10 PASS según brief owner; el "PENDING patcher stageado" de los change logs de la mañana quedó HISTORICAL. La certificación funcional post-patch desde el IDE queda como validación residual de owner.
- **Observability:** `aranea-observability-ro` desplegada y certificada 09-15 (22 tools RO); `aranea-jaeger-ro` sigue DEFERRED/NEEDS_SOURCE_PROOF (roadmap ≠ inventario).
- **Mongo RO/RW:** certificación end-to-end cubierta por el run 09-14 (la nota "pendiente" del runbook era stale desde entonces).
- **Incidente ssh 09-13:** RESUELTO (pool-64, causa identificada 09-15); ya no queda estado vigente "causa UNKNOWN / T6 abierto" por este incidente.

## Deuda abierta preservada (sin resolver, no rotada, no ampliada)

- **Aislamiento de credenciales:** bearers Mongo y PostgreSQL comparten VALOR RO-RO y RW-RW (sha16 `5416e5d2…` / `aeca359b…`); separación por nombre de variable. Rotación coordinada de 4 proxies = owner action posterior.
- **ZCode:** bearer literals en config `600 kor` (sin interpolación `${env:}` documentada para headers HTTP); conservado funcional; alternativa = rotación + canal kor-only (decisión owner).
- **M3:** rol `mcp_echo_prod_ro` sin límites temporales (`0/0/0`).
- **M5:** `get_schema` PROD falla por transporte (~11 MB) → pendiente de diagnóstico como deuda del plane.
- **Host key `.71`** idéntica a `sqx-zeus` (rotación owner-side sugerida, no bloqueante).
- **Temporal / MinIO / etcd / Jaeger-specific:** sin capability; quedan como DEFERRED / NEEDS_SOURCE_PROOF en la nota de certification (ya etiquetados); no se convirtieron en inventario.
- **Codex certificación funcional desde el IDE** post-normalización (residual owner, no bloqueante).

## Escaneo de términos stale (post-edición)

Resultados verificados tras el pase: `export_metadata` persiste sólo en contexto HISTORICAL/superficie DEV (proyectos, workstreams, journal — clasificado, no estado vigente de PROD-RO); "4 tools"/"cuatro tools" idem (HISTORICAL 09-12 o referencias DEV=9); referencias `.211` sólo con marca muerto/retirado/histórico; `202-no-sid`/`pool-64`/`async-202` quedan en notas fechadas como historia/resolución o referencia al quirk vigente de ssh-mcp. Nombres de capabilities antiguos (`aranea-kafka-ro`, `sqx-dev`) no aparecen como vigentes fuera de bitácoras etiquetadas "supersedida".

## Validación

- Zero runtime delta: sin comandos contra `mcps`, sin smokes MCP, sin cambios de config/consumers; `stat` read-only vía `daedalus-ops` como única excepción documentada.
- 10/10 capabilities cuentan la misma historia en skill + runbook de familia + proyecto del plane + ACCESS-CERTIFICATION.
- 8 runbooks de familia/plane existen y están enlazados desde la skill y el proyecto (observability incluida en índice).
- Historia preservada y etiquetada, no mezclada con estado vigente.
- Cero secretos impresos o persistidos.

## Fuentes

- Nota de certificación: `10-projects/Aranea/AGENT-PLATFORM/agentes/workstreams/ACCESS-CERTIFICATION.md`
- Change logs: `2026-09-16-gap-echo-010-shared-stdio-child-repaired`, `2026-09-16-tri-client-consumer-certification`, `2026-09-16-tri-client-mcp-config-normalization`, `2026-09-16-access-ops-capability-reconciliation`
- Skill de mecánica: `mcp-access-plane-operations` (perfil Hermes)
- Brief owner: `MCP ACCESS PLANE / DOCUMENTATION CANONICALIZATION` (2026-09-16)
