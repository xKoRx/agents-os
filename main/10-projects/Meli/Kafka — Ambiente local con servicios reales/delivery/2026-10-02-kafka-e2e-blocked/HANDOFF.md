# Entrega E2E Kafka — checkpoint bloqueado, 2026-10-02

**Veredicto: BLOCKED. El encargo completo no está terminado.** Hay código, escenarios, launchers, CI y documentación revisados en cinco checkouts aislados y commits locales. Faltan ejecución de negocio con KVS real, ambos Playmaker, proveedores administrados y job CI; la reproducción independiente de una ruta completa también sigue pendiente.

El [índice de entrega](delivery-index.json) fija bases, ramas, HEAD completos, parches y SHA256. Los originales se conservaron con sus modificaciones; su [estado final de sólo lectura](original-workspace-final-state.json) está registrado. No se hizo push, PR, release ni despliegue. Todo cambio nuevo sigue **WORK_BRANCH_PENDING**, separado del master canónico y de develop.

## Implementación y decisión

Se eligieron source sets Gradle en el CP y una extensión aislada del harness local de Playmaker. Así los contratos y pruebas siguen el mismo commit del CP, se reutiliza la orquestación RIO con MySQL y se separan unitarios, funcional local y proveedor administrado. Un repositorio E2E adicional duplicaría coordinación de versiones y clients; mezclar estas dependencias con unitarios impediría aislar los gates corporativos. La [SPEC técnica](</Users/rjara/fuentes/rio-controlplane-kafka-e2e/meli/features/20261001-real-e2e/2-technical/spec.md>) contiene alternativas y fundamentos.

Se implementaron Kafka KRaft de cinco brokers con imagen fijada y ajuste SVE sólo para ARM, routing por corrida, CP real, Toolkit productivo con mapeos Sandbox exclusivos, resultados observables sobre Kafka, ambos perfiles de Playmaker con MySQL, clientes Entity/Tiger/ACME reales, fallas de red/procesos propios, journals durables, ownership y teardown condicionado a ausencia comprobada. La incertidumbre produce fallo y retención; no autoriza borrar recursos. Kafka local no certifica OAuth ni BigQueue. Los cuerpos administrados existentes fallan antes de ejecutar cuando faltan contratos/recursos reales.

Hay regresiones y correcciones acotadas del CP para schema/metadata inválida antes de dispatch; el SDK conserva el ProducerBuilder configurado. La corrección SDK no está publicada ni adoptada por el artifact CP1.3.1. Las diferencias de autorización entre master Playmaker y develop se preservan; se prepararon escenarios separados. No se presentan como políticas productivas nuevas.

| Repositorio/checkpoint | Base | HEAD local | Rama |
|---|---|---|---|
| Kafka CP | develop `4302481c` | `3bea4809` | `feature/kafka-real-e2e` |
| Playmaker candidato | develop `7673f4bf` | `acbda2f1` | `feature/kafka-real-e2e` |
| Playmaker overlay canónico | master `0c83575c` | `47df54fe` | `feature/kafka-real-e2e-canonical` |
| SDK events | master `ad2c98b8` | `97146e9f` | `feature/kafka-e2e-publisher-fix` |
| Knowledge library | master `de7cde85` | `65bcbb97` | `docs/kafka-real-e2e` |

La evidencia canónica usa el [snapshot de referencias GitHub fechado](evidence/final-github-canonical-ref-receipt.json): CP master f74e856e, Playmaker master0c83575c, SDK ad2c98b8 y biblioteca de7cde85. Un refresh posterior fue rechazado por allowlist IP HTTP403. Es evidencia de esos commits; no confirma qué está desplegado ni representa un refresh vigente exitoso.

## Cobertura y validación observada

La [matriz versionada](evidence/coverage-matrix.tsv) tiene **351 capacidades, 22 columnas**, SHA256 `2f0d813088fe8b6d2e88a8c39bc5d850edebc2a860bc0d3dbd34040111b2c50e`: 304 FULL preparadas, 29 PARTIAL y 18 NONE. **351/351 están NOT_EXECUTED en su contrato físico completo.** FULL significa preparación revisada, no éxito runtime. Las [brechas restantes](evidence/remaining-gaps.md) separan siete ramas defensivas sin estímulo físico conocido, once fronteras SDK/proveedor y tres joins nuevos parciales.

| Capa | Resultado | Alcance comprobado |
|---|---|---|
| CP unitarios + jar | PASS: 822 tests, 0 fallos/errores/skips | Reglas aisladas y compilación; no KVS Sandbox |
| Playmaker candidato unitarios | PASS: 4384/4386; 2 skips baseline | Los dos skips históricos no acreditan suites E2E |
| SDK unitarios | PASS: 708, 0 skips | Regresión RED→GREEN del builder, sin delivery administrada |
| Tres familias reales | PASS de compilación | 48/42/16 clases y bootJar; cuerpos de negocio sin ejecutar |
| Kafka físico ARM | PASS | Cinco brokers, RF1–5/ISR/readiness y limpieza propia |
| MySQL/controles físicos | PASS limitado | 37 migraciones, ACL/proxies y limpieza de componentes propios |
| Revisión independiente | PASS de scopes concretos | Regresiones limpias, guardian/PID/lease, journals, controles de task/worker; no ruta completa |
| Parches desde bases limpias | PASS 5/5 | apply/check y árbol exacto al HEAD; clones retirados, refs originales intactas |
| CI sin inputs obligatorios | FAIL esperado | Intentó cuatro gates; cada uno status2, agregado1; no skips ni verde falso |
| Knowledge estructural/histórico/diff | PASS | 691 IDs /194 Markdown; 17 documentos corregidos |
| Knowledge formal | FAIL baseline | 937 errores, mismos bytes que baseline, 0 introducidos/retirados |
| Negocio CP/KVS/Playmaker y managed | BLOCKED / NOT_EXECUTED | Sin contratos físicos completos certificados |
| Job CI y revisión formal Meli | BLOCKED / NOT_EXECUTED | Sin ejecución ni aprobación |

Se conservaron los REDs, fallas de compilación y carreras de drivers previas. Los ajustes corrigieron código/control de espera; no cambiaron outcomes para aprobar defectos. El [ledger](evidence/verification-ledger.json) contiene 95 registros. La [revisión independiente de portabilidad](evidence/patch-portability/review.json) conserva los cinco checks limpios. El [freeze final](evidence/root-final-source-freeze.json) ata 29 paths, SHA256 `23409c2bc593f8373a419255e4c00b08747f8d01f2499a95e17755795f50b0b1`, verificados sin drift; los [peers finales](evidence/root-v4-1-r2-peer.json), [documentales](evidence/root-final-docs-peer.json) y [de validadores KL](evidence/kl-final-integrated-validator-peer.json) delimitan su alcance.

## Bloqueos y acción necesaria

1. **KVS:** Fury autenticado e inventario devolvieron200; dos BCs propios se crearon200, pero clone del servicio CP `triggers-status-nonprod` devolvió403. Se retiraron con delete200/ausencia404. Habilitar clone a la identidad actual para un alias KVS propio de Kafka CP, o suministrar otro alias propio clonable; confirmar además los dos aliases distintos propios de Playmaker para results/locks. Después ejecutar el Toolkit real: creación exclusiva, versión inicial del servidor, CAS válido/obsoleto, incremento y TTL. No hubo claves ni instancias KVS creadas en este ensayo.
2. **Entity/Tiger/ACME/Odin:** proporcionar target no productivo propio de EntityService, deployment/runtime/identity metadata verificable y grants de team/project, caller permitido y caller genuinamente denegado. `scopes` produjo ZeroTrustUnauthorizedException y deployments400; no equivalen a ausencia de servicio. El import APPROVED requiere contrato y actors/recipients autorizados de Odin, sin mensajes externos enviados en esta sesión.
3. **Managed:** cluster/credenciales OAuth GCP propios con principal permitido/denegado; endpoint MSK compatible con el transporte vigente; topics/consumers/callback BigQueue propios con schema, ventana completa, retry/DLQ/ACK y cleanup observable. Templates200 y CLI mock no certifican esos recursos. No se pausó un consumer compartido. Resolver publicación/adopción autorizada del SDK corregido antes de certificar segment/buffering.
4. **CI:** identificar runner protegido con Docker/JDK25, red corporativa/Maven/Fury y Environment autorizado. Configurar los inputs, variables y seis secretos del workflow; ejecutar realmente el job con los dos SHAs Playmaker revisados. Un archivo workflow no es evidencia de ejecución.
5. **Workflow formal:** renovar Spellbook privadamente si es requerido y autorizar expresamente destinos/acción de Zord. Auto-review rechazó enviar el diff privado a Claude/Anthropic y Codex/OpenAI y actualizar su cursor persistente sin autorización explícita. La skill exige: “Si Zord estándar no puede correr, bloquear cualquier revisión Meli” ([SKILL.md](</Users/rjara/obsidian/SecondBrain/main/80-agents/skills/signals-code-review/SKILL.md:66>)). Peers locales no sustituyen esa aprobación.

## Reproducción y limpieza

Desde `/Users/rjara/fuentes/rio-controlplane-kafka-e2e`, usar JDK25 y Docker propio. Los comandos y schemas completos están en [e2e/README.md](</Users/rjara/fuentes/rio-controlplane-kafka-e2e/e2e/README.md>). Configs privados reales y vigentes son obligatorios, no fixtures para fingir permisos.

```sh
export JAVA_HOME=/Users/rjara/Library/Java/JavaVirtualMachines/corretto-25.0.4/Contents/Home
export DOCKER_CONTEXT=colima-rio-kafka-e2e-01a0f8e0
./gradlew --no-daemon test validateRealE2eHarness compileRealIntegrationTestJava compileE2eTestJava compileManagedIntegrationTestJava bootJar
python3 e2e/check-kafka.py
```

Una vez concedido clone y confirmados los aliases propios, `e2e/sandbox.py up` crea el Sandbox por corrida y genera el archivo privado. `verify` exige configuración fresca; `down` sólo puede ejecutarse tras reconciliar ownership/ausencia y workers. Los nombres de comandos efectivos son:

```sh
"$E2E_FURY_PYTHON" e2e/sandbox.py up --cp-service "$E2E_CP_KVS_SERVICE" --pm-results-service "$E2E_PM_RESULTS_KVS_SERVICE" --pm-locks-service "$E2E_PM_LOCKS_KVS_SERVICE"
E2E_KVS_ENV_FILE=/absolute/private/cp-sandbox.env ./e2e/run.sh realIntegrationTest
E2E_KVS_ENV_FILE=/absolute/private/canonical-sandbox.env ./e2e/run.sh e2eCanonicalPlaymakerTest
E2E_KVS_ENV_FILE=/absolute/private/candidate-sandbox.env ./e2e/run.sh e2eCandidatePlaymakerTest
./e2e/managed.sh all
./e2e/ci.sh
"$E2E_FURY_PYTHON" e2e/sandbox.py down --directory /absolute/private/verified-own-run
```

Los tres Sandboxes/runs locales son distintos. PM requiere seleccionar los dos checkouts, caller y recibos Entity/denied correspondientes a cada run; managed conserva sus recibos físicos propios. Las rutas `/absolute/private/...` son inputs a suministrar, no artefactos creados exitosamente. El launcher automatiza inicio/test/teardown; incertidumbre conserva recursos y journals y termina con fallo. No borrar marcadores ni ejecutar down manualmente sobre recursos retenidos sin reconciliación. La última [inspección Docker propia](evidence/final-owned-docker-inventory-2026-10-02.json) tenía cero contenedores/volúmenes y sólo redes builtin; no se cambió el contexto Docker compartido.

## Continuidad

Al resolver gates: verificar permisos y contratos físicos → provisionar sólo recursos propios → ejecutar CP completa → ambos Playmaker → managed → CI → repetición independiente desde checkout limpio y casos críticos de falla → mapa por capacidad con run/efecto/evento/KVS/estado PM/cleanup → validadores y revisión formal → actualizar knowledge con evidencia de rama hasta integración canónica. No saltar escenarios ni bajar expectativas.

La sesión AGENTS OS permanece activa porque el objetivo sigue incompleto; proyecto y agent_run registran este checkpoint y el siguiente paso. Token usage y coste: **desconocidos**, la plataforma no expone métricas atribuibles.
