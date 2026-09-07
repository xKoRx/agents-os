---
type: agent_memory
scope: project
tags:
  - kind/learning
  - project/symphony
  - area/sqx
created: 2026-07-15
updated: 2026-07-15
---

# Continuidad Cognitiva: Despliegue Remoto de sqx-watcher en Zeus

En esta sesión se migró por completo la ejecución de **SQX Watcher** (`sqx-watcher`) desde el entorno local (MacBook Pro) a la máquina remota **Zeus** (`192.168.31.101`) integrada de forma nativa en el pipeline del `deployer-watcher`.

## Contexto y Cambios

1. **Pipeline de Despliegue Ampliado**:
   - Se modificó [deploy_sqx.sh](file:///Users/rodrigojara/go/src/github.com/xKoRx/symphony/deploy_sqx.sh) para compilar transversalmente tanto `symphony` (worker) como `sqx-watcher` (watcher) para la plataforma `linux-amd64` en el directorio de release target.
   - Se actualizó el manifiesto local [deploy/manifest.json](file:///Users/rodrigojara/go/src/github.com/xKoRx/symphony/deploy/manifest.json) para incluir el de `"watcher"` apuntando a la ruta correspondiente en el bucket de MinIO para la nueva versión `0.1.121`.

2. **Detección Automática de Auto-Upgrade en el Watcher**:
   - Se implementó un bucle de monitoreo en [main.go](file:///Users/rodrigojara/go/src/github.com/xKoRx/symphony/sqx/cmd/sqx-watcher/main.go) que verifica periódicamente si el enlace simbólico `/opt/symphony/current` ha cambiado a un release diferente de la ruta física del ejecutable actual.
   - Si se detecta un cambio de release activo (debido al despliegue de una nueva versión por el stager), el watcher se auto-cancela ordenadamente. Esto permite que systemd lo reinicie cargando automáticamente el nuevo binario sin intervención humana.

3. **Configuración de Infraestructura en Zeus**:
   - Se actualizó `/usr/local/sbin/symphony-stager` en Zeus para descargar la llave `"watcher"` desde el manifest remoto e instalar el ejecutable en `/opt/symphony/current/bin/sqx-watcher` con permisos `0755`.
   - Se creó y habilitó el servicio systemd `/etc/systemd/system/symphony-watcher.service` en Zeus que levanta el watcher apuntando al directorio de entrada `/var/lib/symphony/input` bajo el usuario `kor`.

4. **Verificación y Monitoreo**:
   - Se compiló y liberó la versión `0.1.121`. El local `deployer-watcher` la cargó a MinIO actualizando el manifiesto.
   - El stager remoto de Zeus descargó ambos binarios y actualizó `/opt/symphony/current`.
   - Se detuvo la sesión de screen local del watcher (`watcher`), asegurando que no queden rastros locales.
   - Se inició el servicio systemd `symphony-watcher.service` en Zeus y se verificó por syslog que corre exitosamente en producción.
   - Se realizó una prueba E2E subiendo un archivo `config.json` y sus `.cfx` correspondientes a `/var/lib/symphony/input` en Zeus. El watcher los procesó correctamente de forma inmediata, lanzó el workflow de Temporal (`sqx-main-00_configs-v37-NDX-H1-L-1784084422`) y archivó los archivos procesados sin emitir trazas locales.
   - Se actualizó el índice de Graphify Personal (`graphify-personal update .`).
