---
type: change_log
schema_version: 1
scope: session
created: "2026-09-18"
updated: "2026-09-18"
area: "[[Aranea]]"
project: "[[HERMES — Infrastructure Operations]]"
application:
entities:
  - "[[HERMES — Infrastructure Operations]]"
  - "[[HERMES — ARANEA AUTONOMOUS OPERATIONS]]"
related:
  - "[[windows-operator-contract]]"
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
  - area/aranea
  - project/hermes-aranea-autonomous-operations
  - domain/infrastructure
---

# 2026-09-18-w1-windows-native-bootstrap

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created + updated
- **Archivo(s):**
  - `10-projects/Aranea/agentes/HERMES — Infrastructure Operations.md` — objetivo inmediato, intro matriz H3 (nota W1), fila worker-kronos de la matriz H3, nota de ejecución del bundle, llaves de recuperación, gate H3 (→ `H3 ENABLEMENT PASS — VERIFIED SCOPE`), Estado actual (bullet W1 + reclasificación de la fase read-only), Bitácora (entrada W1).
  - `30-resources/runbooks/windows-operator-contract.md` — habilitación W1 incorporada: canal SSH nativo VERIFIED con identidad/procedimiento/validación/revoke reales; spec pendiente marcada EJECUTADA.
  - `30-resources/aranea/01-topologia/fechas-captura.md` — fila de probes/certificación W1 (2026-09-18 noche, drift 0).
  - `10-projects/Aranea/HERMES — ARANEA AUTONOMOUS OPERATIONS.md` — fila H3 del rollout (enablement-only) y Estado actual (H3 PASS), Bitácora (entrada W1).
  - `80-agents/journal/logs/2026-09-18-w1-windows-native-bootstrap.md` — este log.

## Motivo

- Mandato owner W1 (2026-09-18): resolver integralmente el bloqueo Windows de H3 habilitando un canal administrativo NATIVO, autenticado, seguro y recuperable para que Ariadna administre worker-kronos sin depender del MCP Access Plane. Autorización estrictamente delimitada a VM 135 (verificación de identidad en vivo previa a cualquier escritura); las mutaciones necesarias para instalar el acceso se registran como mutaciones reales (no ZERO INFRASTRUCTURE MUTATIONS); después de W1, Infrastructure Operations vuelve a boundary enablement-only.

## Fuentes usadas

- Canon: [[HERMES — Infrastructure Operations]] (matrices H1/H2/H3), [[windows-operator-contract]], bundle `~/aranea/work/h3-enablement-20260918/owner_bundle_draft.md` (sección W1), change logs H1/H2/H3 del día, inventario vivo PVE vía SSH `ariadna` (llave `~/.ssh/ariadna_pve`).
- Discovery y certificación en vivo (evidencia fuera del vault, `~/aranea/work/w1-windows-native-20260918/`): `qm config/status 135`, `qm guest cmd 135 network-get-interfaces/get-osinfo/get-time`, exec read-only (usuarios, grupos, servicios, registro, firewall, sshd_config, ACLs, netstat), probes SSH de autenticación, logs `sshd.log`, G4 hijo fresco con transcript (`g4/`).

## Resolución aplicada

- **Target proof doble:** VM 135 @ kronos RUNNING (`name: worker-kronos`, `agent: 1`, `ostype: win11`); IP viva del guest `192.168.31.128` vía `network-get-interfaces` — coincide con DNS `mt5-kronos.lab.aranea.cl` (el `.133` del bundle era supuesto: drift corregido ANTES de mutar); origen autorizado verificado (VM 118 `agent` = hermes-vm, .122).
- **Discovery (read-only, qm guest exec):** OpenSSH for Windows 9.5 YA instalado y RUNNING (Auto, LocalSystem, listener `0.0.0.0:22`, conexión ESTABLISHED del plano consumer .161) — instalación consumer con `authorized_keys` de `echo-dev` (`echo-dev@mcps`); `ariadna-win` NO existía; `administrators_authorized_keys` NO existía; sshd_config con `Match Group administrators → __PROGRAMDATA__/ssh/administrators_authorized_keys` (no modificado); firewall con regla preexistente "OpenSSH SSH Server (sshd)" (In/Private/TCP22/Any) — NO tocada (el plano .161 depende de ella); Guest INACTIVO; Administrators pre = {Administrator, KoR}.
- **Transporte (REUSE > CONFIGURE > INSTALL):** OpenSSH for Windows reutilizado; alternativa WinRM/HTTPS descartada (instalaría segundo servicio; el port 5985/5986 ni siquiera está abierto).
- **Gate de bootstrap:** canal host-mediated `qm guest exec` (agent PVE ya certificado H2/H3) como mecanismo de instalación; QGA no se presenta como management nativo: el canal certificado es SSH con identidad propia.
- **Mutaciones exactas (todas acotadas a VM 135 y reversibles):** (1) usuario local `ariadna-win` creado + Administrators — password aleatoria generada DENTRO del guest y descartada (jamás transitó red/chat/vault; autenticación W1 = 100% llave); (2) `C:\ProgramData\ssh\administrators_authorized_keys` creado con ACL canónica (`inheritance:r; SYSTEM:F; BUILTIN\Administrators:F`) y UNA línea `from="192.168.31.122" ssh-ed25519 AAAA…Gddx ariadna-win-w1-20260918` (llave nueva `~/.ssh/ariadna_win` en hermes-vm, 600); (3) `known_hosts` de hermes-vm pinneado con la host key ed25519 obtenida por fuente independiente (ssh-keygen inside-guest: `SHA256:OKjlEQRES+YmmLYmq3SS5z4LRtegcD0Xl0mRubZY3us`); (4) alias `worker-kronos` en `~/.ssh/config`; (5) fixture de staging `C:\Windows\Temp\w1.ps1` borrado tras uso (verificado). Instalador idempotente `W1_INSTALL_IDEMPOTENT.ps1` (sha256 `26bf13f6…20fd8a63`) stageado byte-exacto (base64+certutil). NO se tocaron: echo-dev, KoR, Administrator, Guest, sshd_config, firewall, servicios, tareas, MT5. SIN restart de sshd (PID 1056 / StartTime 9/10 intactos) ni de Windows.
- **Incidente de proceso (corregido y registrado):** el marcador de idempotencia reportó "KEY already present" con `keycount=0`; el ground truth (type + dir, size=0) mandó sobre el log: archivo vacío confirmado, llave instalada por `[IO.File]::AppendAllText` verificado inmediatamente (107 bytes, contenido correcto). Causa: `Add-Content -Raw` con entrada de pipeline no escribió el contenido. Lección: en staging multi-hop, verificar contenido real del archivo tras CADA escritura, no confiar en el log del script.
- **Certificación positiva (SSH nativo desde .122):** `whoami` → `worker-kronos\ariadna-win`; grupos con token admin completo (S-1-5-114 + S-1-5-32-544); lecturas administrativas que con echo-dev estaban denegadas (0x80041003) ahora PASS: `Get-CimInstance Win32_Service` (sshd Running/Auto/LocalSystem) y `Get-ScheduledTask` (`AraneaEvidencePublish: Ready`). Logs del target (`sshd.log`): `Accepted publickey for ariadna-win from 192.168.31.122 … ED25519 SHA256:EBKQ…`.
- **Certificación negativa:** sin credencial (kor) → Permission denied; llave equivocada (ariadna_pve) → Permission denied; restricción de origen a NIVEL IDENTIDAD (`from=` nativo de OpenSSH, línea verificada in-guest) — el firewall/listener quedan como estaban (dependencia del plano consumer documentada; sin exposición nueva atribuible a W1).
- **No-impacto:** sshd sin restart (mismo PID/StartTime), conexión consumer .161:42758→:22 viva antes/durante/después (misma conexión que el discovery pre-mutaciones), `qm guest exec` operativo, resto del guest sin cambios (usuarios/grupos post = baseline + ariadna-win).
- **Golden G4 (sesión fresca aislada, sin MCP, sin secretos en el prompt):** 10/10 PASS — resolución por nombre lógico desde Matriz H3 → VM 135@kronos → endpoint .128 → identidad W1 → host key pinneada verificada → autenticación SSH → lectura CIM administrativa → tarea programada → `mcp_calls=0` → revoke/recovery identificados. Nota: un primer intento de hijo G4 murió por hang del provider (esperando respuesta del modelo, sin ejecutar nada); el segundo ejecutó completo. Evidencia: `~/aranea/work/w1-windows-native-20260918/g4/`.

## Veredicto

**W1 PASS.** Administración Windows nativa funcionando, acceso efectivo desde Ariadna por SSH con identidad dedicada, autenticación por llave con host key pinneada, permisos administrativos demostrados por lecturas antes denegadas, restricción de origen demostrada (from= + firewall intacto), independencia del MCP demostrada (G4 mcp_calls=0), recovery/revoke documentados, sin impacto no autorizado. Mutaciones W1 enumeradas y revertibles (rollback RB-01/02/03 que NO depende del canal nuevo). **Con W1 PASS, H3 pasa de `PARTIAL — LINUX ENABLED / WINDOWS BLOCKED` a `H3 ENABLEMENT PASS — VERIFIED SCOPE`: el alcance Windows certificado queda explícitamente limitado a worker-kronos VM 135** (no implica flota Windows habilitada; WinRM no provisionado; resto de Windows sin canal propio).

## Siguiente exacta

Infrastructure Operations vuelve a su boundary enablement-only (W1 fue excepción única). H4 (provisioning enablement) NO se inicia por iniciativa propia. Pendientes opcionales heredados del bundle: L1 (daedalus docker-grupo/sudo) y L2 (qemu-guest-agent en guests sin agent) — requieren decisión owner propia. Publicación vault→GitHub por flujo canónico con verificación por archivo y contenido.
