---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related: ["[[Echo — Producto Integrado]]", "[[F — Decision Register]]"]
aliases: []
tags:
  - kind/doc
created: "2026-10-22"
updated: "2026-10-22"
---

# 0 — Shot 1 Gate and Baseline

## Propósito

Paquete ejecutable de diseño de `THE_LAB_V4_RUNTIME_FORGE_INTEGRATION`, dentro de Echo / The Lab. Owner KoR; padre [[Echo — Producto Integrado]]. Exactamente cuatro shots: diseño GOD, implementación GLM, auditoría independiente GOD, correcciones/certificación GLM con revisión final dentro del cuarto shot. Este documento gobierna el gate del Shot 1 actual, sin reabrir decisiones ratificadas ni continuar el Shot 4 histórico.

## Contenido

**Estado de trabajo: DESIGN_IN_PROGRESS; dictamen GOD aún no emitido.** Ocho especialistas Sol ONE-SHOT con contextos frescos, ownership documental disjunto y código de sólo lectura. GOD realiza despacho y revisión crítica; no implementa producto ni ejecuta suites masivas.

### Baseline verificado al despacho — 2026-10-22

| Superficie | Evidencia actual | Ownership / permisos efectivos |
|---|---|---|
| `xKoRx/echo`, `feature/ef-runtime-pools` | `git ls-remote` devuelve `2ee61791deb3139be23e1c9be3708b1d41da8d6b`; checkout `fefb-s03-close-20261022/echo` bajo workspace externo Aranea coincide, limpio | `kor`, UID/GID 1000, checkout `kor:kor`, modo 777; únicamente lectura de source autorizada en este shot; el modo del FS no concede ownership operacional |
| `xKoRx/symphony`, `master` | Remoto y checkout limpio `daded14cbe0bc85f6fafda8d079e94036f715b47` | `kor:kor`, modo 775; lectura de contratos Forge/ranking; sin tocar campañas, workers o configuración |
| `xKoRx/agents-os`, `master` | Corte inicial `aa108af602321e030fceddff145f7d6e0d32897a`, limpio; remoto origin correcto | Vault `kor:kor`, modo 775; escritura documental y commit/push directo a master autorizados; no branches/PRs/force-push |
| Infraestructura Echo / Forge | No accedida ni certificada en este shot | No se asume ownership de bases, runtime, colas, flota, cuentas u órdenes; producto SOURCE no demuestra deployment |

La rama Echo se fija al SHA para investigación reproducible; D24 prohíbe usar ramas antiguas como baseline, compararlas o trasplantar implementación. El código histórico no es evidencia de compatibilidad. `sync.sh` y `.sync/` quedan fuera del alcance.

### Autoridades

D09/D10/D11/D16 y D17–D24 de [[F — Decision Register]] prevalecen; D24 resuelve toda instrucción histórica incompatible. Se consultaron [[0 — Submanager State]], [[SHOT4_HANDOFF]], [[THE_LAB_V4_Diseno_para_revision]] y `V4 — Shot 2/1 — TECHNICAL_FREEZE_PACKET.md` para requisitos compatibles, no para heredar implementación ni certificados. El contrato ambiental [[Echo + Echo Forge — Environment Contract]] fija Echo DEV/PROD y Forge operacional único, con aislamiento por recursos; no autoriza intervención física por sí mismo.

### Propiedad de entregables

A runtime/autoridad y CURRENT→TARGET; B ingesta/readiness; C historias/economía; D curvas/métricas/workers; E rankings/paridad; F SQL/migraciones; G Hasura/UX y consolidación funcional/paquete Shot 2; H matriz QA/oráculos. Los especialistas no editan estado padre ni change_log. El gate final y las correcciones materiales del paquete pertenecen a GOD.

### Adjudicaciones de revisión crítica

- Un único hash nuevo `wire.HashTagged`/`wire.Digest` del SDK; se descarta la receta de longitudes propuesta inicialmente en A. Los IDs nativos existentes no cambian.
- Vocabulario público `run_id`, `config_revision`, `execution_mode`, rol `REFERENCE|EXECUTION|NATIVE` y `reference_basis` separado. El `operation_ref` fuente A se guarda en `source_operation_id`/`correlation.source_operation_ref` de C; la ref de History representa ese hecho bajo una historia y no crea otra autoridad.
- Decoder V2 cerrado, sin claves duplicadas/desconocidas; decimales canónicos rechazados si no cumplen. Digest y ID opaco son tipos distintos. Receipt replay se resuelve antes de CAS; precondición stale devuelve 412, ausencia 428, conflicto de identidad/idempotencia 409.
- Readiness externa OBSERVE_MASTER no fabrica Operation/Signal nativos. Native sólo acredita snapshot realmente cargado; incompatibilidad requiere arranque aislado propio y estado explícito, sin hot reload inventado ni reinicio compartido.
- Fuente exacta, derivados `derived-fixed24-half-even.v1` con B/deltas cuantizados24, sumas exactas y cota de error; descarta fracciones compuestas expandidas por crecimiento de memoria. Métricas HE24; único kernel MinMaxV1 binary64 compatible con Forge, conversión declarada en el borde. Submódulo puro `v3/shared-analytics` dentro de Echo, ningún repositorio adicional ni segundo kernel decimal; `sdk/analytics` existente importa SDK y no puede ser raíz del módulo puro.
- Cohorte exige misma semántica comparable; run/config/selection individuales viven en membership, no se exige compartir un run físico entre estrategias. Se publica el conjunto completo atómicamente.
- Migraciones nuevas 067–074 adjudicadas a F sobre catálogo real 066; sin copiar numeración/DDL de ramas antiguas. Runner mínimo con transacción y checksum de bytes externos; no auto-hash circular. Retiro destructivo y migración de estrategias quedan fuera.

## Fuentes

Fuentes primarias: repositorios y SHAs de la tabla; mandato Owner del 2026-10-22; notas canónicas citadas. Los documentos de especialistas incorporarán rutas y líneas verificadas en ese único corte. No hay certificación E2E, de seguridad dinámica ni de infraestructura por completar este diseño.
