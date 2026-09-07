---
type: runbook
schema_version: 1
scope: application
created: "2026-06-27"
updated: "2026-08-11"
area: "[[Echo]]"
project: "[[Echo Forge]]"
application: "[[echo-forge]]"
entities: []
related:
  - "[[echo-forge-workers-shared-access]]"
aliases:
  - Manipulación segura de archivos en workers remotos
  - Remote file manipulation runbook
confidence: high
source_session: "8c11ec26-7ad2-4f0d-a862-0c85ceebe285"
load_policy: manual
indexable: true
index_priority: high
tags:
  - agent/behavior
  - app/echo-forge
  - app/echoforge
  - area/echo
  - kind/runbook
  - project/echo-forge
  - project/echoforge
  - scope/application
---
# Safe File Manipulation on Remote Workers (Zeus, Hera, Kronos)

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Propósito

- Establecer el procedimiento seguro y auditable para inspeccionar y modificar archivos de configuración o de datos (ej: `.cfx`, `.json`, logs) en los workers remotos de Symphony (Zeus, Hera, Kronos), mitigando el riesgo de cambios mudos o corrupción de archivos remotos por edición directa sobre SSH.

## Precondiciones

- Conexión por SSH habilitada a los workers.
- Herramienta `scp`, `rsync` o utilidades del worker-ssh disponibles localmente.

## Procedimiento

1. **Localizar el archivo remoto:** Identificar la ruta absoluta en el worker (ej: `/var/lib/symphony/PENDING` o `/opt/symphony/CURRENT`).
2. **Descargar el archivo a la máquina local:**
   Usar `scp` para traer el archivo al entorno local (ej: a la carpeta de scratch o de artefactos):
   ```bash
   echo-forge-worker scp-from zeus /path/to/remote/file /path/to/local/workspace/
   ```
   *Nota: Si el archivo es muy pequeño y de texto plano, se puede usar redirección o lectura directa desde la terminal local, pero se prefiere SCP para mantener la integridad de binarios o archivos estructurados grandes.*
3. **Inspeccionar/Modificar localmente:**
   Utilizar las herramientas locales del agente para analizar o editar el archivo de forma segura (ej: scripts locales de Python para extraer y volver a zipear archivos `.cfx`, herramientas de parseo de JSON, etc.).
4. **Subir el archivo de vuelta al worker (si aplica):**
   Una vez manipulado, transferir el archivo editado de vuelta al servidor remoto en un path seguro (o temporal si requiere privilegios de root para reubicarlo):
   ```bash
   echo-forge-worker scp-to /path/to/local/file zeus /path/to/remote/target
   ```
5. **Aplicar privilegios (si es necesario):**
   Si se requiere mover el archivo a una ubicación protegida (ej: `/opt/` o `/etc/`), ejecutar un comando remoto con `sudo`:
   ```bash
   echo-forge-worker sudo zeus mv /tmp/file /opt/symphony/file
   ```

## Validación

- Validar que el archivo en el host remoto tiene el tamaño y contenido esperado mediante una lectura rápida de metadatos (`stat` o `md5sum` en remoto vs local).
- Monitorear el log del servicio correspondiente para asegurar que el cambio surtió efecto sin fallos de lectura o permisos.

## Rollback / recuperación

- Guardar siempre una copia local de respaldo del archivo remoto original antes de realizar cualquier modificación, para poder restaurarlo con un simple `scp` de vuelta en caso de error.

## Evidencia

- [[rjara-agent-profile]]
- [[echo-forge-workers-shared-access]]
