El runtime propio queda RUNNING en gRPC, vacío y disponible para root. El probe físico del host respondió ApiVersions en los cinco puertos 39092–39096: correlaciones 6101–6105, error 0,61 APIs y376 bytes por respuesta. Ambos clusters temporales se eliminaron; containers/volúmenes/redes propias y children SSH ausentes, cinco puertos libres. Esto certifica sólo infraestructura/readiness, no negocio ni SuiteFull.

El fallo inicial se localizó en el forwarding: cinco brokers HEALTHY dentro de la VM pero cinco SSH `-O forward` muertos por SIGKILL. `/usr/bin/ssh` fue el mismo ejecutable en hostagent y caller (SHA e22a8f30...). `-O check` funcionó; los cinco forwards nativos y el único túnel fresh sin multiplexado también recibieron señal 9. El emisor sigue UNKNOWN; no hay evidencia que atribuya la causa a VPN o permisos. El reinicio normal no corrigió el fallo.

Colima 0.8.1 no admite `--port-forwarder` y su fuente fija `LIMA_SSH_PORT_FORWARDER=true` en subprocess ([fuente v0.8.1, líneas 31–36](https://raw.githubusercontent.com/abiosoft/colima/v0.8.1/environment/vm/lima/lima.go)). Lima 1.0.5 sí selecciona el forwarder gRPC cuando ese entorno es false ([HostAgent v1.0.5](https://raw.githubusercontent.com/lima-vm/lima/v1.0.5/pkg/hostagent/hostagent.go)); la [documentación oficial](https://lima-vm.io/docs/config/port/) declara soporte desde Lima 1.0. Por ello se inició directamente la instancia Lima propia con esa opción soportada.

Comandos efectivos de recuperación, aplicados únicamente después de comprobar cero recursos y procesos de prueba propios:

```bash
/opt/homebrew/bin/colima stop --profile rio-kafka-e2e-01a0f8e0
LIMA_HOME=/Users/rjara/.colima/_lima LIMA_SSH_PORT_FORWARDER=false /opt/homebrew/bin/limactl start --tty=false colima-rio-kafka-e2e-01a0f8e0
/opt/homebrew/bin/docker context create colima-rio-kafka-e2e-01a0f8e0 --docker host=unix:///Users/rjara/.colima/rio-kafka-e2e-01a0f8e0/docker.sock
```

El contexto se recreó porque Colima stop retiró su metadata; Colima start con VM ya Running retornó `already running, ignoring`. El primer control Dockerinfo FAIL está preservado en grpc-runtime-first-failure.json. La recreación mantuvo el endpoint original y no activó el contexto. Para comandos Docker se utilizó siempre `--context colima-rio-kafka-e2e-01a0f8e0`.

Probe efectivo: mismo e2e/compose.yaml e imagen pinned, proyecto fresh rio-kafka-e2e-6eb2fcb44f5a4b25b90642c9557a388c, env privado grpc-probe.env. Up `--detach --wait --wait-timeout 120`, cinco requests Kafka ApiVersions v0 nativos desde host y teardown `down --volumes --remove-orphans`, con validación previa de labels y ausencia final. Los comandos exactos y resultados están en los receipts; no hubo topics de negocio, CP ni Gradle.

Pins conservados byte a byte: VZ/aarch64/4CPU/6GiB; colima.yaml SHA 5b75fd2dddff4103df7fd11d055094e6226a24bf8ce222fc3270d11351270c21 y lima.yaml SHA 6348d8e85ac680b90dc49de41840c1ca75de5744b501fe7e51ed187ca1b09235. Hostagent 41634 tiene env false observado. Docker 27.4.0, MemTotal 6198427648. Contexto activo sigue colima; no se modificaron shared runtime ni CP source. Ocho archivos del run fallido original quedaron sin drift.

El modo vive en el entorno del hostagent. Una futura llamada normal de Colima 0.8.1 para arrancar la VM volvería a forzar SSH; el wrapper reproducible, si root lo asigna, debe conservar este límite y validar mode/readiness. Este turno no escribió wrapper ni código CP. No se certifica repetibilidad por una sola corrida.
