---
type: session
schema_version: 1
scope: session
created: "2026-10-19"
updated: "2026-10-19"
area: "[[Echo]]"
project: "[[Echo Futures — Runtime Pools]]"
application:
entities:
  - "[[Echo Futures — Runtime Pools]]"
related:
  - "[[Echo + Echo Forge — Environment Contract]]"
  - "[[2026-10-19-zcode-glm53-echo-runtime-pools-resume03-typename-fix]]"
aliases: []
confidence: high
source_session: ZCode (GLM-5.3-Flash, submanager CERT-NT-01 RESUME-03, mandato GPT-6 Primary Manager)
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/session
  - scope/session
---

# 2026-10-19-cert-nt-01-resume03-summary

> [!info]+ Session summary L1
> Resumen operativo. Para beta queda fuera del corpus normal de Graphify.

## Objetivo

- Ejecutar RESUME-03 de CERT-NT-01: el mandato autoriza IMPLEMENTACIÓN CORRECTIVA local (no otra inspección) — resolver el P1 del typename de `marketJsonType`, publicar release corregida, restaurar el procesamiento Futures en DEV sin romper FX y retomar la certificación Ninja/Sim101 donde las precondiciones lo permitan. SUBMANAGER LOCAL + especialistas A→B→C secuenciales.

## Contexto cargado

- Bootstrap Agents-OS (cold start), entidad [[Echo Futures — Runtime Pools]]: ledger CERT-NT-01 (RESUME-01/02), checklist, handoffs previos. El Owner adjuntó el contenido del `echo-execution-addon.json` (token enmascarado) — primera confirmación del CONTENIDO.

## Trabajo realizado

- **Gramática pinneada del runtime real:** clase `TypeName` extraída del jar del contenedor StateFun 3.2.0 en .75 (md5 `9a7bf01c…`, copia durable `/root/cert-nt-01-evidence/`) + source verbatim `release-3.2.0` (`parseFrom`: split `/`, 2 partes exactas, empties trailing recortados). Corregida en vuelo una transcripción del submanager (fila trailing-slash) gracias al hallazgo de A.
- **Preflight:** feed reanudado SOLO a las 22:00Z (pausa ordinaria NQ 16:00 CT — la parada de 21:00Z NO fue avería; QUOTE event_ts <2 s verificado); anomalía nueva: actor externo borró `futures/enabled`+`config_snapshot` a las 22:31Z (rev 61252) → re-provisión byte-exacto 22:39Z con el helper A6 (snapshot validado con el parser del release). Gotcha nuevo: el gateway ETCD .250:2379 devuelve vacío en range key-only (usar range_end) — explicación alternativa a lecturas «fuzzy» pasadas.
- **A (fix):** `marketJsonType` → `"echo.types/"+name`; 21 call sites (descubrió 2 en strategy_engine); regresión permanente con mirror exacto + caminata por reflexión; rojo 21/0 → verde 4/4; 257 PASS + baseline exacta. SHA `c37d1351`.
- **B (verificación):** VERIFIED V1–V7; inventario 0 inválidos restantes; rojo replicado en clone scratch; checkpoint-safe (estados futures frescos, cero migración, FX preservado).
- **C (release/deploy):** push FF (master intacto), release por SHA desplegada, module verbatim → **demostración en vivo: 10 estados registrados y ~375K mensajes frescos consumidos sin ninguna excepción de typename**. Defecto NUEVO: 3× `RequestTimeoutException` netty→core bajo burst → rollback de module íntegro a PRE (28/28 estable, FX lag 0). Core c37d1351 permanece.
- **JSON AddOn:** contenido confirmado NO CONFORME (binding ejecución RJARA…551 real + mercado a 9771) → armado prohibido; corrección exacta entregada al Owner (Sim101, multi-binding, ntx_port 9770).

## Artifacts creados o modificados

- Producto: `xKoRx/echo@feature/ef-runtime-pools` `b13ef43d→c37d1351` (2 commits pusheados FF, master intacto); release DEV `~/opt/echo-dev/releases/c37d1351…` (core desplegado; module PRE).
- [[Echo Futures — Runtime Pools]]: sección RESUME-03, gates C2/C3, estado final, bitácora; `OWNER-CHECKLIST-CERT-NT-01.md` (feed resuelto, typename cerrado, nuevo bloqueo timeout, JSON no conforme + corrección exacta).
- Durable: `~/aranea/work/cert-nt-01-{a,b,c-resume3,mgr}/RESUME03-*` (handoffs A/B/C, gramática, JSON, runbook C).

## Memoria propuesta o creada

- Continuidad en memoria de proyecto (RESUME-03): typename cerrado con evidencia de producción; siguiente despacho = timeout de transporte + arming con JSON Sim101.

## Decisiones

- No armar: el JSON vincula una cuenta comercial real (prohibición /frozen) y la estabilidad de C2 quedó detenida por el defecto nuevo de transporte; ningún remedio fuera de scope.
- Backlog (~1,36M histórico): NO consumido por diseño declarado del release (`startupPosition: latest`); alternativas (surgery del module / replay 21,8M) rechazadas y documentadas; decisión del Manager.

## Pendiente

- (1) Análisis/corrección del timeout transporte (call-timeout/capacidad worker 2048 MB / `statefun.async.max-per-task=8` o remedio de producto) + re-aplicación del verbatim; (2) Owner: JSON corregido Sim101 + reinicio NT; (3) arming SIM acotado y C3/C4. UNKNOWN V8 (hash del .cs instalado) opcional. Fuera de certificación: decidir quién borró ETCD 22:31Z (auditoría de actores DEV).
