---
type: remediation_plan
schema_version: 1
status: final
created: "2026-10-18"
area: "[[Echo]]"
project: "[[Echo Forge — Operación Real V2]]"
tags:
  - kind/plan
  - area/echo
  - tech/performance
---

# REMEDIATION — corrección real del defecto de suministro (no workaround)

Principio: la causa demostrada es de SUMINISTRO de trabajo (lote 1 + secuencialidad de groups con `source`), no del motor. Corregir el suministro con el mínimo cambio compatible con los contratos congelados. Nada de esto toca 0.3.1 en producción: son decisiones para el Manager/owner con evidencia lista.

## Vía 1 (config de campaña, SIN cambio de código) — RECOMENDADA

**Subir `batch_size` del group de retester durable** (semántica canónica congelada por owner 2026-09-28: batch_size = paralelismo interno SQX por host). El funnel declara hoy `batch_size:1` en el group robust (con `source`); los stages de retest por lote admiten N por corrida.

- Evidencia de efecto: ladder físico N=10→600 — throughput 4,5→36,7 str/s monotónico, pico 72-74 cores a N≥450, paridad de repetibilidad (n30 ×3, n300 ×2).
- Alcance por campaña: iterable por campaña (dimensión declarada por el owner); NO aplica al optimizer (contrato exactly-1-upstream intacto) ni al final reretester (1 estrategia por contrato de fidelidad).
- Riesgos medidos: memoria JVM crece con N (MaxRSS 1,4→2,7 GB en 90 estr; heap 55 G da margen sobrado); blast radius de reintento por lote mayor (chunk fallido = re-lote completo). Sugerido: 60-150 en primera adopción, medir, escalar.
- Gate: decisión owner/Manager en la config de la siguiente campaña (es config, no release).

## Vía 2 (código candidate, requiere aprobación de arquitectura) — SI la Vía 1 es insuficiente

**Habilitar fan-out `max_parallel` para groups con `source`** (hoy fail-closed a secuencial: `generic_workflow.go:1790-1834`, `config.go:268-271`). Permitiría procesar chunks en paralelo ENTRE hosts conservando el orden durable dentro de cada chunk. Cambio mínimo y acotado en el predicado del fan-out + test del contrato; decisión exclusiva del Manager (el mandato lo marca como cambio de contrato congelado → adjudicación, no implementación unilateral). NO implementado en esta sesión.

## Vía 3 (fuera de alcance deliberado)

- Overview exporter secuencial (87 % del wall del builder): candidato existente `perf/overview-s02` (4,7-5,1× medido), pendiente de integración por el pipeline de release estándar. NO re-tratado aquí por directiva del mandato.
- Modo SQX residente para amortizar boot de retests de 1 estrategia (final reretester): requiere rediseño del contrato un-proceso-por-actividad; documentado como no viable KISS en S01.

## Deuda del harness de medición (candidate-local, sin impacto en flota)

1. `p0-prep-retest.sh` hardcodeaba sqx144-p0 (corregido a `SQXROOT`); los runs `retest142-n3/n10/n90` del primer ladder quedan INVALIDADOS en CPU-BENCHMARK.csv.
2. Campo psr del sampler per-tid desalineado (métrica distinct_cpus inválida); los canales usados (group jiffies, per-tid ticks, RUNNABLE, task-time, throughput) son válidos.
3. jcmd attach no funciona contra el JVM del launcher (snapshots vacíos); si se quiere evidencia de nombres de pool: correr la GUI/CLI con JFR (flag ya documentado en sqcli.config) en ventana owner.

## Rollback

Ninguna mutación de flota/repo/release en esta sesión: veredicto + evidencia + harness candidate-local (`/home/echo-dev/forge-multicore-p0/`, 15 MB crudo) + entrega en vault. Las Vías 1-2 son decisiones futuras; cada una con su propio plan de rollout/rollback al momento de adoptarse.
