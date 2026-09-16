---
type: change_log
schema_version: 1
scope: session
created: "2026-09-16"
updated: "2026-09-16"
area: "[[Aranea]]"
project: "[[HERMES — Agent Access Operations]]"
entities:
  - "[[HERMES — Agent Access Operations]]"
  - "[[AGENT-PLATFORM - MCP Access Plane]]"
related:
  - "[[ACCESS-CERTIFICATION]]"
aliases: []
confidence: verified
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-09-16-tri-client-mcp-config-normalization

%% Routing: area/project/entities/related usan links canónicos. %%

## Cambio

- **Tipo:** recovery + verificación de estado externo + staging de instrumento read-only. Sin mutación de configs de consumidores en esta sesión.
- **Archivo(s):**
  - Daedalus:`/tmp/tri-kor-inspect.py` (created, staging; sha16 `de782b8708a13a82` verificado local↔Daedalus).
  - `/home/kor/.cursor/mcp.json` (VERIFIED, no tocado: corrección Mongo RO/RW de la sesión 18:29 sigue persistida).
  - Este log + feedback + touch de [[ACCESS-CERTIFICATION]].

## Motivo

- Cierre del brief owner TRI-CLIENT: dejar consistentes las configs MCP de ZCode, Codex y Cursor en Daedalus, recuperando el estado de la sesión colgada 18:56 sin repetir auditoría ni smokes.

## Fuentes leídas

- Workspace `~/tmp-tri-client/` de la sesión anterior (fix + sweep + resultados 13 filas).
- Historial de la sesión colgada (discovery, docs oficiales ZCode, clarify sin respuesta — resuelto por el brief de esta sesión).
- `/home/kor/.cursor/mcp.json` leído de disco (parse completo, 11 entradas).
- Runbook `aranea-mcp-capability-plane.md` (B2 onboarding + B4 chain), workstream ACCESS-CERTIFICATION, logs B3.3 y reconciliación access-ops 2026-09-16.

## Resultado

- **Cursor: READY.** Refs Mongo `ARANEA_MONGO_FORGE_MCP_RO/RW_BEARER` persistidas en disco (mtime 15:29, posterior al fix); 11 entradas (10 capabilities + clon `aranea-postgres-ro-hermes-managed` contractual del mecanismo B2, RETAINED); sweep 11/11 PASS heredado.
- **ZCode: funcional conservado (READY con caveat).** Smoke 10/10 heredado sobre su config actual; los docs oficiales ZCode (verificados 2026-09-16) no documentan interpolación `${env:}` en headers HTTP (sólo env para stdio) ⇒ por decisión del brief §6 se conserva la config funcional con bearer literals, `600 kor` (rotación + canal kor-only queda como alternativa para decisión owner).
- **Codex: PENDING (OWNER_ACTION_REQUIRED).** Config `600 kor` sin ACL — ilegible para `hermes-ops` por diseño; el binario soporta `bearer_token_env_var` como mecanismo nativo. Único camino: inspector read-only que el owner corre como kor.
- **Anomalía registrada (sin resolver):** ambos configs kor tienen mtime 2026-09-16 13:26:41 con backups `.bak-mcp-20260916-132641`; la sesión vault de la mañana (reconciliación access-ops) declara read-only y no hay change_log que ampare esa edición. Origen a identificar por el owner (la sesión misma lo listará: ver backups en su `$HOME`).
- Residuos `/tmp` de Daedalus de la sesión anterior eliminados (gate1-*, tri-smoke*); intacto lo de kor.

## Instrumento para el owner (única acción)

- `tri-kor-inspect.py`: READ-ONLY + redactado (sha16+len, jamás valores), imprime ZCode/Codex/chain env (por nombres), crea backups `.bak-tri-<ts>` de ambos configs; rollback trivial = nada que revertir (los .bak son copias idénticas; borrar si sobran). Ejecutar como kor en Daedalus: `python3 /tmp/tri-kor-inspect.py`.
- Auto-test del script PASS contra configs sintéticos (redacción, detección ref/literal, comentarios del chain ignorados).

## Validación

- Cursor: parse real de disco (11 entries, refs exactas por nombre) — no sólo el sweep heredado.
- Script: sha16 idéntico en ambos hosts antes de la entrega; self-test RC=0.
- Cero ejecución de herramientas MCP, cero smokes, cero secretos impresos, cero ampliación de ACL, cero uso de sudo.

## Pendiente

- Owner corre el inspector → salida pegada en sesión → normalización ZCode/Codex sólo si hay drift demostrado (mecanismo nativo por cliente).
- Owner prueba los tres IDEs (requiere reiniciar los clientes para re-absorber el chain env si cambiara).
- Identificar origen de la edición 13:26:41 de ambos configs kor.
