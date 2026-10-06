---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[BTG-PLAN]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-05"
updated: "2026-10-06"
---

# BTG-S01-REAL-GERARD-RESULT

## Propósito

Conseguir el baseline histórico REAL de la Strategy Gerard exacta y GerardMM compartido, corregir defectos demostrados y entregar evidencia al Primary Manager para revisión. El submanager conserva continuidad; no acepta el gate Owner ni inicia S02.

## Contenido

### Estado observado

STATE = BLOCKED_DECISION
SECONDARY_STATE = BLOCKED_EXTERNAL
REAL_SMOKE = NOT_RUN
LONGITUDINAL_RUN = NOT_RUN
DETERMINISTIC_RERUN = NOT_RUN
ECONOMIC_STAGE_COVERAGE = NOT_DEMONSTRATED
SIGNALS / OPERATIONS / FILLS / ACCOUNT_PNL = NOT_MEASURED

El inventario previo del Primary es preparación documental; no acredita datos físicos ni una corrida. S00–S04 son ACCEPTED_INPUT para capacidades; D6, Generic20/GAU50 y simuladores previos son REFERENCE_ONLY. Otros runs permanecen UNREVIEWED.

### Autoridad recuperada y aislamiento

El paquete solicitado procede de `xKoRx/agents-os`, commit de rama documental `a16f4bb25cfb6882146f437f5913302a191313c2`, segundo padre del merge existente `d67319f0878610c786b94aa2ad31e5e4503e7efa`. La rama remota ya no aparece en `ls-remote`; su contenido existe en el checkout vigente. Esta sesión no ejecutó ni exigió el merge, ni alteró master. Evidencia nueva en rama `codex/btg-s01-evidence`; especialistas con ramas documentales propias y ownership disjunto. Sin intervención D6 ni cambios de infraestructura.

HEADs refrescados directamente por `git ls-remote` al inicio (2026-10-06 UTC, fecha local 2026-10-05):

| Autoridad | HEAD observado | Estado local |
| --- | --- | --- |
| Agents-OS master | `bb9fa98be22057e8468e83f72cb53fd147accc09` | limpio |
| Echo master | `372af59a7b83604781346613da01e3d510ea1360` | referencia remota |
| Backtester certificado | `cd451972b242c8933321e03001decd4b6d778c61` | worktree certificado limpio |
| D6 | `d08a30ce9815f820fda7132e20dc42cc345eb8e8` | referencia remota; intocado |

### Delegaciones y revisión

- TOP LOCAL `gpt-6.1-sol`, ONE-SHOT: autoridad/configuración inspeccionada; [[BTG-S01-IDENTITY-CONFIG]] en commit `08b79f27bb0b951af3a305f49a3201dfce6823ca`. Root comprobó los 11 digests de fuentes y los tres digests de evidencia externa: cero mismatches. Cuatro tests existentes PASS offline; cierre/run/log completados, feedback NONE.
- NORMAL LOCAL `gpt-6-luna`, ONE-SHOT: [[BTG-S01-DATASET-INVENTORY]] cerrado en commit `9bc160a8b7466c5dd399711bc35e8fc9242b5d8f`. Revisión root corrigió la afirmación inicial sobre inexistencia de Downloads/Documents; el barrido corregido no halló candidatos. El nombre de capability MinIO RW no se trató como prohibición automática de sus métodos RO; metadata de 12 buckets inspeccionada sin mutaciones. Cierre/feedback completados; run-register skipped por lookup/documentación. Root reparó sólo el delimiter de cierre del frontmatter del feedback importado; su digest de contenido cambia, no sus observaciones.
- TOP LOCAL `gpt-6.1-sol`, ONE-SHOT: [[BTG-S01-NINJATRADER-ACQUISITION]] cerrado en commit `1adec4f09f9b12e91aab0a20d76589a76928f659`. Exportador oficial identificado; corpus NOT_ACQUIRED. Sin repetir probes denegadas ni alterar D6. Cierre/log completados; feedback NONE y run-register skipped por lookup/documentación.

El harness expone ambos modelos. No expone una ejecución CLOUD Pro autónoma; las delegaciones presentes requieren inspección física LOCAL. Consumo confirmado Chat Pro = 0 (Codex). Cada worker ejecutó su cierre ONE-SHOT y persistencia por delta; registro sólo donde hubo pruebas de código. Root no se autocierra.

### Fuente del histórico — steering Owner

El Owner confirmó durante el inventario: “la idea es sacar todo desde ninjatrader”. NinjaTrader pasa a ser la fuente seleccionada para adquisición, sin presumir que ya existe un export durable. El inventario continúa sólo por rutas de lectura/extracción autorizadas de esa fuente; no se solicita otro proveedor ni se captura el feed D6 para reemplazar el histórico. El permiso de lectura del archivo/carpeta o una exportación fuera del carril operativo siguen sin demostrarse.

### Bloqueos evidenciados

| ID / clase | Expected | Actual / evidencia | First divergence / owner / mínima acción |
| --- | --- | --- | --- |
| BTG-B01 / BLOCKED_DECISION | Vínculo canónico entre el nombre Owner Gerard y Strategy/version/config | Source registra S1/S2; ambas usan GerardMM. Ni decisiones seleccionadas ni instalación DEV inspeccionada demuestran cuál es Gerard. PG DEV: 147 strategy_definitions y 7 mappings, cero matches relevantes; ETCD DEV: futures/config_snapshot y futures/enabled ausentes. | Antes de NewRun; Owner/Primary define o aporta autoridad exacta, sin elegir por nombre. |
| BTG-B02 / CONFIG_AUTHORITY_GAP | Config MM real y contexto account/provider para el horizonte | D4 sí define EVALUATION account-days 1–2 SL USD 2.000 / TP USD 1.500. Rows posteriores y FUNDED encontradas sólo como fixtures/modeling; no configuración Owner vigente. | Preflight/config, ningún historical run. Recuperar configuración concreta o definir etapa autorizada; no completar valores por inferencia. |
| BTG-B03 / BLOCKED_EXTERNAL | Corpus físico real con provenance, contratos, orden, timezone y digests | Workspaces históricos seleccionados contienen Polymarket/MLB. Evidencia de feed vivo no acredita corpus multiday. Candidato NinjaTrader no listado: permiso OS denegado bajo perfil RO; ruta/stock quedan no resueltos, no declarados inexistentes. | Antes de DatasetSource; aportar ubicación del export existente o acceso RO a esa fuente. No comprar ni tocar el feed/runtime. |

No se registran findings de software BT2-Fxx cerrados: ninguna corrida histórica real ocurrió y no se observó una primera divergencia histórica. Los bloqueos anteriores son de autoridad/configuración/datos; no fueron maquillados como defectos corregidos ni como ausencia global.

### Evidencia independiente obtenida

El worker TOP observó Core DEV binario source `372af59a`, `vcs.modified=false`; ese commit no contiene `v3/sdk/futures`, `futuresruntime` ni `futuresvertical`. El symlink de release no prueba el source del proceso vivo. No se desplegó otro Core: el mandato es offline y esa instalación no acredita Gerard Futures vigente.

Cuatro tests existentes GerardMM pasaron bajo namespace sin red externa: day1/2, day3 sin resolver, FUNDED ausente/configurado y scaling explícito. Sirven como evidencia de fail-closed y capacidades compartidas; REAL_SMOKE sigue NOT_RUN. Config instalada y fixtures permanecen separados. Logs completos y comandos en [[BTG-S01-IDENTITY-CONFIG]].

Originales y producto no modificados; no hubo suite amplia, seeds, trading, runtime restart ni configuración de infraestructura. El aislamiento `unshare --user --map-root-user --net` funciona. Toolchain observado Go 1.27.1 linux/amd64; no claim de determinismo entre builds.

### No interferencia D6

D6 refrescado desde remoto y worktree limpio: `d08a30ce`. Base común con S04 `7fbd7e990ac6628df3e4cc2717e96efd83bfbbf6`; commits exclusivos D6 desde esa base afectan sólo `v3/futures-bridge/` (adapter, AddOn y harnesses). Ningún delta exclusivo D6 en SDK/Core. Esta sesión no cambia producto ni interviene D6, y no infiere estado físico intacto por el tree Git: sólo realizó observación autorizada.

### Adquisición NinjaTrader verificada como mecanismo, no como corpus

El especialista TOP confirmó un mecanismo GUI oficial `Tools → Historical Data → Export` para generar TXT UTC por contrato/intervalo/data type desde datos disponibles. Falta validar cobertura del caché y original exportado. El harness no expone GUI nativa NinjaTrader; SSH autorizado no lee la carpeta fuente. La mera existencia del exportador no satisface adquisición ni fidelidad. Detalle oficial, formato, límites y acción mínima en [[BTG-S01-NINJATRADER-ACQUISITION]].

Acción física mínima: exportar desde la GUI la caché existente `Tick / Last` por contratos físicos, y `Bid / Ask` sólo si están disponibles, conservando TXT y registro de opciones sin editar. Recuperar esos archivos desde un stage accesible o adjunto; el submanager comprobará cobertura y provenance antes de convertir. No descargar, reconectar ni cambiar Merge Policy en la instancia D6 activa. Si la caché no alcanza, adquisición posterior requiere un contexto NinjaTrader independiente autorizado y entitlement real; no se afirmó que exista.

BBO es un gap técnico condicionado al corpus: el NDJSON actual asigna a ambos lados un único timestamp/ref; combinar exports Bid/Ask independientes como QUOTE simultánea alteraría age lateral. La representación derivada debe conservar timestamps/refs por lado detrás del DatasetSource existente. Se registró compatibilidad pendiente, sin implementar adapter ni cerrar un finding de run no ejecutado. TRADE_MODEL también necesita costos/offsets explícitos; no se seleccionó por inferencia.

### Continuidad y próximo paso

Pregunta de identidad sigue pendiente Owner en la superficie LOCAL. La pregunta de fuente fue respondida: NinjaTrader; su acceso/extracción sigue pendiente de resolver con permisos existentes o acción mínima indispensable. La falta de respuesta no autoriza una Strategy aproximada ni un corpus sintético. Primary Manager revisa estos bloqueos y recupera/define sólo los inputs faltantes; con esa autoridad, este mismo submanager continúa el slice real, remediación y longitudinal dentro de S01. S01 no está aceptado ni cerrado; S02 no inició.

REUSABLE_BEHAVIOR_CANDIDATES = NONE adjudicado por root en esta fase; candidatos/fricción propios de workers quedan en sus artefactos, sin editar skills generales.

### Persistencia y verificación documental

Evidencia consolidada en `xKoRx/agents-os`, rama `codex/btg-s01-evidence`, base `bb9fa98`. Importación por contenido de archivos seleccionados; sin merges, rebases ni cherry-picks preventivos. Root comprobó digests de entrada y fuentes del worker TOP. Guards S04 conservados; ninguna modificación a sync o policy/skills generales.

Refresh antes del handoff: Echo master `372af59a`, S04 `cd451972`, D6 `d08a30ce`, source/D6 trees limpios. Agents-OS master avanzó a `a326c237d6a2fdfd6fc9367da927da40328df33b`; diff desde base no afecta Echo Futures ni Agents-OS/skills relevantes. No se integró ese delta ajeno. Documentación nueva y plan con lint dirigido sin findings; nota de proyecto mantiene cinco errores de lint preexistentes (dos tags y tres secciones), idénticos al baseline, sin ampliación.

ROOT_AGENT_RUN = SKIPPED: coordinación, revisión de evidencia y documentación; el único segmento de tests de producto atribuible está registrado por el worker TOP. ROOT_SESSION_CLOSE = NOT_REQUESTED.

### Handoff compacto

```text
SUBTASK = BTG-S01
STATE = BLOCKED_DECISION; SECONDARY = BLOCKED_EXTERNAL
BASELINE_SHA = cd451972b242c8933321e03001decd4b6d778c61
DATASET = NINJATRADER_SELECTED; CORPUS_NOT_ACQUIRED; MANIFEST/DIGEST_NOT_AVAILABLE
GERARD_STRATEGY_AUTHORITY = EXACT_ALIAS_AND_CONFIG_NOT_DEMONSTRATED
GERARD_MM_AUTHORITY = D4-B2 + shared gerardmm; day1/2 SL2000/TP1500; runtime config NOT_RECOVERED
REAL_SMOKE = NOT_RUN
LONGITUDINAL_RUN = NOT_RUN
DETERMINISTIC_RERUN = NOT_RUN
ECONOMIC_STAGE_COVERAGE = NONE_DEMONSTRATED
SIGNALS / OPERATIONS / FILLS / ACCOUNT_PNL = NOT_MEASURED
OPEN_MATERIAL_FINDINGS = NO_REAL_RUN_FINDINGS_ADJUDICATED; BLOCKERS_B01_B02_B03_OPEN
ARTIFACT = BTG-S01-REAL-GERARD-RESULT + identity/config + dataset inventory + NT acquisition
AGENTS_OS_COMMIT = final consolidated commit supplied in chat/PR handoff
GAPS_FOR_S02 = identity/config + historical corpus + horizon rows/stages + economic units/rules/fees/settlement
NEXT_PRIMARY_MANAGER_ACTION = resolve exact Gerard identity/config; Owner NT cache export; same S01 continues offline after input verification
OWNER_ACCEPTANCE = NOT_ADJUDICATED
SUBMANAGER_SESSION = OPEN
PRO_CHAT_POOL_DELTA = 0
```

### Gaps para S02

Pendientes de inventario, sin inferencias económicas nuevas: unidad de `5k / 120k`; programa/prop/fees/settlement; stage config vigente; cuatro retiros netos cobrados y reinversión; preservar una cuenta operando a la vez salvo fuente posterior. S02 no iniciado.

## Fuentes

- [[BTG-PLAN]] y [[BTG-S01-SUBMANAGER-PROMPT]], commit de origen identificado arriba.
- [[Echo Futures]], autoridades master vigentes.
- [[Echo Futures — BT-S01 Backtester V1 Design]], enmiendas frozen.
- [[Echo Futures — BT-S04 Final Remediation and Certification]].
- [[Echo + Echo Forge — Environment Contract]], bootstrap y technical-project-manager.
