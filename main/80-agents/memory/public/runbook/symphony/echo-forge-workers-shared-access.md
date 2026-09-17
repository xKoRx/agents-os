---
type: runbook
schema_version: 1
scope: application
created: "2026-08-11"
updated: "2026-08-11"
area: "[[Echo]]"
project: "[[Echo Forge]]"
application: "[[echo-forge]]"
entities:
  - "[[StrategyQuant X]]"
  - "[[Symphony]]"
related:
  - "[[sqx-instrument-sync-history-only-verification-gap]]"
  - "[[2026-07-29-sqx-watcher-missing-on-hera-kronos]]"
aliases:
  - Echo Forge worker access
  - acceso Mac a workers Symphony
  - echo-forge-worker
  - echo-forge-workers-macos-keychain-access
confidence: verified
source_session:
load_policy: when_application_loaded
indexable: true
index_priority: high
tags:
  - kind/runbook
  - scope/application
  - area/echo
  - project/echo-forge
  - app/echo-forge
  - tech/macos
  - tech/ssh
---

# Acceso compartido desde macOS a los workers de Echo Forge

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Propósito

- Dar a [[Codex]], [[Claude Code]], [[Cursor]] y [[Antigravity]] una interfaz común para acceder a los workers de Echo Forge.
- Por instrucción explícita del owner, la credencial vive temporalmente en `80-agents/tools/echo-forge-worker-access/credentials.env`; el wrapper la entrega directamente a `sshpass` o `sudo -S` y no la imprime.

## Precondiciones

- macOS con `sshpass` disponible y una copia sincronizada del vault.
- `~/bin` en `PATH`; si una superficie no lo hereda, usar `~/bin/echo-forge-worker`.
- Paquete canónico: `80-agents/tools/echo-forge-worker-access/`; `credentials.env` es la única fuente de la credencial y contiene warnings/TODO de endurecimiento.
- Mapeo no secreto: `zeus → 192.168.31.101`, `hera → 192.168.31.111`, `kronos → 192.168.31.121`.

## Procedimiento

1. En cada Mac, desde la raíz del vault, ejecutar `80-agents/tools/echo-forge-worker-access/install`; el instalador crea un symlink local en `~/bin/`, igual al patrón de distribución de Graphify.
2. Verificar la fuente sin mostrar el valor: `echo-forge-worker status`.
3. Consultar aliases: `echo-forge-worker workers`.
4. Abrir shell: `echo-forge-worker ssh zeus`.
5. Ejecutar un comando read-only: `echo-forge-worker ssh hera 'hostname; id -un'`.
6. Ejecutar sudo sin imprimir la clave: `echo-forge-worker sudo kronos systemctl status symphony-watcher.service --no-pager`.
7. Copiar hacia un worker: `echo-forge-worker scp-to ./archivo zeus /tmp/archivo`.
8. Copiar desde un worker: `echo-forge-worker scp-from hera /tmp/archivo ./archivo`.
9. Ejecutar el setup de proyectos desde el checkout Symphony: `echo-forge-worker setup-projects kronos`; si no se ejecuta desde el repo, pasar su path como segundo argumento o definir `SYMPHONY_REPO`.

### Contrato para agentes

- Usar únicamente `echo-forge-worker`; no hacer `source credentials.env` manualmente, no imprimir variables y no registrar trazas que contengan la clave.
- Codex, Claude Code, Cursor y Antigravity comparten el mismo wrapper y mapeo; no mantener copias por IDE.
- No proponer ni implementar otra solución de secretos sin nueva instrucción explícita del owner; la deuda futura está marcada en `credentials.env`.
- Las acciones remotas siguen requiriendo autorización normal según su impacto. Tener la credencial no autoriza mutaciones ni sudo indiscriminado.

## Validación

- `echo-forge-worker status` devuelve `Credentials: configured`, la ruta canónica y el usuario sin revelar el valor.
- `bash -n 80-agents/tools/echo-forge-worker-access/echo-forge-worker` pasa; `credentials.env` tiene modo `0600`; `~/bin/echo-forge-worker` apunta al wrapper canónico del vault.
- Smoke test SSH read-only del 2026-08-11: los tres hosts terminaron por timeout desde el entorno actual; la fuente de credenciales y la resolución local están verificadas, pero la conectividad end-to-end debe repetirse con LAN/VPN/ruta disponible.

## Rollback / recuperación

- Si el symlink falta o el vault cambió de ruta, volver a ejecutar el instalador canónico.
- Si cambia la credencial, editar sólo `credentials.env` y conservar el formato de dos variables; no repetir el valor en otro documento.
- Para retirar completamente el acceso, eliminar el symlink y el archivo de credenciales sólo por petición explícita; ambas acciones son destructivas.

## Evidencia

- Archivo canónico creado con modo `0600`; wrapper y symlink validados; comandos `status` y `workers` operativos.
- El paquete funciona en otro Mac al sincronizar/copiar el vault y ejecutar su instalador local; no depende de usar la misma Apple Account.
- Los timeouts simultáneos a `.101/.111/.121` indican ausencia de ruta o disponibilidad remota, no fallo de recuperación del secreto.
