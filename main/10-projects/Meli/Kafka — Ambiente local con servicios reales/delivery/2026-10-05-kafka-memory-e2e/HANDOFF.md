# Kafka CP local con mapa — corte 2026-10-05

**Cambio implementado y revisado; E2E físico BLOCKED, objetivo incompleto.** El owner reemplazó Fury Sandbox por un mapa en memoria y priorizó CP Kafka; ecosistema después. No hace falta login Fury, VPN, alias KVS ni provisión Sandbox para el comando local. Producción conserva su cliente remoto.

## Fuente y entregables

| Repo | Rama / commit | Base y worktree |
|---|---|---|
| Kafka CP implementación | `feature/kafka-e2e-memory@7615b210e5b70667912b956c2f27cc0d1ebc80eb` | Base `7f1720d950446638ff9b15a0e4e167f3e8e26e43` |
| Kafka CP HEAD, suplemento sólo docs | `4c66d0d5ca77e1de4aef5b08c9e601921eb60a9b` | `/Users/rjara/fuentes/rio-controlplane-kafka-memory-e2e` |
| Knowledge library | `docs/kafka-e2e-memory@0feee7b5fad32c8c7dc3dcc252d65166b15c0cd9` | Base `5c4cb45d9fa8c3e4a95d73542ecd58c04c7c1530`; `/Users/rjara/fuentes/ads-signals-knowledge-library-kafka-memory-e2e` |

Los dos nuevos worktrees y los anteriores están limpios; refs en `worktrees.json`. Sin push/PR/release. Master CP canónico auditado el01/10: `f74e856ef3de881e2d504c6cb1ced573681c1058`; memoria es trabajo pendiente, no producción. SPEC funcional→técnica→tareas: delta `LOCAL-MEMORY-1` en `meli/features/20261001-real-e2e/`, copiado en `source/`. `patches/` contiene deltas aplicables a esas bases; replay desde clones nuevos produjo árboles idénticos a ambos HEADs (`evidence/patch-replay.json`), verificación de importación únicamente.

Arquitectura: reutiliza sourceSet/fixtures Gradle del CP, task `localKafkaE2eTest` y perfil `local,real-e2e,memory-e2e`; conserva controllers, validadores, processors, provisioners y guard. Cinco brokers pinned cubren RF AWS1–5/GCP1–3/default2; resultados y triggers sobre Kafka real. `LocalInMemoryKvsClient` implementa la interfaz nativa con ConcurrentHashMap por instancia y un monitor CRUD/close, create exclusivo, versiones locales, CAS, TTL, copias de bytes y errores explícitos. Reinicio pierde estado; JVMs no comparten claims.

## Ejecutar

Desde el worktree CP, con Docker propio operativo≥5GiB, JDK25 y puertos39092–39096 libres:

```sh
DOCKER_CONTEXT=<contexto-propio-operativo> JAVA_HOME=<jdk25> ./e2e/local.sh
# O con dependencias internas ya cacheadas:
DOCKER_CONTEXT=<contexto-propio-operativo> JAVA_HOME=<jdk25> ./e2e/local.sh --offline
```

`./e2e/run.sh` sin argumentos delega al mismo comando. Startup/test/teardown automatizados; reportes en `build/local-e2e/<run>/`. Faltantes, selección vacía, fallos/skips, falta de prueba nativa o cleanup incierto retornan nonzero. UNKNOWN o trabajo retenido conserva recursos propios; no borrar journals para forzar PASS. Comandos remotos mantienen requisitos propios. Selección exacta en [LOCAL.md](/Users/rjara/fuentes/rio-controlplane-kafka-memory-e2e/e2e/LOCAL.md).

## Evidencia y estado

| Capa / capacidad | Estado | Evidencia y límites |
|---|---|---|
| Adapter/config/guard | PASS59 |17+14+28 unitarios; `evidence/domain/`; no servidor KVS ni Kafka |
| CP unitarios + compilación | PASS845 | Revisor distinto, clon limpio inicial detached7615,65clases/0fallos/0errores/0skips; `evidence/independent-clean-clone/`.33fuentes sin drift; Swagger generado en clon propio/diff conservado |
| Controles launcher/verificador | PASS49 | `evidence/independent-controls/launcher-v5/`; tipos/owner/tuple/proof, ausencia nativa, retención, entry. V1–V4 REDs conservados; fuente/metadata/proceso únicamente |
| Primera corrida física | FAIL | `evidence/physical-attempt-48711a6c/`:343invocaciones/309fallos/34PASS/0skip. Brokers internos5healthy/5IDs; host39092refused, primer fixture timeout. Ninguna familia completa PASS; receipt V1 intacto |
| Kafka físico final y reproducción independiente | BLOCKED | Colima propio forwarding SIGKILL exit-9, causa desconocida. `evidence/runtime/`; sin fix causal verificado. VM propia detenida, compartido2GiB intacto |
| Matriz capacidad→escenario→evidencia |5PASS unit/config,226BLOCKED,125NOT_EXECUTED |356filas en `source/meli/features/20261001-real-e2e/local-coverage-matrix.tsv`; matriz remota351 intacta. No sumar capas como éxito E2E |
| Knowledge validadores | Estructural/histórico PASS; formal FAIL937 baseline |691IDs/194Markdown; formal byte-idéntico SHA268be6f39a764e42569d5deafe535299f01bc5be000245779e9bd2e18bb9cdf5,0nuevos. `evidence/knowledge/` |
| Knowledge/doc revisión independiente | PASS documental |5docsKL+2docsCP consistentes con fuentes/recibos,0findings; `evidence/independent-documentation/` |
| CI local | NOT_EXECUTED | `.github/workflows/local-kafka-e2e.yml` existe; falta job real en runner elegido con Docker/JDK25/Maven interno |
| Ecosistema/OAuth/BigQueue/Toolkit remoto/recovery durable | NOT_EXECUTED en esta familia | No se certifican por memoria o Kafka plaintext; fase posterior explícita |

Tres assertions enum/string en `RealKvsIntegrationTest` se corrigieron a `ErrorCode.CONFLICT.getCode()` sin modificar oráculos create/CAS; replay pendiente. V1 eliminó recursos propios tras el fallo; revisión encontró falsos verdes de proof/UNKNOWN. El código final retiene ante UNKNOWN y exige prueba nativa exacta; no transformar aquel receipt FAIL en PASS.

## Siguiente gate concreto

1. Restaurar Docker propio≥5GiB con host loopback39092–39096 funcional. El launcher final valida los cinco listeners con deadline30s. SIGKILL confirmado; no atribuir causa a permisos, VPN, auth o AMFI sin evidencia.
2. Ejecutar toda la suite local, verificar efectos/resultados/mapa/cleanup y repetir. Revisor distinto debe reproducir desde checkout limpio la ruta completa y fallas críticas Kafka/publicación/proceso.
3. Elegir y ejecutar runner CI local; publicar branch/PR según workflow autorizado. Adjuntar evidencia real por capacidad y actualizar matriz.

El paquete conserva JUnit saneado, IDs, receipts y hashes; raw logs permanecen privados en /private/tmp. Tokens/coste desconocidos: no expuestos por plataforma. AGENTS OS sigue activo/parcial; objetivo E2E incompleto, sin cierre.
