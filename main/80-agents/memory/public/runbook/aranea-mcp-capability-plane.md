---
type: runbook
schema_version: 1
scope: area
created: "2026-09-11"
updated: "2026-09-11"
area: "[[Aranea]]"
project: "[[AGENT-PLATFORM - MCP Access Plane]]"
application:
entities:
  - "[[Aranea]]"
related:
  - "[[aranea-mcps-expert]]"
  - "[[aranea-ssh-mcp]]"
  - "[[aranea-postgres-mcp]]"
  - "[[aranea-mongodb-mcp]]"
aliases:
  - runbook capability plane MCP Aranea
  - aranea mcp plane
  - troubleshooting MCP Aranea
confidence: verified
source_session:
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/runbook
  - scope/area
  - area/aranea
  - tech/mcp
  - action/mcp-plane
---

# aranea-mcp-capability-plane

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Propósito

Validar y diagnosticar el capability plane MCP de Aranea cuando el fallo es del cliente, el proxy o la capability misma, no del backend de datos. La fuente agent-facing de selección/autoridad es [[aranea-mcps-expert]]. Los procedimientos por familia viven en [[aranea-ssh-mcp]], [[aranea-postgres-mcp]] y [[aranea-mongodb-mcp]]. No mantener un segundo catálogo de endpoints aquí.

## Precondiciones

- El target es infraestructura Aranea; si es MELI/corporativo, abortar y no usar este runbook.
- Ya se confirmó que el síntoma no se explica por un backend concreto, o la capability esperada falta/desconecta/`401`/transporte inválido.
- `VAULT_ROOT` resuelve el marker `80-agents/agents-os/agents-os.md`.
- El agente no pide, imprime, copia ni persiste bearers, passwords ni private keys.

## Procedimiento

1. **Confirmar el estado normal del cliente.** Un cliente de desarrollo Aranea correctamente configurado expone: `aranea-ssh`, `aranea-postgres-ro`, `aranea-postgres-rw`, `aranea-mongo-forge-ro` y `aranea-mongo-forge-rw`. Los detalles de endpoint/autoridad son canónicos en la skill y en el runbook de familia; no duplicarlos aquí.
2. **Preflight antes de culpar al backend.** Confirmar que la capability `aranea-*` esperada aparece conectada; confirmar que la acción pedida calza con su autoridad; cargar el runbook de la familia; probar la operación read-only más pequeña primero; distinguir fallo de cliente/auth frente a fallo de backend/aplicación.
3. **Enrutar capability missing/disconnected.** Verificar la configuración MCP del cliente y recargar/reconectar. No pedir que el usuario pegue bearers en el chat. No publicar puertos de backend como workaround.
4. **Enrutar `401`.** Tratarlo como fallo de bearer/entorno del cliente en el boundary del proxy autenticado. No rotar, imprimir ni pedir secretos hasta que haya evidencia de que la rotación es necesaria.
5. **Enrutar `POLICY_DENIED` / permission denied.** Tratarlo primero como boundary de autoridad. En viewer/RO, reducir la operación a la lectura mínima permitida. Si la mutación es genuina, seleccionar la capability RW/operator existente. No alterar ACLs ni crear un bypass sólo para facilitar el diagnóstico.
6. **Enrutar timeout.** Estrechar query/comando antes de proponer expansión de policy. Para PostgreSQL, consultar [[aranea-postgres-mcp]] por timeouts de rol. Para MongoDB, acotar tamaño de resultado/filtro. Para SSH, partir lecturas viewer compuestas cuando la policy o la semántica del shell sea el problema.
7. **Enrutar MCP HTTP `invalid request`.** En smokes de transporte manual, validar headers/sesión de protocolo antes de diagnosticar el backend de datos. Ver [[aranea-mongodb-mcp]] o [[aranea-postgres-mcp]] según aplique.
8. **Disciplina de cambio.** Al agregar o cambiar una capability MCP Aranea: actualizar primero [[aranea-mcps-expert]]; actualizar el runbook de familia correspondiente en `80-agents/memory/public/runbook/`; actualizar skills consumidoras de dominio sólo si cambió su routing/ownership; nunca persistir material bearer/password/private-key en docs; validar conectividad del cliente y least-privilege end-to-end.

## Validación

Success requiere:

```text
Plane symptom:       missing|401|POLICY_DENIED|timeout|invalid request
Client vs backend:   distinguished
Family runbook:      loaded only after plane/auth is discarded or scoped
Bypass:              none
Secrets:             none persisted
```

Checklist:

- [ ] El síntoma se clasificó como plano MCP/cliente y no se abrió un dump de backend por default.
- [ ] Se cargó sólo el runbook de familia necesario, o ninguno si el fallo es puramente de cliente/auth.
- [ ] No se pidieron ni persistieron secretos.
- [ ] No se publicaron backends internos ni se crearon side channels.

Cualquier bypass o persistencia de secreto deja la operación `ABORTED`.

## Rollback / recuperación

Abortar sin mutar cuando:

- falta la capability y el único workaround sería publicar un backend;
- `401` no se puede resolver sin que el usuario pegue el bearer;
- resolver el conflicto exigiría cambiar policy o ACLs fuera de scope.

Ante fallo:

1. registrar capability afectada y el boundary cliente/backend;
2. no rotar secretos preventivamente;
3. handoff al runbook de familia sólo cuando el plano MCP ya no es el sospechoso;
4. no emitir éxito para un diagnóstico que no distingue cliente de backend.

## Evidencia

Registrar al cerrar:

- capability afectada;
- boundary cliente/backend que falló;
- evidencia recolectada;
- acción correctiva;
- resultado de validación;
- riesgo residual.

Los secretos nunca forman parte del closeout.
