# Session feedback — 2026-09-16 E-02 physical certification (Ariadna/Hermes)

## Fricciones

1. **Transporte MCP no documentado por familia (fricción mayor, ~2h).** Cada proxy nginx-wrapped exige un patrón distinto y NO documentado en los runbooks: hasura-family alternó entre sync-200+sid, async-202-sin-sid y "Not connected" según estado interno; kafka acepta sid client-chosen en un wrapper y server-issued en otro; ssh-mcp sirve en `/` (no `/mcp`). Los errores (`-32000 Missing session ID`, `-32603 Not connected`, `-32001 Session not found`, `-32600 Bad Request`) no distinguen "probe bug" de "capability degradada" — consumí horas diagnosticando transporte antes de poder tocar el gate real. **Propuesta:** el runbook `aranea-mcp-capability-plane` debería incluir una tabla por familia: path, sid semantics (client/server-chosen), patrón de reintentos, y el error→significado.

2. **Defecto async-202 (GAP-ECHO-010, P1).** El modo degradado de los proxies (202 sin sid) es indistinguible de un bug del cliente; el recovery (restart del backend proxy) es workaround, no solución. Segundo caso en 24h. Urgente diagnóstico durable del mcp-proxy (pool/leak/streams).

3. **Redacción de secretos en herramientas destruye código legítimo.** El editor aplicó redacción `Authorization: *** ` dentro de un archivo Python legítimo del helper (valor no-era-secreto: patrón de header). Detectado por el runtime error `202` en lugar del esperado; costó varios ciclos. Sugerencia: restringir redacción de patrones de credenciales a outputs de chat, no a writes de archivos verificados por hash.

4. **`mcps-ops` + heredoc/pipe**: combinaciones complejas (pipe cross-host con sudo cat) activan approval gates o timeouts; los scripts deben correr íntegramente en el host remoto con bearer por path, nunca cruzar el valor al cliente.

## Aciertos

- Helper único de sesión (`e02-hermes-mcp.py`, SDK mcp + httpx2) después de la corrección del owner: eliminó la re-implementación por probe (era el patrón a corregir).
- Clasificación KEEP/REMOVE antes de continuar (corrección del owner): evitó una regresión real (roles E-02) que mi rollback ciego había causado; re-aplicación inmediata vía SDK.
- Gate 3 con control mínimo (restart de 1 container) en vez de resubmit agresivo; recovery probado con checkpoint `restored=1`.

## Lecciones transferibles

- "Baseline" ≠ "estado correcto": restaurar baseline incompleto respecto del spec es regresión. Clasificar mutación antes de revertir.
- Ante transporte MCP errático: primero diagnóstico bounded del plane (health, logs, /status sessions), después asumir defecto del target.
