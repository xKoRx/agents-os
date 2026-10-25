---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related: ["[[Echo Futures — Runtime Pools]]", "[[EF-PROD-GIMPL-MANAGER-REVIEW-20261024]]", "[[EF-PROD-B3-GI-CLOSURE-EVIDENCE]]", "[[EF-PROD-GLM-01-EVIDENCE-INDEX]]", "[[EF-PROD-GOD-05-MANAGER-ADJUDICATION]]"]
aliases: []
tags:
  - kind/doc
created: "2026-10-25"
updated: "2026-10-25"
---

## Propósito

Evidencia del cierre GI-2 del dictamen «Re-review del Primary Manager» 2026-10-24 ([[EF-PROD-GIMPL-MANAGER-REVIEW-20261024]]): GI-REC-P0 (restore real obligatorio en el arranque compuesto), GI-REC-P0b (identidad física del topic Kafka), GI-RDY-P1 (frescura efectiva con expiración y último guard) y GI-QA-EVIDENCE (cobertura diff-aware del código añadido/modificado), con verificador C adversarial independiente sobre el SHA final. Documento de evidencia del Submanager GLM-5.3-Flash LOCAL; NO constituye aceptación G-IMPL (ese dictamen es del Manager), ni certificación física, ni autorización de despliegue.

## Contenido

Estado entregado, cadena de SHAs, cierre por hallazgo, L3 real, coberturas honestas, verificación independiente, residuales y límites.

# EF-PROD PRD.4 — GI-2 CONTINUITY CLOSURE (2026-10-25)

## Estado entregado

**STATUS: GIMPL_READY_FOR_MANAGER_REVIEW** — FINAL SHA **`0e17c4d3f1179cde709f923c8dd28e8cd853afc9` REMOTE_VERIFIED** (push FF `9daa57cb..0e17c4d3` sin force sobre `xKoRx/echo feature/ef-runtime-pools`; `origin` re-leído en `0e17c4d3`). Verificador C adversarial read-only sobre el SHA integrado: **READY_FOR_MANAGER_REVIEW** (ítems 1-7 PASS con disclosables MINOR; cero MATERIAL). La brecha de cobertura vs el piso GOD-03 ≥95% (ver §Cobertura) queda publicada sin maquillaje como hallazgo para la adjudicación del Manager. Sin deploy, sin merge a master, sin tocar DEV/PROD compartidos, Ninja físico, cuentas, The Lab ni Forge; laboratorio estrictamente loopback.

## Cadena de SHAs (delta `9daa57cb..0e17c4d3`, 54 archivos, ~5.4k inserciones)

| Etapa | SHA | Contenido |
|---|---|---|
| BASE (re-review Manager) | `9daa57cb` | HEAD remoto confirmado; worktrees A/B creados desde aquí |
| A1 GI-REC-P0b | `5ffa2192` | `TopicOffset.TopicID` (KIP-516) + `ConsumerGroup` aditivos; chequeos estrictos MISMATCH/UNAVAILABLE/UNVERIFIED; sarama `1.43.3→1.44.0` (mínimo que expone `Uuid`; negociación Metadata v10 `sarama.V3_0_0_0`) |
| A2 GI-REC-P0 | `b22e337a` | El gate escribe `<storage-root>/master-restore-args`; compose (develop+production) consume `-s/--fromSavepoint <copia independiente> --job-id <manifest job>` vía el entrypoint OFICIAL `/docker-entry-point.sh` (con guión — la divergencia exacta del addendum; verificado contra flink-statefun-docker `3.2.0-java11` y `StatefulFunctionsClusterConfigurationParserFactory` release-3.2.0; `-n/--allowNonRestoredState` NUNCA se pasa) |
| A3 GI-REC-P0 | `fb39c636` | Attestation con lectores REALES: `latest.restored` REST con igualdad estricta id+path, `SaramaGroupOffsets` committed ≥ manifest por partición, protocolo job↔control firmado por nonce, oráculo EXTERNAL aditivo, single-job check (`FlinkJobsLister`) |
| A4 contrato | `c1dd6883` | Protocolo attest como contrato sdk público (`attest_protocol.go`: `SignAttestReport`/`AttestRequest`/`AttestReport.Verify`) + CLI `seal` (certifica el checkpoint que el PROPIO Flink reporta `latest.completed`, copia `_metadata` a storage independiente, sella offsets/identidad/roster, instala `ActiveManifestRef` por CAS) + CLI `bootstrap-token` |
| A5 tests | `2f19ab98` | `TestAttestCompetitorJobBlocked` + `FlinkJobsLister` como capability aditiva |
| B1..B5 GI-RDY-P1 + QA | `bcc217a3`,`a0681aef`,`bf69c6b0`,`446597cc`,`6cdd52c7` | Contrato `FreshnessDoc` central (schema intacto + campos aditivos `produced_at/max_age_ms/streams[]`); productor REAL en echo-core (espejo de los veredictos servidos del market engine por `echo.futures.market-stream-state.v1`; `evaluated_at` = veredicto espejado MÁS VIEJO; sin evidencia nueva NO publica; sin segundo cálculo económico); expiración `FRESHNESS_DOC_EXPIRED` en `readMarketFreshness` (defaults 30/60/5 intactos); último guard en `permit.Checker.Admit` (solo expansión, después del permit, código aditivo 5003 `MARKET_FRESHNESS_NOT_FRESH`; manage-only pasa); `efprod-diff-coverage.sh` (métrica separada, original intacto) |
| Integración | `40fad3a5` | Merge FF de `wrk-gi2/restore` + merge no-FF de `wrk-gi2/fresh` (ramas divergentes de la base; ownership disjunto verificado: intersección de archivos vacía; rationale «gate FF repair» como en el ciclo GI-01..04) |
| Wiring integrador | `0e17c4d3` | Seam GI-REC-P0 residual de A: `echo/recovery_attestor` registrado en `cmd/echo-core` (`recovery_attestor_wiring.go`) → `futuresruntime.ServeAttestRequest` → egress `echo/futures-recovery-attest-report-egress` (exactly-once); bootstrap namespace attesta nada (CLI BLOCKED, honesto); tests propios (`TestAttestorDeliver*`, `TestRegisterRecoveryAttestor*`) |

## Cierre por hallazgo del addendum

| Hallazgo | Estado | Cierre (source + física) |
|---|---|---|
| GI-REC-P0 (restore no obligatorio en el arranque compuesto) | CERRADO + L3 | El ÚNICO camino de boot es `gate && args-file && exec /docker-entry-point.sh $args`: RESTORE ⇒ args nativos `--fromSavepoint`+`--job-id` pineado (el job restaurado lleva EXACTAMENTE el JobID certificado); BOOTSTRAP ⇒ archivo vacío (token single-use por CAS; jamás bootstrap implícito); BLOCKED ⇒ exit 1 + args stale borrados; fs read-only ⇒ exit≠0 (no hay boot sin imposición). Cero segundos submitters (`HTTPFlinkRest.Submit` sigue observation-only). Attest exige: job RUNNING == manifest, UN solo job del deployment, `latest.restored` == manifest checkpoint (igualdad estricta de path), committed de consumer group ≥ offset manifest por partición dentro de la ventana viva, y reporte de owners firmado por nonce (roster real de markers C-REC-3 + ValueSpecs persistidos). `gate exit 0` NUNCA es prueba de restore. |
| GI-REC-P0b (identidad Kafka incompleta) | CERRADO + L3 | `TopicOffset.TopicID` físico (uuid KIP-516 leído por metadata v10; uuid cero ⇒ `TOPIC_IDENTITY_UNAVAILABLE` ⇒ BLOCKED) + `ConsumerGroup`; gate y attest re-verifican: identidad viva ≠ manifest ⇒ `TOPIC_IDENTITY_MISMATCH`; manifest legacy sin identidad ⇒ `TOPIC_IDENTITY_UNVERIFIED` ⇒ BLOCKED (ausencia de evidencia ⇒ bloqueo, nunca éxito por offsets compatibles). Aditivo: `schema_version` congelado intacto, manifests viejos siguen válidos como documentos. |
| GI-RDY-P1 (frescura sin fuente ni expiración) | CERRADO | Productor REAL = espejo de la autoridad existente (`echo/market_stream` ya evaluaba FRESH/STALE/UNKNOWN con bounds 30/60/5); echo-core publica el doc a ETCD `futures/market/freshness` al cadencio del watchdog; silencio degrada (el veredicto STALE del engine baja el doc; sin evidencia nueva `evaluated_at` envejece); reader expira (`FRESHNESS_DOC_EXPIRED` ⇒ known-pero-BLOCKED, no UNKNOWN silencioso); `NewRiskEligible` cae sola; ÚLTIMO guard físico en `permit.Checker.Admit` rechaza expansión bajo STALE/UNKNOWN/expirado/ausente con causa tipada y código 5003, inmediatamente antes del send; cancel/reduce/manage-only pasan; permit vigente NO sustituye mercado fresco (orden permit→freshness sin bypass). Defaults 30/60/5 intactos; cero segundo cálculo económico en Bridge. |
| GI-QA-EVIDENCE (cobertura sólo de archivos nuevos) | CERRADO COMO MÉTODO, brecha visible | `efprod-diff-coverage.sh` NUEVO (ejecutable separado; el original intacto): denominador = bloques que intersectan rangos añadidos por `git diff -U0` en archivos Go preexistentes modificados vs `ac0621a1`; numerador = bloques cubiertos por la batería completa (101 paquetes, mismos skips declarados); publica numerador/denominador global y por archivo, perfiles y comandos; exit 1 <95%; exit 2 en fresh si un archivo del denominador queda sin observación (fallo de método, nunca exclusión silenciosa). C# declarado sin instrumentación equivalente. La batería fresh sobre el SHA final reveló el alcance verdadero (ver §Cobertura). |

## Prueba L3 real (laboratorio `/tmp/ef-gi2-lab`, loopback estricto)

etcd :12379 · Kafka 3.7.1 KRaft :28092 · Flink 1.14.3 + StateFun 3.2.0 JAR real vía `unshare -rm` bind-mounts · kills SOLO por PID registrado (cero `pkill -f`) · cero topics/processos fuera de localhost. Corrida FINAL con binario `echo-runtime-control` RECONSTRUIDO del árbol integrado (sha256 `ec0e41aa…`, HEAD `0e17c4d3` verificado, árbol limpio). Evidencia cruda: `A-L3-RESTORE.md` + `A-L3-FINAL.md` (workspace `~/aranea/work/ef-prod-gimpl-20261025/evidence/`), crudo `/tmp/ef-gi2-lab/logs/run-l3-FINAL.out`.

| Escenario | Resultado |
|---|---|
| S1.p0 bootstrap autorizado (token single-use; args file VACÍO) | PASS — job RUNNING |
| S1.p1 feed 1..20 + checkpoint externo + `seal` (topic id `jP4TkC61Q2OVkjlfF-PXjQ`, grupo, offsets {0:20}) | PASS |
| S1.p2 kill JM+TM por PID → gate RESTORE → boot con `--fromSavepoint chk-2/_metadata --job-id <certificado>` → job RUNNING id PINNADO == certificado; `latest.restored` desde la copia independiente | PASS |
| S1.p3 feed 21..30 + duplicado seq=20 → `attest` **CLEAN** (restored-from + committed 31≥20 + reporte firmado) + egress 1..30 monótono sin huecos, dedup del duplicado | PASS |
| S2 checkpoint incompatible (`chk-999`) | PASS — attest BLOCKED («restored checkpoint 3 != manifest chk-999») |
| S3 topic recreado (mismo nombre+particiones, id nuevo `HXlifxfoSKGV4kkpKOZgNA` ≠ manifest) | PASS — gate BLOCKED `TOPIC_IDENTITY_MISMATCH` |
| S4 job competidor | PASS-UNIT+RUTA-CERRADA — detección `TestAttestCompetitorJobBlocked` PASS en el SHA; el dist del lab no trae handlers de submission (`POST /jobs`, `/jars/upload` ⇒ «Not found», `web-submit:false`), el log crudo conserva honestamente «attest exit=0 (expected 1)» |
| S5 restore omitido (defecto original: master sin args) | PASS — attest BLOCKED («attested job … is not running (state absent)») |
| S6 `allowNonRestoredState` ausente obligatorio | PASS — snapshot corrupto RECHAZADO por Flink (0 jobs vivos, 0 ocurrencias del flag) |

## Cobertura final (números honestos, sin maquillaje)

Batería fresh completa ×2 sobre `0e17c4d3` (101 paquetes por corrida; 202 logs revisados por C con 0 FAIL; BASE `ac0621a1`):

- **Archivos nuevos (`efprod-coverage.sh`): 2267/2734 bloques = 82.92% → UNDER_THRESHOLD (exit 1 por diseño).** La cifra 1982/2050=96.68% del ciclo GI se conservaba para el delta anterior; el delta GI-2 añadió ~684 bloques (attest protocol, seal/restore-args, group offsets env-gated, productor de frescura, wiring) de los que ~285 quedaron cubiertos por la batería sin entorno de broker real.
- **Diff-aware (`efprod-diff-coverage.sh`): 396/518 bloques = 76.45% subset observado, exit 2** (9 archivos del denominador sin ningún dato de perfil; el exit de método precede al check de umbral). La nueva métrica expuso que código del CICLO ANTERIOR en archivos preexistentes (p.ej. `core/cmd/echo-core/main.go`, `functions/*` 60-75%, `market/batch.go` 50%) tampoco alcanzaba 95% — era invisible para la métrica de archivos nuevos: ese es exactamente el hallazgo GI-QA-EVIDENCE.
- Causa principal de la brecha: rutas de integración real-broker que sólo corren env-gated (`ECHO_TEST_KAFKA_BROKERS`, loopback-only) fuera de la batería + patas de wiring/`os.Exit` declaradas como process-input + archivos sin observación listados (nunca excluidos en silencio).
- C# (Ninja AddOn/harnesses): sin instrumentación equivalente — declarado, sin porcentaje inventado.
- **La brecha NO se maquilló** (ni aserciones ajustadas ni exclusiones encubiertas): queda como hallazgo visible para la adjudicación G-IMPL del Manager, con la causa y los comandos reproducibles publicados.

## Verificación independiente (verificador C, read-only, SHA `0e17c4d3`)

Ítems 1-7 del mandato: **PASS** (restore real con lectores reales; vacío/omitido BLOCKED; topic recreado rechazado; FRESH expirado rechazado en readiness y último salto; M1 y egress intactos — ahora 8 egress exactly-once por manifest con el nuevo egress de control; FEFB/F1/M2/Ninja merge intactos, delta dentro del ownership; cobertura y regresiones reconciliadas). Cero MATERIAL. C re-verificó la integridad de la evidencia cruda (SHA256 de binarios del lab == declarados; PIDs y timestamps coherentes; digests de manifest consistentes entre seal/gate/attest/negativos; el svc del lab usa el sdk del MISMO árbol con `replace` y firma con `recovery.SignAttestReport`; 202 logs de cobertura 0 FAIL) y ejecutó tests puntuales en el SHA (CLI completo ok 1.569s con competitor PASS; futuresruntime -run Attest 3/3; echo-core attest wiring PASS; permit/session/market ok; vet limpio; `TestRealModuleFiles` PASS sobre ambos module.yaml).

## Residuales y NOT_RUN

1. Attest CLEAN vía el binario echo-core integrado no demostrado físicamente en el lab (el lab no compone postgres/namespace futures; el handler del wiring está cubierto por unit tests y el protocolo quedó demostrado end-to-end con el contrato sdk real) — punto G-ENV/G-REC.
2. S4 dual-JM físico: el dist StateFun no expone ruta de submit; la exclusividad de submitter queda demostrada por unit test + ruta cerrada en crudo; una demostración con dos JM vivos requiere dist con flink-runtime-web.
3. `TestFEFBW4CapacityCampaign` (functions) se cuelga >600s TAMBIÉN en el baseline `9daa57cb` (verificado con stash) — preexistente; corre con `-skip` junto a los 2 skips heredados.
4. Brecha de cobertura (§Cobertura): 82.92% / 76.45% subset vs ≥95% GOD-03 — decisión del Manager.
5. `run-l3` deja `L3-SUMMARY.txt` vacío (los veredictos van a consola); comentario doc en `offset_window.go:35-36` dice «32 lowercase hex» donde el código usa base64url 22 chars — sólo documentación (MINOR de C).
6. Todos los NOT_RUN heredados del cierre GI siguen vigentes (G-ENV/G-REC/G-FEED/G-SIM/PROD sin autorización): commit-at-checkpoint con función remota, PG outbox real, terminal NT físico, SIM/venue, envelope/capacidad, power-loss eléctrico, RCA E01 UNRESOLVED.

## Límites y estado físico

Sin deploy, sin merge a master, sin ETCD/Kafka/Flink/PG compartidos del Owner, sin Ninja físico, sin cuentas ni órdenes; el lab es un nuevo directorio loopback con puertos propios y kills por PID. Estado operativo permanece DESARMADO. Evidencia de trabajo: `~/aranea/work/ef-prod-gimpl-20261025/` (CONTINUITY.md, briefs/{A,B,C}.md, evidence/{A-REPORT,A-L3-RESTORE,A-L3-FINAL,B-REPORT,B-COVERAGE-FINAL,C-REPORT}.md); agent-run [[2026-10-25-zcode-glm53-flash-ef-prod-gi2]].
