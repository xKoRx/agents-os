---
type: evidence_pack
schema_version: 1
status: final
created: "2026-10-18"
updated: "2026-10-18"
area: "[[Echo]]"
project: "[[Echo Forge — Operación Real V2]]"
baseline: "xKoRx/symphony 492a271e (release 0.3.1)"
tags:
  - kind/evidence-pack
  - area/echo
  - tech/performance
---

# JVM-LAUNCH-CONTRACT — cómo lanza Forge el JVM de SQX 144 (verificado en flota)

## Cadena de lanzamiento (los 3 hosts, idéntica)

1. **systemd** `stager-runtime.service` + drop-in `/etc/systemd/system/stager-runtime.service.d/symphony-canary.conf`: `User=kor`, `EnvironmentFile=/etc/environment` (sin vars Java), `Environment="JAVA_TOOL_OPTIONS=-Xms34g -Xmx55g -XX:MaxDirectMemorySize=1g -XX:MaxMetaspaceSize=512m -XX:ReservedCodeCacheSize=256m -Xss1m -XX:+ExitOnOutOfMemoryError"`, `WorkingDirectory=/var/lib/symphony`, `MemoryMax=infinity`, sin `CPUQuota`/`CPUWeight`/`Nice`/`CPUAffinity`.
2. **Worker Go** `/opt/stager/releases/0.3.1/bin/symphony` (PID hijo, 26–38 hilos, nice 0). El JAR/snippet de evidencia ya no participa en el lanzamiento.
3. **`sqx/adapters/cmd-executor/process_nonwindows.go`**: `exec.CommandContext(ctx, binaryPath, args...)` con `Setpgid: true` (grupo de proceso propio del comando); **no setea `cmd.Env`** ⇒ el proceso sqcli hereda íntegro el environment del worker, incluido `JAVA_TOOL_OPTIONS`. Sin wrapper, sin nice, sin affinity.
4. **Binario** `/home/kor/sqx/144/sqcli` (resuelto por `runtime.GetSQXExecutablePath()` = `<exec_root>/<sqx_version>/sqcli` con `sqx.exec_root=/home/kor/sqx`, `sqx.sqx_version=144` desde ETCD; evidencia: log worker Hera 05:07:09Z y full_command `/home/kor/sqx/144/sqcli -project action=start name=custom`). Es un **ELF 64-bit Go** que lanza él mismo la JVM (no es script; el `run_sqcli.sh` de 144 existe pero Forge NO lo usa).
5. **JVM** `j64/bin/java` = Zulu OpenJDK **25.0.2** LTS 64-bit (idéntico en los 3 hosts).

## Opciones JVM efectivas

El JVM antepone `JAVA_TOOL_OPTIONS` y después recibe los `option` de `/home/kor/sqx/144/sqcli.config` como argumentos; los duplicados se resuelven por última aparición:

- De JTO (unidad systemd): `-Xms34g -Xmx55g -XX:MaxDirectMemorySize=1g -XX:MaxMetaspaceSize=512m -XX:ReservedCodeCacheSize=256m -Xss1m -XX:+ExitOnOutOfMemoryError`
- De sqcli.config (desde instalación, mtime 2026-06-01): `-Djava.net.useSystemProxies=true -Djava.net.preferIPv4Stack=true -XX:+UseParallelGC -Djdk.tls.trustNameService=true --enable-native-access=ALL-UNNAMED -Xms4g`
- **Efectivo: `-Xms4g` (sqcli.config pisa al 34g de JTO por venir último) `-Xmx55g` (solo JTO) `-XX:+UseParallelGC`** y el resto de las flags no duplicadas.
- Prueba física: durante el builder de 69 min Kronos usó ~12 GB de RSS (sar -r: 12,2–12,7 GB kbmemused); con `-Xms34g` efectivo el heap inicial comprometería 34 GB de inmediato. La doble declaración es redundante pero inocua; documented as-is (REMEDIATION-PLAN ítem 3).

## Qué NO interviene

- `/home/kor/sqx/sqcli` (symlink → `142/sqcli`) es solo la ruta de mantenimiento ETCD `sqcli/binary_path`; el executor no la usa.
- `run_sqcli.sh` de 144 (`JAVA_TOOL_OPTIONS -Xms34g -Xmx55g; ./sqcli -gui`) no forma parte del camino headless; su existencia no afecta al CLI (mismo JTO ya presente en la unidad, misma cifra).
- No existe `-XX:ActiveProcessorCount` en ninguna fuente ⇒ `Runtime.availableProcessors()` = cores del host (28/64/76), corroborado por las líneas SQX "Using: N cores".
