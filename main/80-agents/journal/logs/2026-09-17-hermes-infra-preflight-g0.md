---
type: change_log
schema_version: 1
scope: aranea
created: 2026-09-17
project: "[[HERMES — Infrastructure Operations]]"
tags:
  - kind/change-log
  - area/aranea
  - project/hermes-aranea-autonomous-operations
---

# 2026-09-17 — Preflight G0 mandato Infrastructure Enablement

## Contexto

Mandato owner "HERMES INFRASTRUCTURE ENABLEMENT" (ventana 10h, referencia 18-09): adelantar trabajo reutilizable para administración progresiva de Aranea por Hermes, orden obligatorio preflight → implementación → integración → certificación → handoff. Este log registra el preflight G0 y su evidencia.

## Ejecutado (2026-09-17 21:52–19:0x UTC, hermes-vm)

1. **Bootstrap canónico Agents-OS** ejecutado (constitución + perfil global + continuidad + registry de skills). `VAULT_ROOT=/home/hermes/obsidian/SecondBrain/main` verificado.
2. **Validación matrix agent-read: 6/6 PASS** (athena/zeus/hera/kronos/hades/truenas; probe `sudo -n <wrapper> node`).
3. **Captura `all` 6/6 OK** → `~/aranea/topology/discovery/<nodo>_20260917_185839.txt` (athena ~634 KB, resto ~82–88 KB, tamaños esperados).
4. **Inventario materializado** → `~/aranea/topology/inventory_20260917_185839.json` (59 VMs: 42 running / 17 stopped; 10 storages PVE; shape_gaps documentados por el script).
5. **Smoke management paths**: `mcps-ops` OK (hostname `mcps`, sudo activo, 26 containers), `daedalus-ops` OK (key-only, sin sudo — por diseño).
6. **Runtime Hermes**: config MCP leída — sólo `aranea-postgres-ro` configurado. SSH config: aliases `mcps-ops`, `daedalus-ops`. `gh`/`sshpass` ausentes (no requeridos aún).
7. **Canon actualizado por delta** (30 patches OK): `00-index.md` (callout frescura + totales 36/19→42/17), `fechas-captura.md` (6 filas nuevas + 20260916 marcada superseded + drift), 6 `nodo-*.md` (Capturado/Fuente primaria/previa/Alcanzabilidad), `20-areas/Aranea.md` (inventario + status_detail), proyecto [[HERMES — Infrastructure Operations]] (bitácora + matriz authority + I0.1–I0.4 cerrados con evidencia).

## Hallazgos de preflight

1. **`sync.sh` sin scheduler verificado**: el repo `~/workspace/agents-os-repo` (origin `xKoRx/agents-os`, master, limpio) tiene `sync.sh` (commit+rebase+push cada 1 min) pero en hermes-vm NO hay cron de usuario ni timer systemd que lo ejecute y `.sync/sync.log` está vacío. Los últimos commits "sync HH:MM" (18:14–18:16 -03) llegaron por otra vía no identificada. Pendiente: identificar el mecanismo real antes de confiar en sync automático.
2. **Repo main/ es copia, no symlink** de `VAULT_ROOT` (inodos distintos). La edición canónica es en vault; el repo requiere sincronización para publicar.
3. **Gap G3 (integración runtime)**: Hermes runtime sólo consume `aranea-postgres-ro`; el resto de capacidades (ssh family, hasura, temporal, minio, etcd, mongo) no están en `~/.hermes/config.yaml` aunque existen en el plane.
4. **Inventario**: 59 VMs coincide con R0; delta vs doc del index (36/19) era drift del doc, corregido.

## Authority verificada (resumen — detalle en proyecto)

| Target | Clase |
|---|---|
| 6 nodos vía agent_ro + agent-read | observe (wrapper-only; bypass = violación de canal) |
| LXC mcps vía mcps-ops | operate completo (AUTO per contrato) |
| daedalus vía hermes-ops (ACL-scoped) | operate consumer configs gestionadas |
| hermes-vm self | operate (systemd --user) |
| Windows worker-kronos vía ssh-mcp | observe/operate parcial (plano MCP) |
| APIs nativas Proxmox/TrueNAS | **absent** — owner action requerido para H2/H4 |

## Estado de gates del mandato

- **G0**: PASS (este log + bitácora del proyecto). Baseline, contratos y authority confirmados.
- **G1**: candidato PASS — discovery integrado y auditable (captura + JSON + canon delta). Cierre formal junto con matriz de cobertura por máquina.
- **G2/G3/G4**: no iniciados (requieren implementación de componentes e integración en config runtime — G3 tocará `~/.hermes/config.yaml`, archivo protegido que exige consentimiento owner).

## Siguientes pasos (orden del mandato)

1. **Bloqueante de procesos**: aclarar el mecanismo de sync del repo agents-os (hallazgo 1) — es el canal de publicación de commits exigido por la entrega.
2. Implementar componentes independientes (workstreams A–D) sobre el baseline G0/G1.
3. Integración G3: batch de MCPs al runtime + consentimiento owner para `config.yaml`.
4. Certificación G2/G4 por familia (Linux/Windows/Proxmox/TrueNAS) hasta el nivel de authority permitido.
