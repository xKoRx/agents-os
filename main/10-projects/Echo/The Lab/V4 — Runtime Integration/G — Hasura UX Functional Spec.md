---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[F — Decision Register]]"
  - "[[F — SQL Migrations Ownership]]"
  - "[[D — Curves Metrics Workers]]"
  - "[[E — Rankings Shared Go Parity]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-22"
updated: "2026-10-22"
---

# G — Hasura UX Functional Spec

## Propósito

SPEC funcional definitiva para la entrada real de Strategy Lab, su detalle y su contrato Hasura/identidad. D21 gobierna la experiencia; D11 conserva composición estática y D24 fija una sola rama runtime. Este TARGET se implementa en Shot 2 y se audita en Shot 3; no acredita implementación, metadata aplicada, permisos efectivos ni aceptación GOD. Las autoridades de economía, cohorte y SQL son C/D/E/F; esta nota fija cómo se consultan y presentan sin otra fórmula en Vue o SQL.

## Contenido

### 1. CURRENT demostrado y superficies precisas

Corte único `xKoRx/echo`, `feature/ef-runtime-pools@2ee61791deb3139be23e1c9be3708b1d41da8d6b`, HEAD exacto y worktree limpio comprobados en lectura local. No se ejecutaron suites, builds, consultas remotas ni metadata apply.

| Evidencia del código en ese SHA | Consecuencia TARGET |
|---|---|
| `v3/front/src/router/index.js:25`; `views/LabView.vue:17,22,74`; `lens/lensRegistry.js:15–19` | CURRENT `/lab` abre StrategyLabClean y conserva cuatro tabs. Sustituir la entrada por un screener V4 y detalle, sin afirmar que los componentes del handoff antiguo existen aquí |
| `v3/front/src/services/graphql/client.js:13,35–39,139–150` | CURRENT admite admin secret HTTP y WS. El recorrido V4 y su bundle no pueden enviarla ni hornearla; usar bearer humano scoped |
| `v3/front/src/services/session_tokens.js:3,25,41` | Reutilizar sesión read/config por actor; el token no es un namespace ni identidad elegidos por el navegador |
| `v3/gateway/internal/server.go:126`; `hasura_auth_hook.go:10,24–31,40–44` | Hook real valida bearer y sólo retorna rol readonly/config_operator. Ampliar su mapping de identidad; no presumir tenant actual |
| `v3/hasura/metadata/tables/lab_curves_v3.yaml:8,14,37,65` | CURRENT readonly expone filtros vacíos. Metadata V4 aditiva exige filtro de namespace y owner de bundle, sin permisos de escritura |
| `v3/front/src/services/graphql/labExecutionScope.js:22–46` | Ranking de cuentas legacy no es ninguno de los dos rankings D20; no reutilizar fidelity_score como score de estrategia |

Los componentes históricos son referencias visuales/requisitos compatibles. No copiar ni fusionar ramas antiguas; implementar sobre este SHA y reutilizar sólo presentadores puros útiles del checkout vigente.

### 2. Identidad, roles y transporte

Conservar credenciales opacas del gateway y ETCD mediante SDK. Ampliar el mapping servidor de B a `credential -> principal_ref UUID, registry_namespace, role, permissions, allowed_profiles`; cada credencial resuelve exactamente un namespace. El hook `/api/v1/auth/hasura` retorna `X-Hasura-Role`, `X-Hasura-User-Id=principal_ref` y `X-Hasura-Registry-Namespace`, después de validar credencial y grant `lab:read`; role es exclusivamente lab_readonly o lab_config_operator según mapping servidor. No confiar headers `x-hasura-*` aportados por browser ni permitir que body/query cambie namespace. Un operador autorizado a otro namespace usa otra sesión/grant explícito; no se inventa un IdP nuevo. `lab_readonly` y `lab_config_operator` son roles NUEVOS y obtienen idéntica lectura V4; lab_config_operator sólo muta negocio vía Gateway y sus grants. Las credenciales LAB emiten exclusivamente estos roles allowlisted, sin heredar ni poder elegir readonly/config_operator legacy que mantienen filtros abiertos. No reutilizar bearer legacy sin mapping/grant V4 explícito; la sesión LAB solicita credencial scoped propia. Producer-ingest y runtime-ack no obtienen sesión humana por compartir bearer sintáctico.

Falta bearer/credencial inválida =>401; principal válido sin permiso=>403; auth mal configurada o mapping incompleto=>503 fail-closed. El hook nunca emite un rol V4 sin namespace/principal y no permite al cliente elegir un rol legacy. Missing sesión Hasura deniega la consulta; no filtro `{}` ni default global. Cada vista `lab.v4_*` tiene `registry_namespace = X-Hasura-Registry-Namespace`; read_bundles/screener_rows y sus hijos además tienen `owner_principal_ref = X-Hasura-User-Id`. Hijos económicos exponen namespace propio y se relacionan con bundle mediante FK scoped, no sólo UUID. Las vistas no exponen artifacts crudos, secretos, tablas de credenciales ni columnas internas de error. Lista de columnas explícita, límite por permiso de 201 filas, agregaciones sólo donde se especifican y siempre scoped. No INSERT/UPDATE/DELETE/actions mutation en lab.* para esos roles. Source Hasura V4 separado `echo_lab_v4` apunta a la MISMA DB con login leastpriv que sólo puede SELECT de views V4 allowlist; no duplica DB ni reutiliza login admin/sourcelegacy. Metadata aditiva preserva sourcelegacy sin exponerlo bajo roles nuevos. Crear credencial/aplicar sólo en harness propio en Shot2; ningún secreto real/deploy se realiza aquí.

HTTP y `connection_init.payload.headers.Authorization` WS usan el mismo bearer scoped. Eliminar `HASURA_ADMIN_SECRET` de cliente/config pública y cualquier fallback admin para esta aplicación; secreto de Hasura sólo en backend/runtime autorizado. Quitar tokens de control/config de variables VITE y no persistirlos en URL. Config pública sólo endpoints. Entrada de token read explícita en sesión, error accionable y logout limpia sesión/cache/bundles; no popup repetido por componente ni log del token. TLS fuera de harness loopback. No aplicar metadata ni reiniciar Hasura compartido en Shot 1.

### 3. Bundle de lectura y generación

F materializa `lab.read_bundles` y `read_bundle_rows` desde snapshot transaccional corto REPEATABLE READ; no hace cómputo económico dentro de él. Bundle `{read_bundle_ref, registry_namespace, owner_principal_ref, query_digest, sort_digest, created_at, catalog_revision, ranking_context_ref, ranking_snapshot_ref?, row_count, status}` y filas congeladas `{ordinal,strategy_ref,strategy_version_ref, resolution, target_ref?, generation_ref?, displayed_revision_vector_digest?, selection_revision?, ranking_membership_ref?, curve_result_ref?, metric_snapshot_ref?, ranking_input_generation_ref?, freshness_snapshot}`. `ordinal` se sella UNA vez tras ordenar todo el conjunto consultable; índice `(namespace,bundle_ref,ordinal)`. No ROW_NUMBER recalculado por página ni OFFSET de un head mutable. Un bundle no es nueva verdad económica y no muta su contenido cuando se publica otro derivado.

La curva visible fija bundle analítico default de cuatro perfiles D; sus puntos, contribuciones, operaciones, movimientos, calendario, distribución y métricas se leen sólo por ese `generation_ref` y vector de revisiones. Score/rank fija la cohorte E completa, con su propia curva/ventana de entrada; puede referenciar una generación anterior a la curva visible, y se etiqueta explícitamente como tal. No se finge que ambos snapshots son la misma generación ni se exige el mismo run/config entre estrategias. Cabecera muestra `display_curve_profile`, `ranking_algorithm`, `ranking_input_curve_profile`, ventana/cohorte, fecha de cálculo y estado de cada uno. Cambiar selector curve cambia columnas/gráfico/unidad, jamás renormaliza score; cambiar ranking cambia score/rank/explicación, jamás curva visible.

Detalle devuelve `head_revision_vector` separado de `displayed_revision_vector`, `desired_seq`, `generation_ref`, `is_stale` y motivos. Head N+1 aún pendiente conserva TODOS los valores explicativos de N, incluidos conteos y operaciones. Banner «Actualización pendiente: mostrando revisión publicada N; N+1 en cálculo». Al estar N+1 disponible se ofrece «Ver actualización»; el click reemplaza el bundle/detalle completo, conserva filtros y reinicia cursors. No swap automático en medio de una página/inspección. Sin publicación previa: identidad/readiness e historia visibles; zona analítica PENDING o insuficiente con razones, sin ceros inventados. Cursor viejo sigue leyendo su revisión retenida.

### 4. Contrato Hasura y Gateway de lectura

Nombres definitivos de vistas F: `lab.v4_read_bundles`, `v4_screener_rows`, `v4_curve_points`, `v4_operations`, `v4_movements`, `v4_daily_bins`, `v4_distribution_bins`, `v4_history_candidates`, `v4_copy_comparisons`, `v4_static_compositions`. Custom root fields Hasura `lab_v4_*`; custom column names conservan snake_case. Metadata del source `echo_lab_v4` en `v3/hasura/metadata/databases/echo_lab_v4.yaml` y allowlist de vistas en `metadata/tables/lab_v4_runtime.yaml`; query action en `metadata/actions.yaml` y tipos en `metadata/actions.graphql`, ensamblados por el builder de metadata V4 de I; el checkout actual no demuestra un root ensamblador completo. Las tablas fuente de F no son el API público por defecto.

`BundleService.Prepare(principal, query) -> ReadBundle`; `Page(principal,bundle_ref,cursor?,limit)->Page` y `Detail(principal,bundle_ref,strategy_ref)->DetailBundle` son los únicos servicios de consulta. Rutas públicas `POST /api/v2/lab/read-bundles` (lectura materializada, no mutación de negocio), `GET /api/v2/lab/read-bundles/{ref}/page` y `GET /api/v2/lab/read-bundles/{ref}/strategies/{strategy_ref}`. Prepare devuelve 200 y primera página; repetir query es válido y puede observar otro snapshot, mientras repetir con bundle_ref mantiene el original. Auth y límites aplican también a llamadas internas.

El producto obtiene el screener por query action síncrona Hasura `lab_v4_screener_page(input: LabV4PageInput!): LabV4Page!`, tipo `query`, nunca mutation. Input `{bundle_ref:String,cursor:String,limit:Int,query:LabV4ScreenerQuery}`: primera página exige query y bundle_ref/cursor nulos; siguientes exigen bundle_ref y query nula. Output `{read_bundle_ref,query_digest,ranking_snapshot_ref,row_count,rows,next_cursor,status,reasons}`. Handler `POST /internal/hasura/lab/screener-page` delega los mismos métodos Go; Hasura envía `X-Echo-Hasura-Service-Authorization: Bearer <service credential>` desde variable sólo servidor, `Authorization` humano reenviado en su header separado, y session_variables del hook; nunca sobrescribir bearer humano con el service credential. Handler valida ese actor, compara sesión con la identidad del bearer humano reenviado y rechaza headers/claims inyectados. Jamás aceptar `session_variables` de un cliente directo sin autenticar el servicio Hasura. Servicio interno no emite órdenes ni ejecuta mutaciones.

Cursor producto es base64url de payload canónico + HMAC-SHA256 Go, clave ETCD server-side con key_id y rotación conservando claves de cursors retenidos. Payload `{v:1,principal_ref,namespace,bundle_ref,target_ref?,generation_ref?,revision_vector_digest,query_digest,sort_digest,last_key}`; para screener `last_key=ordinal`, para operaciones `(opened_at,operation_ref)` y movimientos `(economic_at,batch_ref,seq,movement_ref)`. Verificar MAC antes de usar campos, tamaño≤4096, sin namespace de fallback. Base64 inválido/MAC inválido=>400 `CURSOR_INVALID`; scope o bundle ajeno=>404; cursor de otra query/sort/generación=>409 `CURSOR_CONTEXT_CONFLICT`. Limit default50, 1..200; leer limit+1 para has_more, sin count de operaciones completo por request. No cursor que salte al head si cambió publicación.

Las vistas GraphQL permiten además keyset nativo autorizado `(read_bundle_ref,ordinal)` y consultas detalle pinneadas; el ordinal raw no se presenta como cursor firmado de la API producto. Ejemplo query de detalle acotada:

```graphql
query LabCurve($ns: String!, $bundle: String!, $generation: String!, $after: bigint!, $limit: Int!) {
  lab_v4_curve_points(where: {registry_namespace: {_eq: $ns}, read_bundle_ref: {_eq: $bundle}, generation_ref: {_eq: $generation}, seq: {_gt: $after}}, order_by: [{seq: asc}], limit: $limit) {
    generation_ref curve_result_ref seq economic_at value_calc delta_calc drawdown_calc rounding_error_bound value_display12 numeric_policy_digest
  }
}
```

`$ns` sólo estrecha el filtro de sesión: cambiarlo nunca amplía acceso. El frontend no aporta namespace para autorizar y obtiene el valor visible del contexto de sesión. Los campos calc son strings decimales computacionales HE24 versionados y acotados por D/F; `rounding_error_bound`/policy identifican la precisión del derivado. Fuente económica permanece exacta38,18. Gráfica usa conversión sólo de display, y el detalle ofrece política/rango/frontera ambigua cuando afecta la interpretación; no expone instrucciones de ingeniería en el flujo. Puntos por rango/resolución máximo2000, respuesta marca `resolution` y `is_downsampled`; tabla/descarga exactas paginadas, jamás métricas recalculadas del muestreo. Gateway expone lectura de hijos `GET /api/v2/lab/read-bundles/{ref}/strategies/{strategy_ref}/{points|operations|daily|distribution|histories|copies}` y movements `.../operations/{operation_ref}/movements`, reutilizando repositorio scoped de las vistas. Todos exigen pin y las mismas semánticas; no segunda economía REST.

### 5. Screener de entrada real

`/lab` abre una grilla con una fila por StrategyRef canónico. No fixtures ni leaderboard de cuentas. Resolución `SELECTION` usa selección vigente sellada, `SINGLE` única historia candidata, `UNRESOLVED` conserva estrategia sin elegir entre alternativas y `NO_HISTORY` muestra registro sin datos. Versiones paralelas no duplican la estrategia: el usuario resuelve explícitamente versión/selección cuando no existe una única opción. `UNRESOLVED/NO_HISTORY` conservan nombre/identidad/readiness y métricas null con razones; no quedan ocultas por default.

Default: curve `r_net_cumulative.v1`, ranking `edge_duo.v1`, sort `rank ASC NULLS LAST,strategy_ref ASC`, page50. Selector de ranking incluye Edge Dúo y Forge Calidad 4; catálogo leído del registry, no copia de pesos en JS. Filtros server-side: búsqueda literal normalizada `q`≤128 caracteres sobre nombre/canonical ID; símbolo exacto (multiinstrumento aparece si cualquier operación del snapshot lo acredita); timeframe declarado por definición, source_kind, run_mode, reference_role, readiness, resolution, analytics_status, curva/perfil, ventana/período, cobertura, rango de métricas y score. `timeframe=null` se muestra «no declarado», nunca inferido del nombre/frecuencia. Buscar `q` usa escaping literal y debounce250ms, nueva query cancela petición anterior; sólo la respuesta cuyo query_digest coincide actualiza pantalla.

Columnas: nombre/StrategyRef, versión, símbolos, timeframe, fuente/modo, resolución, readiness, estado/frescura analítica, n_closed/n_open, net_change, return_fraction cuando aplique, PF, win_rate, expectancy, max/current DD, RetDD, Sharpe, SQN, score/rank. Cada valor incluye status/reason/unit; `UNDEFINED` se muestra «—» con razón, no 0. Retorno porcentual sólo con base positiva acreditada; R no se etiqueta dinero; 10k es capital virtual. Curve money multi-currency muestra NOT_COMPARABLE del scalar y drill-down por moneda, no suma global falsa.

Sorts allowlist `rank,score,name,symbol,timeframe,net_change,return_fraction,profit_factor,win_rate,expectancy,max_drawdown,ret_dd,sharpe,sqn,n_closed,updated_at` más `strategy_ref ASC` obligatorio. Unidad y profile/config fijados en bundle; no ordenar magnitudes incompatibles como si fueran la misma unidad. Valores no DEFINED/missing siempre NULLS LAST en ambas direcciones, tie por StrategyRef byte ASC. Columna con units incompatibles devuelve 422 `SORT_NOT_COMPARABLE` y conserva sort anterior; no mezcla USD/EUR/R. La fila numérica sin score sigue al final y es seleccionable. No descargar 20k filas para filtrar/ordenar en browser.

Filtros cosméticos reducen filas de la cohorte sellada sin recalcular extremos/score/rank. Se muestra `visibles/total cohorte`. Cambiar universo, input profile, ventana, sample/calendario o partition es un contexto de ranking nuevo mediante servicio de targets D/E, con estado PENDING; nunca «ranking de esta página». El formulario ofrece contextos registrados y creación explícita por operador, no evaluación dentro del SELECT. No scheduler, selección Top N automática ni rotación.

### 6. Detalle completo y estado navegable

Click fila abre `/lab/strategies/:strategyRef?bundle=<ref>`; deep-link sin bundle prepara uno scoped para esa estrategia y muestra el mismo detalle. Back conserva bundle, cursores y scroll de la lista. URL serializa `curve,ranking,context,from,to,asOf,knowledge,period,history,selection,sort,dir,q,sym,timeframe,source,runMode,status`; no bearer, writer libre ni cuenta usada como permiso. Query anterior `tab=strategyLabClean|strategyCurveV3|labV4|portfolios` normaliza al único Strategy Lab y se informa si un parámetro deja de ser aplicable. Mantener Account Lab fuera de la entrada de estrategia hasta inventario/cutover F, sin borrar consumidores ajenos por inferencia.

| Panel requerido | Datos y comportamiento definitivo |
|---|---|
| Identidad/estado | Strategy/Version/recipe, source/history/writer, run/binding/config y MM cuando hay, source vs representation operation ref al expandir; cuatro tiempos construction_at/cutoff/available_at/Echo-start con evidencia y UNKNOWN visibles. Acceptance, readiness y analytics separados; READY operacional no se deriva de un gráfico |
| Curva/métricas | Cuatro perfiles del registry; origen/config/unidad y banner balance realizado, sin afirmar equity flotante. Curva exacta de generación, downsampling etiquetado, tiles con formula/version/status/reason/ventana/sample/cost coverage; explicación de ranking independiente con componentes/extremos/cohorte y perfil de input |
| Drawdown | Área DD absoluto; % sólo perfil normalizado con peak>0; selector explícito `window_local`/`curve_running`, cambia target/spec calculada, no resta local en JS. Tiempo bajo máximo con tramo abierto censurado; sin marks no DD intrabar/equity |
| Calendario | UTC diario `utc_day_365.v1` por default, label zona y `[from,to)`. Bin COMPLETE sin actividad=0; GAP/OUTSIDE_COVERAGE=sin datos; nunca verde cero falso. Cada celda net_delta/unidad/n_terminal/n_movements/coverage y click filtra movimientos económicos de ese día del mismo pin. Cambio de calendario sólo a descriptor registrado y target calculado |
| Operaciones/movimientos | Tabla paginada por apertura+operation_ref, columnas estado/grano/open/close, qty/side/instrumento acreditados, Q_i/tag/evidencia, B_i y contribución del perfil, net/costos/exposición. Expandir lista movimientos parciales/costes con economic_at/known_at y refs orders/fills cuando existen. CLOSED_SUMMARY se muestra una vez, sin fills inventados; OPEN no cuenta como ganador terminal |
| Distribuciones | Histograma de contribuciones por ciclos terminales evaluables del perfil, no histogramar parciales como trades. Bins/bordes/counts y min/max/zero_count/n_excluded derivados servidor con policy digest; missing separado. Daily distribution distinta y etiquetada; ningún score recalculado por gráfico |
| Pre/post y ventana | Split por opened_at respecto construction_at probado, junto a corte as_of/knowledge y coverage. Money/time/Q desconocidos limitan sólo lo afectado; construction desconocido no inventa frontera desde import/cutoff. Mostrar duración/n y net/DD/PF/expectancy con deltas abs/relativos sólo donde definidos; relativo con base cero=>UNDEFINED. «Pre/post construcción» y «Forge/Echo» son ejes independientes |
| Historias/revisiones | Candidatas con cuenta/run/modo/rol/MM/grano/cobertura y revisiones retenidas. Principal y alternativas explícitas; segmentos `[from,to)` por opened_at con política anti-solape C, crosswalk SAME_ECONOMIC_FACT y errores visibles. Selección por CAS vía Echo, preview de cobertura; publicación anterior sigue legible mientras calcula. No suma automática de historias alternativas |
| Copias | Referencia exacta vs ejecuciones por broker y cuenta diferenciados; expected/executed/omitted/rejected/unmatched, qty/cobertura, VWAP y slippage sólo con links acreditados C. Sin enlaces=>INSUFFICIENT_LINK_EVIDENCE; diferencia de PnL/MM no se atribuye a slippage y sin fill no se fabrican latencias |
| Composición estática | Selección manual de miembros/versiones/historias fijadas, pesos iniciales Σw≤1, capital/riesgo y composition_start_at. Preview cash y C0_j; confirma por Echo CAS. Capital separado, flat start excluye ciclos previos completos; gráfico total+componentes/unidad virtual y exposición faltante. Peso positivo insuficiente propaga estado, no cash implícito. Etiqueta «análisis retrospectivo de composición», sin selección causal automática |

### 7. Mutaciones y estados de UX

Operador con grant puede `PUT /api/v2/lab/strategy-versions/{ref}/selection`, `POST /api/v2/lab/static-compositions`, `PUT /api/v2/lab/static-compositions/{ref}`, `POST /api/v2/lab/analysis-targets` para spec registrada y `POST /api/v2/lab/analysis-targets/{ref}/retry`. Son servicios Echo, Bearer config, Idempotency-Key y CAS body expected_revision/expected_digest para recursos existentes; If-Match es complementario opcional y, si aparece, debe coincidir con expected_digest; no UPDATE Hasura ni SQL desde front. Selección usa contrato C, composición C/D, target/retry D. Crear no implica live allocation. Retry no cambia inputs para eludir error permanente; después de timeout GET receipt por scope antes de repetir. 412 refresca estado para intención nueva, 409 idempotencia conserva key/payload y explica conflicto; no reenvío automático con CAS nuevo.

Estado de página `LOADING|READY|EMPTY|PARTIAL|ERROR|UNAUTHORIZED` separado de `resolution`, `economic_status`, `calculation_status` y `operational_state`. Skeleton inicial, estado vacío con filtros restablecibles; error 503 conserva snapshot previo claramente desactualizado y botón retry. WS sólo notifica desired/current refs de targets del namespace para mostrar actualización disponible; no stream masivo de operaciones/puntos. 401 requiere sesión; 403 acceso insuficiente; 404 objeto ausente/ajeno sin revelar existencia; 422 campo inválido; 429 respeta Retry-After; 5xx reintento con backoff acotado y cancelación. Nunca convertir error GraphQL parcial en tabla vacía ni mostrar éxito por HTTP200 con errors.

### 8. Acceptance funcional y capacidad — diseño, NOT_RUN

| ID | Gate verificable Shot 2/3 |
|---|---|
| G01 | Abrir sesión limpia `/lab` con estrategia auténtica aislada: fila→detalle sin fixtures productivos, source refs/StrategyVersion/readiness/analytics rastreables |
| G02 | Cambiar R→money→ambos10k cambia columnas/curva/unidades; score y cohorte permanecen idénticos. Cambiar Edge→Calidad cambia sólo ranking; explicación señala input10k aunque display R |
| G03 | Pin N, aceptar N+1 mientras tabla/movements abierta: todos los datos siguen N con banner; cursor anterior íntegro; adoptar publicación reemplaza todo por N+1, incluyendo n_closed/coverage |
| G04 | 20k estrategias, page50 y sorts allowlist/filtros aplicados antes de paginar: sin duplicados/saltos al recorrer bundle, null-last ambas direcciones, ties estables y ninguna descarga global JS; actualización concurrente no altera bundle |
| G05 | Dos namespaces y dos principals: HTTP/GraphQL/action/WS/direct child queries no cruzan scope; token producer/config sin grant no provisiona ni emite ACK; missing session failclosed; bundle/cursor ajeno404, MAC inválido400; build assets sin admin/control secrets |
| G06 | Calendario distingue COMPLETE0/GAP, pre/post no usa cutoff, DD local≠running, money/R sin % falso, distrib terminal no cuenta parciales, CLOSED_SUMMARY y costs no doble suman; detalle muestra unknown y razones |
| G07 | Copia con enlace exacto produce comparativa y denominador; copia summary/unmatched conserva rendimiento y muestra insuficiencia de slippage; no matching por hora/precio |
| G08 | Composición60/40 C0=10000=>6000/4000, flat start y cash residual; miembro faltante propaga insuficiencia; operación pre-start cierra después y no aporta. Sin I2 ni órdenes |
| G09 | Errores/cancelación/back/reload/deep-link/actualización WS conservan query y pin; timeout mutación recupera receipt sin duplicar; snapshot previo visible sólo con stale label |

SLO TARGET a medir, nunca PASS heredado: máquina/CPU/RAM/PG/Hasura/longitud de historias/concurrencia declaradas en H; catálogo20k con cuatro perfiles y ambos rankings, al menos10 lectores concurrentes, page50 warm p95≤500ms y cold≤2s durante corrección1% de estrategias; prepare bundle p95≤2s y respuesta screener≤1MiB. Primer detalle con≤2000 puntos p95≤1s y≤2MiB; 132805 operaciones en una historia se consultan paginadas, nunca inline. Browser mantiene≤200 filas/tabla y≤2000 puntos/gráfico. SQL EXPLAIN/rows/memoria/backlog y times por etapa en H; si no alcanza, corregir índices/bounded work dentro del scope, no reducir población ni presentar target como garantía. Catálogo20k no certifica20k instancias de trading.

## Fuentes

- [[F — Decision Register]] D09/D10/D11/D16–D24 y [[Echo — Producto Integrado]].
- [[A — Runtime CURRENT TARGET]], [[B — Forge Ingestion Readiness]], [[C — Histories Revisions Economy]], [[D — Curves Metrics Workers]], [[E — Rankings Shared Go Parity]], [[F — SQL Migrations Ownership]] y [[H — Test Matrix Independent Oracles]].
- [[THE_LAB_V4_Diseno_para_revision]], [[1 — TECHNICAL_FREEZE_PACKET]] y [[SHOT4_HANDOFF]] para requisitos compatibles; no segundo baseline.
- `xKoRx/echo@2ee61791deb3139be23e1c9be3708b1d41da8d6b`, archivos y líneas de §1.
