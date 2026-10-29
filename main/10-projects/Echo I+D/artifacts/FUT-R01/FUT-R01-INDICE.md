---
type: doc
schema_version: 1
status: active
area: "[[Trading]]"
project: "[[Echo I+D — Futures]]"
related:
  - "[[FUT-R01-RV-01-CONSOLIDADO]]"
  - "[[FUT-R01-RESEARCH-MANDATE]]"
aliases:
  - "FUT-R01 expediente consolidado"
tags:
  - kind/doc
  - area/trading
  - project/echo-rnd
created: "2026-10-28"
updated: "2026-10-29"
---

# FUT-R01 — Expediente de DR-01–04 y RV-01

## Propósito

Reunir los retornos disponibles, el mandato/corrección Owner y el consolidado en una sola carpeta. Este índice es la entrada documental del expediente; [[Echo I+D — Futures]] conserva la planificación y decisiones del programa.

## Contenido

**Continuidad actual — 29-10-2026:** I01-A/B recibidos; adjudicación y propuesta de lote en [[FUT-R01-LOTE-COBERTURA-01]]. Ocho bases, siete existentes y una nueva, techo propuesto 24; primera preparación FBC15/ORB30/MR04. OWNER_ACCEPTANCE=REVIEW, sin ejecución. C conserva su manager; S04 SOURCE integrado, aceptación semántica pendiente al corte C04. La pausa y A/B pendientes de notas anteriores son antecedentes superseded.

**Estado al 28-10-2026:** RV-01 documental terminado con dictamen **`NO_APTO_AUN`**. Clasificación: **AUTORREVISIÓN ADVERSARIAL DOCUMENTAL**, porque la independencia histórica de autores no es acreditable. La reparación focal está incorporada en el consolidado. No se aprobaron gasto, ejecución, estrategias ni G0–G5.

### Orden de lectura

| Archivo | Qué contiene | Precaución |
|---|---|---|
| [Lote de cobertura 01](FUT-R01-LOTE-COBERTURA-01.md) | Recepción/adjudicación A/B, propuesta 8/24, paquetes, alternativas, costes y mandato LC01-PREP. | Recomendación del manager pendiente Owner; sin conformidad ni ejecución nuevas. |
| [I01-A: ficha de persistencia de cierre](FUT-R01-I01-SPEC.md) | Señal causal, geometría candidata y casos documentales. | Original preservado; entrada market/fill tardío necesita reparación antes del freeze ejecutable. |
| [I01-B: contratos y economía](FUT-R01-I01-CONTRATOS.md) | Perfil candidato Rapid EOD, UNKNOWN, MM y caja. | PARTIAL_DOCUMENTAL; A ya recibida; corregir estrategia/cuenta y atribución de fase 3/4 NQ. |
| [Consolidado RV-01](FUT-R01-RV-01-CONSOLIDADO.md) | Dictamen; 24 hallazgos con evidencia, impacto y reparación; caja/matemática; contradicciones; dependencias; decisiones Owner; experimento y alternativa; registro de fuentes. | Revisión de lo efectivamente disponible, sin certificar cuatro originales completos. |
| [Mandato v4 y corrección económica Owner](FUT-R01-RESEARCH-MANDATE.md) | Cápsula y alcance de los cuatro DR y RV-01; antecedente exploratorio rectificado. | Preservado sin cambios. Su estado histórico «NO EJECUTADOS» no sustituye este índice ni el planner actualizados. |
| [DR-01: captura editorial disponible](retornos/echo-futures-dr01-deep-research-2026-10-28.md) | Apartados, fórmulas y conclusiones preservadas por el agente de ingestión. | **No es el original íntegro** «Texto pegado(7).txt». Ausencia declarada, no reconstruida. |
| [DR-02 preservado](retornos/FUT-R01-DR-02-contratos-prop-NQ-2026-10-28.md) | Resumen, matriz comercial y notas con control de uso. | Retorno **PARCIAL**, 38 líneas, sin URLs oficiales. |
| [DR-03 preservado](retornos/FUT-R01-DR-03-mecanismos-NQ-2026-10-28.md) | Texto declarado íntegro por la ingestión más sus advertencias. | Los errores se adjudican en RV-01; no se corrige silenciosamente este original. |
| [DR-04 preservado](retornos/FUT-R01-DR-04-indicadores-reglas-validacion-NQ-2026-10-28.md) | Texto declarado íntegro por la ingestión más sus advertencias. | Las fichas no equivalen a especificaciones listas ni a evidencia de campañas. |

### Trazabilidad de la reorganización

Origen congelado: `xKoRx/agents-os@aa7c33a890c3686676c944d8448fdafa68886a9f`. Rutas de esta tabla relativas a `VAULT_ROOT`; el repositorio usa el prefijo `main/`. Se conservan los mismos blobs Git al mover: el contenido de los cuatro retornos disponibles y del mandato no cambia.

| Documento | Ruta anterior | Ruta actual dentro de este expediente | Blob Git preservado |
|---|---|---|---|
| DR-01 captura | `30-resources/futures/_sources/echo-futures-dr01-deep-research-2026-10-28.md` | `retornos/echo-futures-dr01-deep-research-2026-10-28.md` | `7702f0f689869724a56def97108b013d4bd215f3` |
| DR-02 | `10-projects/Echo I+D/artifacts/FUT-R01-DR-02-contratos-prop-NQ-2026-10-28.md` | `retornos/FUT-R01-DR-02-contratos-prop-NQ-2026-10-28.md` | `fb1b382958c4e8fdddcc8492f61c516ea7cf86d5` |
| DR-03 | `10-projects/Echo I+D/artifacts/FUT-R01-DR-03-mecanismos-NQ-2026-10-28.md` | `retornos/FUT-R01-DR-03-mecanismos-NQ-2026-10-28.md` | `af24bac2737898192679549046bcd929ff7c384e` |
| DR-04 | `10-projects/Echo I+D/artifacts/FUT-R01-DR-04-indicadores-reglas-validacion-NQ-2026-10-28.md` | `retornos/FUT-R01-DR-04-indicadores-reglas-validacion-NQ-2026-10-28.md` | `6f1a62221aaf5c74c5053f69f8ba74077131f170` |
| Mandato v4 | `10-projects/Echo I+D/artifacts/FUT-R01-RESEARCH-MANDATE.md` | `FUT-R01-RESEARCH-MANDATE.md` | `df4f10a048dc50c1ea75cc859ce563a4b77682d6` |

Los nombres de archivo se preservan para mantener resolución de wikilinks por título. Los punteros de provenance DR-01/DR-03 se actualizan a estas rutas; las páginas curadas siguen en su wiki y enlazan este expediente, sin duplicar retornos. Las rutas históricas quedan recuperables en el commit de origen. El SHA de un blob acredita igualdad de bytes respecto del archivo ya guardado, no integridad frente a un adjunto externo que no se conserva.

### Soporte y autoridades

- [[Echo Futures — DR-01 matemática de campañas prop]] y [[echo-futures-dr01-deep-research-2026-10-28-source]]: curación y provenance DR-01.
- [[Echo Futures — DR-03 mecanismos NQ evidencia y cobertura]] y [[echo-futures-dr03-deep-research-2026-10-28-source]]: curación y provenance DR-03.
- [[Echo I+D — Cobertura Futures]]: inventario y solapamientos; existencia no significa PASS.
- [[30-resources/runbooks/echo-futures-strategy-qualification-runbook]]: autoridad G0–G5, sin cambios.
- [[2026-10-28-echo-futures-rv01-consolidacion]]: cambio documental y cierre de sesión.
- [[2026-10-28-echo-futures-rv01-session-feedback]]: feedback del cierre.

### Siguiente decisión

**Continuidad vigente:** [[FUT-R01-LOTE-COBERTURA-01]] sustituye la espera de A/B por su recepción/adjudicación. Aceptar alcance de ocho bases/techo 24, congelar el primer paquete FBC15/ORB30/MR04 y recuperar receipts existentes; C mantiene su manager. La implementación, el presupuesto físico y las incógnitas contractuales siguen su propia admisión. No esperar a resolver toda la ruta comercial para clasificar mecanismos, ni usar esa preparación para declarar economía viable.

[[FUT-R01-ITERACION-01]] conserva el mandato de origen. El consolidado, los cinco blobs de entrada y ambos retornos A/B se preservan sin modificación. RV-01 sigue NO_APTO_AUN por alcance; no repetir los cuatro DR ni abrir DR-05. El cierre histórico de la sesión RV-01 no cierra el programa ni al manager Futures.

## Fuentes

- Los cinco blobs de entrada enumerados arriba y sus documentos de provenance.
- [[FUT-R01-RV-01-CONSOLIDADO#12. Registro de fuentes críticas y alcance realmente leído|Registro focal de fuentes y límites de lectura]].
- Instrucción Owner del 28-10-2026 para reunir originales, consolidar, publicar sobre master y cerrar con feedback.


### Continuidad posterior: frente C y economía de campañas

**28-10-2026:** [[FUT-R01-CAMPANAS-CHALLENGE-FUNDED-SIMULATION]] incorpora el último mandato Owner y los prompts de diseño/coordinación. Retiro variable, caja de compras, MM de resolución rápida dentro de reglas, umbral challenge 1/3 y reinversión total. S04 en integración a master informado por Owner; sustituye pausa anterior, no certifica finalización. Al momento de ese mandato A/B estaban pendientes; recepción y revisión resueltas después en [[FUT-R01-LOTE-COBERTURA-01]]. C nuevo no es el antiguo I01-C de recuperación. Los cinco archivos de entrada y RV-01 mantienen sus bytes y su alcance; esta continuidad no los reinterpreta como PASS.
