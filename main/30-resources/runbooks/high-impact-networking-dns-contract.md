---
type: runbook
schema_version: 1
scope: area
created: "2026-09-19"
updated: "2026-09-19"
area: "[[Aranea]]"
project: "[[HERMES — Infrastructure Operations]]"
application:
entities:
  - "[[Aranea]]"
  - "[[HERMES — Infrastructure Operations]]"
related:
  - "[[cluster-node-maintenance-contract]]"
  - "[[proxmox-lifecycle-operator-contract]]"
  - "[[hermes-linux-update-recovery]]"
aliases:
  - high impact networking dns contract
  - contrato networking dns high-impact
  - H5 networking contract
confidence: high
source_session:
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/runbook
  - scope/area
  - area/aranea
  - action/high-impact
  - tech/networking
  - tech/dns
---

# high-impact-networking-dns-contract

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Propósito

Contrato del futuro operador de networking/DNS de alto impacto Aranea (familias A, B y parte de J del índice [[30-resources/aranea/06-high-impact/00-index|high-impact]]). Cubre gateway (OPNsense), DNS interno (Pi-hole + wildcards), DHCP, VPN/Tailscale y el firewall del borde. **Enablement-only:** este contrato NO autoriza ninguna operación; la ejecución pertenece al proyecto ejecutor que lo consuma con autorización owner explícita para cada cambio CLASS 2/3.

Estado habilitación por familia (2026-09-19): **A/B = PARTIAL** — inventario y lectura verificados; sin recovery documentado para OPNsense; configuración interna de OPNsense/iptables no legible con la autoridad actual (ROOT-EQUIVALENT AVAILABLE / NOT EXERCISED sobre el guest).

## Targets y canales

| Target | Identidad estable | Canal nativo certificado | Autoridad actual | Recovery documentado |
|---|---|---|---|---|
| OPNsense | qemu/130 @athena, gateway LAN/WAN, SPOF | Ninguno certificado (sólo qm status vía host) | ROOT-EQUIVALENT AVAILABLE / NOT EXERCISED (ariadna+sudo en athena) | NO — gap principal |
| Pi-hole | lxc/149 @athena, DNS .31 | `pct exec 149` vía athena (ejercitado read-only H5) | ROOT-EQUIVALENT AVAILABLE / NOT EXERCISED | NO (rebuild = ticket community-script) |
| Tailscale gateway | lxc/119 @athena, IP TS 100.75.167.57 | `pct exec 119 -- tailscale status` (ejercitado read-only H5) | AUTHORIZED_NOT_EXERCISED | NO |
| PVE firewall | datacenter/nodos | `pve-firewall status`, `nft list ruleset` (H5: disabled, 0 reglas) | VERIFIED_READ | n/a (disabled) |
| step-ca | lxc/200 @athena STOPPED, CA .12 | `pct config/status` (H5) | AUTHORIZED_NOT_EXERCISED | NO — CA sin backup documentado |

## Precondiciones (para el ejecutor futuro)

1. Target proof doble: VMID + nodo + estado vivo (recuerda N4: `ca.lab.aranea` resuelve aunque el servicio esté stopped).
2. Ventana de mantenimiento aprobada por el owner — todo cambio en gateway/DNS es CLASS 3 y puede dejar fuera a Ariadna y al owner.
3. Owner presencial o consola física/iLO/KVM accesible: si el cambio falla, la recuperación puede requerir acceso fuera de banda.
4. Plan de rollback escrito ANTES del cambio, con la configuración actual respaldada (`pct config 149`, export de config OPNsense desde su UI por el owner).
5. Concurrencia: ningún otro cambio de red en vuelo; verificar que PBS/backup jobs no estén corriendo (dependencia de red).

## Clasificación de operaciones

- CLASS 1 (scoped, requiere contrato + target proof): reinicio de un servicio no crítico dentro de un guest de red; añadir una entrada DNS local en Pi-hole.
- CLASS 2 (compartido): cambio de wildcard `*.lab.aranea` / `lab.aranea.cl`; regla de firewall PVE (hoy disabled); cambios en Tailscale ACL.
- CLASS 3 (owner-gated siempre): reinicio/reconfig de OPNsense, cambio de DHCP, cambio de IP de Pi-hole o de su upstream, reconfig de bridges/vlans en athena, emisión/rotación de CA raíz.

## Procedimiento (plantilla del ejecutor — no ejecutado)

1. Snapshot/pre-captura: `qm status`, config del guest, reglas vigentes, `getent hosts` de los FQDN críticos antes del cambio.
2. Aplicar el cambio mínimo con la ventana activa y owner alcanzable.
3. Verificación inmediata desde TRES puntos: hermes-vm (.122), otro nodo PVE, y un cliente externo si aplica (DNS + gateway + un servicio publicado vía Traefik).
4. Registro: qué cambió, timestamp, evidencia en `~/aranea/work/<run>/`.

## Validación

- DNS: `getent hosts mt5-kronos.lab.aranea.cl` y `dashboard.lab.aranea` resuelven desde hermes-vm y desde un nodo.
- Gateway: default route de un nodo responde; WAN accesible (DNS upstream vivo).
- Tailscale: `tailscale status` vivo en 119 y peer alcanzable si aplica.
- SSH management de Ariadna intacto (las llaves `from=.122` siguen funcionando a los 5 nodos).

## Rollback / recuperación

- Rollback = restaurar la pre-captura (config guest o export OPNsense). NO existe runbook de recuperación de OPNsense: hasta que exista, cualquier intervención en 130 requiere owner presencial.
- Si el cambio deja a Ariadna fuera: consola PVE del owner sobre athena (break-glass universal) y revertir desde ahí.
- Recovery de Pi-hole documentado como reconstrucción (ticket community-script) — NO certificado.

## Evidencia

- Sondas read-only 2026-09-19 15:42–15:50 UTC: `~/aranea/work/h5-high-impact-20260919/probes/` (`pve_probe_20260919_10.txt`, `athena_probe_20260919.txt`).
- Cambio canónico del mandato H5: `80-agents/journal/logs/2026-09-19-h5-high-impact-enablement.md`.
