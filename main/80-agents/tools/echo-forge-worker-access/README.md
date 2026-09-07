# Echo Forge worker access — distribución simple

Fuente canónica de `echo-forge-worker`, su instalador por Mac y un único archivo de credenciales en texto plano aprobado explícitamente por el owner. El wrapper local es un symlink derivado en `~/bin/`.

## Instalación

```bash
80-agents/tools/echo-forge-worker-access/install
echo-forge-worker status
```

En cada Mac que tenga el vault, ejecutar el instalador una vez. El symlink hace que Codex, Claude Code, Cursor y Antigravity usen la misma fuente sincronizada. No depende de la Apple Account: funciona en cualquier Mac que tenga una copia legible del vault y `sshpass` instalado.

## Contrato

- Fuente canónica: este directorio.
- Instalación local derivada: symlink `~/bin/echo-forge-worker`.
- Credencial canónica única: `credentials.env` en este directorio.
- La deuda de seguridad y los TODO futuros están comentados dentro del archivo de credenciales.
- Nunca repetir el valor en Markdown, logs, journal, argumentos visibles ni otros archivos.
