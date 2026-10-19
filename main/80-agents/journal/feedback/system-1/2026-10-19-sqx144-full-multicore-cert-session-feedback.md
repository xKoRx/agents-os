---
type: session_feedback
schema_version: 1
scope: session
created: "2026-10-19"
updated: "2026-10-19"
area: "[[Aranea]]"
project: "[[Echo Forge — Operación Real V2]]"
application:
entities:
  - "[[Aranea]]"
aliases: []
confidence: verified
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/session-feedback
  - scope/session
  - area/aranea
---

# 2026-10-19-sqx144-full-multicore-cert-session-feedback

## Fricción observada

1. **`sftp-upload` del MCP SSH corrompe contenido no trivial**: un base64 de 13 KB llegó con +1 carácter (longitud inválida, `base64 -d` falla en los 3 hosts). Vía confiable medida: staging HTTP LAN + curl + verificación SHA256 en destino. Actualiza la expectativa del runbook (que ya documentaba "no reemplaza fiable un path existente": ahora además, contenido largo llega mangleado).
2. **TTL de sesión MCP (10 min) + cliente sin re-initialize**: tras un gap >10 min sin llamadas aranea-ssh, el cliente ZCode queda pegado al session-id muerto (`Session not found or expired`) y NO reinicializa solo; el plano servidor está sano (initialize manual con bearer responde session nueva al tiro). Recovery funcional usado durante horas: driver curl propio con initialize + `tools/call` + re-init automático (`fc-ssh.sh`). Candidato a parche de cliente o a nota en [[aranea-mcp-capability-plane]].
3. **`read-command` rechaza compuestos** (`tail; ls` = clase "safe" no allowlist): usar `run-command` también para lecturas compuestas o comandos simples.
4. **Gotchas SQX medidos** (para el próximo harness): el Optimizer imprime `Task finished` SIN duración (el Retest/Build con `in N s.`); los databanks reales del builder_test se llaman `Output`/`Input`/`Results`/`Existing portfolio`; el `builder_test.cfx` del repo es un CFX de tarea (root `<Task>`, sin `<Project>`) y su `taskXMLFile` debe contener sólo el body `<Settings>`; `XAUUSD_darwinex` no tiene datos en la flota (usar `_dukascopy`); picos de tasa >nproc en VM = artefacto de muestreo (usar medias integrales jiffies como métrica primaria); la HTTP API local de SQX (`:5050/call?cmd=-project%20action=status%20name=X`) permite leer progreso/estado sin tocar el run.

## Señal positiva

- El patrón "candidate-local lean + symlinks + HTTP+SHA staging + driver con gates resumibles" ejecutó una campaña de ~8 h en 3 hosts en paralelo sin tocar producto y con reintentos limpios — reutilizable tal cual para futuras certificaciones de flota.
