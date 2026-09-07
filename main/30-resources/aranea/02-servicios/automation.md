---
type: doc
schema_version: 1
status: active
area: "[[Aranea]]"
related: []
aliases: []
tags:
  - kind/doc
created: 2026-08-10
updated: 2026-08-10
---

# Automatización

## Propósito

Documentación canónica legacy de [[Aranea]]; se conserva el contenido histórico y su estado requiere verificación antes de uso operativo.

## Contenido


> **Capturado**: 2026-06-28

## homeassistant (qemu/105)

| Item | Valor |
|---|---|
| **Propósito** | Smart home hub — automatizaciones, dispositivos IoT |
| **VMID** | 105 |
| **Tipo** | qemu VM |
| **Nodo** | hades |
| **vCPUs** | 4 |
| **RAM** | 8 GB |
| **Disco** | 50 GB |
| **NetIn** | 12 GB |
| **NetOut** | 552 MB |
| **Estado** | ✅ Running |

### Integraciones probables

- Luces, enchufes, sensores
- EMQX (MQTT broker) como canal de comunicación con dispositivos
- Posible integración con Frigate para eventos de cámara

> Ver también [[media-domotica]] para contexto.

## Runbooks (herramientas)

> [!note] Runbooks declarativos
> El homelab Aranea todavía no tiene sistema formal de runbooks (como las **step-ca setup scripts** que están en `~/aranea/traefik/`). Las decisiones operativas se documentan como tickets en `~/aranea/tickets/`.

### Workflow actual de cambios

1. **Hermes** propone cambio → crea ticket en `pending`
2. **Rodrigo** aprueba → cambia a `approved`
3. **Hermes** ejecuta vía wrappers → cambia a `applied`/`failed`
4. **Post-validación** documentada en el ticket

Ver `~/aranea/tickets/README.md` para la convención completa.

## Cron / scheduling

- No documentado en el wrapper `agent-read`
- truenas + PVE tienen `cron.service` running en todos los nodos

## Workflow engines

### temporal (qemu/158)

Ver [[ml-ia]] § temporal. Orquestador de procesos async.

### k8s-node-2 (qemu/120)

| Item | Valor |
|---|---|
| **Propósito** | Nodo Kubernetes (template stopped) |
| **VMID** | 120 |
| **Tipo** | qemu (template) |
| **Nodo** | hera |
| **vCPUs** | 5 |
| **RAM** | 12 GB |
| **Disco** | 32 GB |
| **Tags** | `kubernetes`, `template` |
| **Estado** | ⏸️ **Stopped (template)** |

> Cluster k8s **no implementado**. Solo template definido en hera.

### docker-hasura (lxc/129)

| Item | Valor |
|---|---|
| **Propósito** | Hasura GraphQL Engine |
| **VMID** | 129 |
| **Tipo** | lxc container |
| **Nodo** | hades |
| **vCPUs** | 4 |
| **RAM** | 8 GB |
| **Disco** | 50 GB |
| **Tags** | `community-script`, `docker` |
| **NetIn** | 486 GB |
| **NetOut** | 325 GB |
| **Estado** | ✅ Running |

> Hasura expone APIs GraphQL sobre Postgres. Probable capa de automatización.

## Resumen

| Componente | Estado |
|---|---|
| homeassistant | ✅ Running |
| tickets workflow | ✅ Convencional (no es servicio) |
| cron systemd | ✅ En todos los nodos |
| temporal | ✅ Running |
| k8s-node-2 | ⏸️ Template stopped |
| docker-hasura | ✅ Running |

## Alertas

- 🟡 homeassistant en hades (concentración, pero aceptable para IoT)
- 🟡 k8s-node-2 como template stopped — sin cluster k8s operativo
- 🟡 Sin Prometheus + Alertmanager → alertas manuales vía tickets

---

**Source files**: `/home/hermes/aranea/topology/services.md`, `/home/hermes/aranea/tickets/README.md`

**Captured**: 2026-06-28 21:18 UTC. Doc generado 2026-06-30.
