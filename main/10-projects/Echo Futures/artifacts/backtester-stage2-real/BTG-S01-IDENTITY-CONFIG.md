---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[BTG-PLAN]]"
  - "[[Echo Futures — D4-B3 S1 Exact Strategy]]"
  - "[[Echo Futures — D4-B2 Q13 Gerard Hardscalping MoneyManagement]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-05"
updated: "2026-10-05"
---

# BTG-S01-IDENTITY-CONFIG

## Propósito

Forensics ONE-SHOT de identidad y configuración para el histórico REAL solicitado como “Strategy Gerard”, sobre source certificado y configuración recuperable en instalación. Resultado de investigación listo para revisión del Primary Manager; sin aceptación Owner ni ejecución histórica.

## Contenido

### Estado y alcance de prueba

`STATE=BLOCKED_DECISION` para el run exacto: no hay autoridad recuperada que vincule “Strategy Gerard” con una Strategy ID/config/version específica. `IDENTITY=NOT_DEMONSTRATED`, `STRATEGY_CONFIG_DIGEST=NOT_AVAILABLE`, `MM_CONFIG_DIGEST=NOT_AVAILABLE`, `REAL_RUN=NOT_RUN`. Ausencia scoped demostrada en fuentes/canales inspeccionados; no se afirma inexistencia universal de una decisión en cualquier conversación o instalación.

Inspección terminada el 2026-10-06 UTC (2026-10-05 America/Santiago). Worker TOP / LOCAL / forensics, modelo reportado por mandato `gpt-6.1-sol`, superficie Codex. Bootstrap ejecutado una vez; routing Echo→Aranea, Environment Contract, technical-project-manager, MCP expert y runbooks ETCD/PostgreSQL leídos. Source read-only y pruebas explícitas offline; no trading, cambios de producto, AddOns, D6, bridge, egress, provider rules, cuentas o perfiles.

### Autoridades y provenance

| Evidencia | Ref exacta | Uso permitido |
| --- | --- | --- |
| Agents-OS base documental | `bb9fa98be22057e8468e83f72cb53fd147accc09` | Autoridades vigentes del vault; master intacto. |
| BTG paquete | `a16f4bb25cfb6882146f437f5913302a191313c2`; disponible también en base actual tras merge ajeno `d67319f` | Mandato de investigar antes de elegir S1/S2; no autorización de merge ni bypass. |
| Backtester certificado | Echo `cd451972b242c8933321e03001decd4b6d778c61`, limpio antes/después | Baseline de source/capacidad. |
| Echo master de continuidad | `372af59a7b83604781346613da01e3d510ea1360` | Referencia; también revisión física del Core DEV observado. |
| D6 | `d08a30ce9815f820fda7132e20dc42cc345eb8e8` | REFERENCE_ONLY; no se adopta su cuenta/Provider para BTG ni se modifica el carril. |
| D4-B3, D4-B2, BT-S01 con enmiendas y BT-S04 | Vault base indicada | ACCEPTED_INPUT para contratos/capacidades; no prueban el run Gerard pedido. |
| Generic20/GAU50, tests y viejo Prop Economics | Source/documentos | REFERENCE_ONLY; sin promoción a datos, importes o baseline económico real. |

### Identidad exacta: evidencia positiva y límite

1. D4-B3 S1 Exact Strategy, líneas 7–24, 361–367 y 440–444, define `S1_NY_ORB_30M_V1`: NQ, barras canónicas 5m, NY_OPEN 09:30–10:00 America/New_York, breakout por TRADE, technical_stop desde inicio premarket hasta última 5m cerrada. Premarket es NamedTradingWindow obligatorio, sin hora default. La nota dice que GerardMM posee la economía, no que Gerard sea alias de S1.
2. D4-B2 Q13, §24 (líneas 744 en adelante), permite S1 y S2 con el mismo GerardMM y exige que MM no branch-ee por strategy_id. Usar GerardMM no identifica cuál Strategy pidió el Owner.
3. Echo `cd451972`, `v3/sdk/futures/strategies/s1/s1.go:43`, posee SpecID `S1_NY_ORB_30M_V1`; líneas 113–133 definen sus parámetros. `v3/sdk/futures/config/snapshot.go:26–43` separa StrategyDef `id/module/stream_id/params`; módulos soportados `s1` y `s2`, validación en línea 195. `v3/backtester/compose.go:554–561` elige esos dos módulos. No hay módulo GerardStrategy en esta composición.
4. Búsqueda enfocada de `GerardStrategy|Strategy Gerard|strategy gerard|gerard_strategy|strategy_gerard` en source no-test V3 y specs no encontró una declaración de alias. Búsqueda del proyecto recuperó la advertencia BTG de no inferirlo, no una autoridad que la cierre.

**Conclusión:** S1 es candidata técnica identificable y GerardMM es una política identificable; la relación nominal “Gerard = S1” no está probada. No se inventó GerardStrategy ni se escogió S1/S2 por conveniencia.

### Importes y selectores GerardMM

| Stage/selector | Autoridad recuperada | Configuración de instalación | Interpretación |
| --- | --- | --- | --- |
| EVALUATION ordinal 1 | D4-B2:12, tabla §4, AC-Q13-01 | No snapshot instalado recuperado | SL USD 2.000 / TP USD 1.500 ya es decisión Owner; no volver a pedir esos importes. |
| EVALUATION ordinal 2 | D4-B2:12, tabla §4, AC-Q13-02 | No snapshot instalado recuperado | SL USD 2.000 / TP USD 1.500 ya es decisión Owner. |
| EVALUATION ordinal 3+ | D4-B2:72: matching exacto, fila requerida; sin heredar day2 | No fila runtime recuperada | Decisión/config de horizonte pendiente si se necesita nuevo riesgo después de day2; no defecto de MM. |
| FUNDED INITIAL / STEADY | D4-B2:74 y 825: schema listo e importes pendientes de futura configuración | No importes ni selector runtime recuperados | Nueva configuración económica requerida antes de riesgo funded; no bloquea una evaluación acotada. |
| Scaling adverse/favorable | D4-B2 §2/13/14: research/test seeds, LIVE/DEMO debe declararlos explícitos | No scaling vigente recuperado | No se copian 0.25R/2/1.0 ni 0.50R/1/0.5 como baseline real. |

`v3/sdk/futures/gerardmm/config.go:99–119` exige plan row set y rechaza LIVE sin scaling; `resolvePlan:125–145` resuelve ordinal o funded_mode exacto. `v3/sdk/futures/config/mm.go:28–44` construye el mismo Manager desde snapshot, sin default numérico. Scaling nil mantiene adds cerrados para modos que lo permiten; eso no constituye por sí mismo una autorización de baseline sin adds.

BT-S01 §10.1, líneas 426–438, permite materialización explícita de `FIXED_BUDGET_PER_ACCOUNT_DAY_V1`; Generic100K sólo fija initial_balance USD 100.000 y el caller aporta MM/RuleSet/fees/calendario/horizonte. La fixture de veinte días declara 2000/1500 en todos los días y adds deshabilitados como política del experimento. Esa extensión **existe**, pero es REFERENCE_ONLY para una configuración Gerard real. No se confundió “código soporta day3” con “Owner ya eligió day3”.

### Instalación inspeccionada

**Canal ETCD:** capability canónica `aranea-etcd-ro`, consumidor Codex real, consultas RO sin bypass directo. `etcd_list_keys /echo/development/`: 75 keys totales, 66 visibles, no truncado. `/echo/`: 113 totales, 99 visibles, no truncado; nombres secret filtrados por servidor. Ninguna key visible `futures/config_snapshot` ni `futures/enabled` en ningún prefijo Echo. GET exacto de `/echo/development/futures/config_snapshot` y `/echo/development/futures/enabled`: ambos `found:false`. No se leyeron valores de bridge/cuentas.

**Canal catálogo DEV:** `aranea-postgres-rw` usado sólo para SELECT; identidad observada `mcp_echo_dev_rw / echo-develop`, PostgreSQL 17.6. `echo.strategy_definitions` tiene 147 filas; cero matches de gerard, S1_NY_ORB o premarket_window en id/name/description/config. `echo.strategy_identity_mappings` tiene siete filas y cero matches gerard/S1_NY_ORB en canonical_strategy_id/strategy_ref. Cero tablas `echo` cuyo nombre contenga futures o gerard. No se descargó config ni manifest completo; no hay identidad Gerard recuperada en ese catálogo.

**Core DEV físico:** unidad `echo-core-dev` ACTIVE, MainPID 9763, `ENV=development`; binario real `/proc/PID/exe` Go 1.27.1, `vcs.revision=372af59a7b83604781346613da01e3d510ea1360`, `vcs.modified=false`, SHA256 `2044a537b108bb9f1c7af5850a6fd4282114ac4fd0f1480ba9defd488105cfd6`. El symlink de release termina en `2af4b21f9a06a8086f26fc54f229ebb12fba10b5`; no se usó ese nombre como identidad de source. `git ls-tree` sobre la revisión física devuelve cero paths para `v3/sdk/futures`, `v3/core/internal/futuresruntime` y `futuresvertical`. No hay base para atribuirle runtime Futures/Gerard canónico. No se hizo restart.

**Configuraciones locales:** búsqueda por filenames/configs seleccionados en workspaces D6 y la instalación DEV sólo recuperó configuraciones AddOn/transporte, test fixtures y Forge artifacts; no un snapshot técnico Gerard autorizado. AddOn de D6 no posee Strategy/MM según D6 design freeze §5/§6. Sus parámetros y la RuleSet GAU50 no se usan para llenar huecos BTG.

Límite: la inspección no descargó PROD completo, registros secretos, todos los artefactos históricos ni conversaciones arbitrarias. Puede existir otra fuente no presentada; la acción mínima alternativa es aportar su referencia exacta para recuperarla, en vez de pedir al Owner reconstruirla.

### Verificación independiente del histórico

Comando ejecutado desde Echo certificado, con namespace de red vacío y proceso fresco:

```sh
unshare --user --map-root-user --net go test ./v3/sdk/futures/gerardmm -run '^(TestEntry_EvaluationDay1AndDay2|TestEntry_UnconfiguredDay3FailsClosed|TestEntry_FundedUnresolvedFailsClosedAndConfiguredResolves|TestLiveRequiresExplicitScaling)$' -count=1 -v
```

Cuatro tests existentes PASS, package 0.007s. Son regresiones de contrato de configuración, **no smoke histórico**, no determinismo de dataset ni LIVE parity. No se crearon tests espejo ni se ejecutaron seeds/suites amplias. Worktree source permaneció limpio.

Evidencia local externa: Aranea workspace `work/btg-s01-identity-config/evidence/`. `config-probes.json` conserva respuestas RO y queries exactas; `source-digests.json` conserva paths repo-relativos y SHA256; `gerardmm-authority-tests.log` conserva los cuatro resultados. Archivos no secretos, fuera del vault.

| Archivo evidencia | SHA256 |
| --- | --- |
| config-probes.json | `e6e2e0750e5508e3ed3d0d4461769fb8ef19086ac6c9a6db6921c511362d6110` |
| source-digests.json | `f5449c12c621bd0fbdbfb6f1f587c0b4aaeb310d54545ed244e25f9521c1608f` |
| gerardmm-authority-tests.log | `d080dcb3c9570a3f7e3e84ceae16609c79b2729e7d984024cd18d5bbd17f010b` |

### Mínimo input que habilita el próximo paso

1. **Identidad:** autoridad exacta o confirmación Owner que vincule el nombre Gerard con `strategy_id + module/spec/version`. Si la intención era “S1 con GerardMM”, dejar esa relación explícita, sin alterar la señal.
2. **Config técnica baseline:** referencia a snapshot vigente o parámetros explícitos de la identidad seleccionada. Si es S1: NamedTradingWindow premarket con hora/timezone/calendario y los restantes S1 params (stream/tick/window/lookback) resolubles; scaling actual GerardMM explícito o decisión/config que declare adds deshabilitados. No hay que volver a decidir day1/2.
3. **Cobertura económica condicionada al horizonte:** para nuevo riesgo en ordinal 3+, filas o política declarada que lo cubra. Para funded, importes INITIAL/STEADY y selector/fase explícitos. Si el run termina en evaluación day1/2, funded y day3 no deben bloquearlo artificialmente.

Identidad ya elevada al Primary Manager antes del cierre. Dataset/provenance lo investiga el carril independiente: este artefacto no afirma que exista o falte un histórico suficiente. Mientras llega la decisión, se puede continuar inventario/conversión de datos y evidencia; ningún run aproximado se etiqueta “Gerard exacto”.

### Cierre ONE-SHOT y continuidad

Artefacto y registro de ejecución materializados mediante schema canónico en worktree documental propio `codex/btg-s01-identity-config`, fuera de vault main; log consolidado incluido. Sin modificaciones al reporte principal, BTG-PLAN, nota de proyecto, master ni sync. El Primary Manager importa/revisa contenido conservando provenance; el worker no adjudica aceptación.

Session-close ejecutado por mandato ONE-SHOT: delta de continuidad queda en este artefacto; sin L0/L1 por falta de transcript raw exportable ni beneficio adicional, sin checkpoint duplicado, sin L3 nuevo. `SESSION_FEEDBACK=NONE`, `REUSABLE_BEHAVIOR_CANDIDATES=NONE`, `PRO_CHAT_POOL_DELTA=0` (Codex, no Chat Pro). Cierre ejecutable completado; no certificación del run.

## Fuentes

- [[Echo Futures]], [[BTG-PLAN]], [[BTG-S01-SUBMANAGER-PROMPT]].
- [[Echo Futures — D4-B3 S1 Exact Strategy]], [[Echo Futures — D4-B2 Q13 Gerard Hardscalping MoneyManagement]].
- [[Echo Futures — BT-S01 Backtester V1 Design]] y [[Echo Futures — BT-S04 Final Remediation and Certification]].
- Echo source `cd451972b242c8933321e03001decd4b6d778c61`, paths/líneas declarados y digests externos. D4-B3 SHA256 `bb33a230e24ac49756459627f3c3e5cb49160d7285f2026b0d83b4e20cb190f8`; D4-B2 `ba93c230af4a573c05efab32b430143395ab929688108b629bd72172cd21aa29`; BT-S01 `b6e8021f40b9d40dbb69e6a8d07051f4f7bbe17ece70a08b9c8165a22d06ed57`; BT-S04 `f4ee5a04db1f85e220be5ee71b97b99aee390586980b9d29060d145dea4cdc9a`.
- [[Echo + Echo Forge — Environment Contract]], [[aranea-mcps-expert]], [[aranea-etcd-mcp]], [[aranea-postgres-mcp]]; probes reales descritos, no documentación usada como prueba física.
