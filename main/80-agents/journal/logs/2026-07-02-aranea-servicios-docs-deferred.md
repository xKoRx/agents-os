# 2026-07-02 — Proyecto SERVICIOS-DOCS-OWNER-PROJECT + ticket 022

## Cambio inicial (sesión formulario Backup/DR)

Por instrucción del owner ("déjalo como tarea para más adelante"), se registra como deferred la iniciativa de **documentar servicios individuales** en el Second Brain.

## Corrección crítica (post-feedback airado del owner)

> **El agente interpretó mal el alcance y clasificó servicios sin seguir lo que el owner nombró explícitamente.**

El owner corrigió con énfasis en:
1. **Aranea NO es homelab hobby**, es **datacenter para el sistema de trading algorítmico "echo"**.
2. Cuando el owner nombra ejemplos (argus, etcd, bases de datos), esos son **EL SCOPE**, no sugerencias para el agente amplíe.
3. **Trading no puede quedar abajo** — es el core que subsidia el homelab.

### Scope inicial corregido (definido por owner)

**21 servicios tier 0** agrupados en 4 capas:

| Capa | Cantidad | Servicios |
|---|---|---|
| Tier 0a — Infraestructura base | 3 | opnsense (130), pi-hole (149), traefik (115) |
| Tier 0b — Storage | 1 | truenas (145) |
| Tier 0c — Cluster quorum crítico | 9 | etcd cluster 5 nodos (101/147/154/155/156) + etcd-keeper UI (148) + kafka 3 brokers (136/138/139) |
| Tier 0d — Sistema echo (trading) | 8 | mt4-demo/real/ftmo/ttp (144/124/133/134) + echo (140) + postgres (152) + mongo (153) + argus (160) |

**etcd**: siempre 5 nodos, NUNCA menos de 3 (bajar de 3 = "warning feo").

### Segunda corrección (owner agregó 2 servicios)

A pedido del owner, se suman `docker-flink (126)` y `docker-hasura (129)` al tier 0d — son parte fundamental de echo.

**Scope final**: **23 servicios tier 0** (3 + 1 + 9 + 10).

### Servicios FUERA de scope (no se documentan sin orden explícita)

mcps, obsidian-sync, docker-observability, emqx, frigate, homeassistant, ubuntu-dev, temporal, sqx-ulab-*, win-*, docker-kafka, etc.

## Archivos creados (ciclo deferred)

| Path | Tipo | Tamaño |
|---|---|---|
| `10-projects/Aranea/SERVICIOS-DOCS-OWNER-PROJECT.md` | proyecto | 7.3 KB |
| `10-projects/Aranea/agentes/agent-project-09-service-docs-rollout.md` | subproyecto agente | 5.2 KB |
| `10-projects/Aranea/05-tickets/2026-07-02-022-deferred-service-docs.md` | ticket formal | 4.6 KB |

## Archivos actualizados (ciclo deferred)

- `10-projects/Aranea/README.md` — tabla de proyectos (+1 fila) + árbol de estructura.
- Los 3 archivos del proyecto se corrigieron post-feedback del owner para reflejar el scope real.

## Lección aprendida (memoria persistida)

> Cuando owner da ejemplos A, B, C en un mensaje → responder sobre A, B, C. NO inventar D-Z por completitud.
> "Déjalo como tarea para más adelante" = DEFER puro, NO invitación a análisis exhaustivo.
> Aranea = datacenter para sistema de trading algorítmico "echo", NO homelab hobby.

## Convención replicable (para futuras tareas deferred)

```text
1. Crear proyecto en 10-projects/<Área>/<SLUG>-OWNER-PROJECT.md con status: deferred, priority: P3
2. Crear agente subproyecto en 10-projects/<Área>/agentes/agent-project-NN-<slug>.md con status: pending
3. Crear ticket formal en 10-projects/<Área>/05-tickets/YYYY-MM-DD-NNN-<slug>.md con status: deferred, severity: low
4. Actualizar README del área con nueva fila en tabla + árbol de estructura
5. Log en 80-agents/journal/logs/
```

---

## Activación 2026-07-02 (post "dale arranca")

Por instrucción del owner, el proyecto pasa de deferred a active.

### Cambios de status

| Archivo | Antes | Ahora |
|---|---|---|
| `10-projects/Aranea/SERVICIOS-DOCS-OWNER-PROJECT.md` | `status: deferred, priority: P3` | `status: active, priority: P1` |
| `10-projects/Aranea/agentes/agent-project-09-service-docs-rollout.md` | `status: pending` | `status: in-progress` |
| `10-projects/Aranea/05-tickets/2026-07-02-022-deferred-service-docs.md` | `status: deferred, severity: low` | `status: open, severity: medium` |
| `10-projects/Aranea/README.md` | Fila 2 "deferred" | Fila 2 "active — Fase 1 tier 0a en curso" |

### Fase 0 (setup) — completada

- ✅ Template `70-templates/service-operational.md` creado (5.9 KB)
- ✅ Folder destino decidido: `30-resources/aranea/02-servicios/`
- ⚠️ NO se hizo validación piloto separada — interpreté "dale arranca" como "avanza sin más preguntas". Si owner quería piloto separado, lo agregamos como Fase 0.5 retroactivo.

### Fase 1 (Tier 0a) — completada

3 notas individuales creadas el 2026-07-02:

| Archivo | Tamaño | Status |
|---|---|---|
| `30-resources/aranea/02-servicios/opnsense.md` | 8.0 KB | `partial` |
| `30-resources/aranea/02-servicios/pi-hole.md` | 7.0 KB | `partial` |
| `30-resources/aranea/02-servicios/traefik.md` | 8.1 KB | `partial` |

Cada nota sigue el template `70-templates/service-operational.md` con:
- Frontmatter completo (vmid, node, tier, owner)
- Propósito describiendo el ROL en el sistema echo
- Acceso con campos explícitos + marcadores `> [!note] Pendiente` para datos faltantes
- Storage + backup policy ref
- Secrets SOLO con referencias (cero valores en plaintext)
- Operación (restart, health check, logs, update)
- Cross-refs bidireccionales con servicios del mismo host

### Pendientes explícitos por servicio

- **opnsense**: IP LAN de la VM, URL admin + puerto, SSH habilitado?
- **pi-hole**: IP del container, integración con Traefik, webpassword location
- **traefik**: IP del container, ubicación exacta de credenciales, qué servicios están realmente detrás

### Archivos actualizados en esta activación

- `30-resources/aranea/02-servicios/README.md` — agregada nota 2026-07-02 apuntando a las 3 notas individuales
- `10-projects/Aranea/agentes/agent-project-09-service-docs-rollout.md` — Fase 1 marcada completa

### Sin comandos ejecutados en Aranea

Esta activación es **solo persistencia en Second Brain**. Cero ssh, cero agent-read, cero cambios en infra.

## Captured

2026-07-02. Sesión formulario Backup/DR (deferred inicial) + sesión "dale arranca" (activación). Sin comandos ejecutados en Aranea. Solo persistencia en Second Brain.