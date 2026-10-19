---
type: acceptance
schema_version: 1
status: final
created: "2026-10-19"
area: "[[Echo]]"
project: "[[Echo Forge — Operación Real V2]]"
application: "[[xKoRx/symphony]]"
baseline: "xKoRx/symphony 492a271e (0.3.1); SQX 144.2953; sqx-zeus/sqx-hera/sqx-kronos"
verdict: "SQX144_FULL_MULTICORE_CERTIFIED (scope excluido: CustomAnalysis del builder de producción)"
tags:
  - kind/acceptance
  - area/echo
  - tech/performance
---

# ACCEPTANCE — gates del mandato (sección 10)

## Gate 1 — Multicore real → PASS

- >1 core simultáneo con correlación de trabajo útil: 30/30 optimizer runs, ladder completo en 3 hosts y builders con stop funcional; outputs válidos en cada run (estrategias sincronizadas, WFO completado).
- Múltiples threads consumiendo CPU: hasta 148 threads del grupo con ticks positivos; mediana RUNNABLE en ventana cálida 72/60/24-25 (Kronos/Hera/Zeus optimizer opt-02).
- Mejora de throughput con paralelismo útil: ladder monotónico 3/3 hosts (4,7→37,1 / 4,8→42,4 / 11,9→52,8 str/s).
- Los picos aislados no se usan como prueba: las medias integrales (jiffies/segundo sobre la ventana) son la métrica primaria.

## Gate 2 — Aprovechamiento de capacidad → PASS

- Retester: 87-92% de los cores en n300-n600 (3 hosts). Optimizer: 70-94% sostenido por ventana de cálculo en 30/30 runs. Builder: picos 94-100% y medias 68-88% en ventanas de segundos; capacidad sostenida demostrada además por la maratón v2 (~3 h a ~100% en los 3 hosts, observación viva) y el antecedente P0 (68,46 × 40 min).
- Fases que no lo consiguen, identificadas y cuantificadas: boot JVM+datos (2-5 cores, 10-18 s, serial por diseño) y save/serialización (~0 cores, 1,5-1,7 s, I/O) — juntas <60% del wall en los builders cortos; CustomAnalysis del builder de producción: secuencial (evidencia previa, fuera del alcance certificado).

## Gate 3 — Agrupaciones → PASS

- Retester: ≥10 estrategias por ejecución SQX (hasta 600), comprobado por conteos de entrada/salida en consola.
- Optimizer: grupo de 10 con exactamente 1 estrategia upstream por ejecución (30 ejecuciones selladas).
- Builder: 20 estrategias auténticas destinadas a la prueba integrada; cohort de 10 para la cadena.

## Gate 4 — Flota → PASS

Evidencia física independiente en Zeus (27), Hera (60) y Kronos (72). Ningún PASS extrapolado: cada host tiene su ladder, su grupo de optimizadores, su builder y su cadena integrada propias.

## Gate 5 — Integración → PASS

Continuidad Builder→Retester→Optimizer por SHA256 en los 3 hosts (sello = 0 faltantes); procedencia auténtica (builder_test.cfx del repo @ 492a271e); sin estrategias inventadas, duplicados, resultados viejos ni pérdidas silenciosas (validaciones en INTEGRATED-RUN.md).

## Restricciones del mandato — cumplimiento

- UNA instancia SQX por VM: guard pgrep antes de cada lanzamiento; 0 violaciones en toda la campaña.
- Un JSON de workflow / un GenericSQXWorkflow raíz: no aplica (harness candidate-local declarado; no se modificó ningún workflow).
- Sin cancelar workflows ajenos, sin reiniciar servicios, sin tocar systemd/ETCD/código productivo/CFX del Owner/databanks productivos: cumplido (0 mutaciones de producto).
- Sin corpus sintético como evidencia principal: corpora auténticos de campaña (overview1117, corpus-pristine, output de builder real).
- Cargas finitas por condición de negocio: stop funcional del builder (databank lleno); ladder por N explícitos; WFO completo por estrategia.
- Única intervención sobre procesos propios: maratón v2 detenida (SIGKILL documentado) tras demostrar 100% de rechazo con stop inalcanzable; los 3 builders v2 eran procesos del propio harness.

## Limitaciones de la certificación

1. CustomAnalysis: NOT_APPLICABLE aquí; evidencia previa la muestra secuencial en el builder de producción. El global se emite con esa exclusión de alcance explícita.
2. Los CSV crudos del maratón v2 fueron sobrescritos por la re-ejecución v5 (mismo label `build-r1`); la saturación del maratón queda documentada como observación viva (loadavg) y no como run certificado.
3. Picos >nproc en Kronos: artefacto de VM; medias integrales usadas como métrica primaria.
4. El builder certificado (builder_test) tiene ventanas de cálculo cortas (1,7-11 s) por su cap interno MaxStrategies=20; la ventana corta se compensa con picos 94-100%, la maratón y el antecedente P0.
5. GUI-vs-CLI y MT5 permanecen fuera del alcance (igual que en P0).

## Veredicto

**`SQX144_FULL_MULTICORE_CERTIFIED`** — motor SQX 144 (genético/retester/optimizer) y cadena integrada, físicamente demostrados en la flota completa con una instancia por VM; alcance excluido y documentado: CustomAnalysis del builder de producción (secuencial según evidencia previa; remediación registrada).
