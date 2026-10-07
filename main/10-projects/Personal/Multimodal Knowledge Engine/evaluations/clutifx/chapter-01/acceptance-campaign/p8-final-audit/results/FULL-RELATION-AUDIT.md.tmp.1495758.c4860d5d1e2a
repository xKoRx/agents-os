# FULL RELATION AUDIT — Clutifx 01 · candidato rerun @ 19b44c1 (P8 aceptación exhaustiva)

- **Alcance**: población COMPLETA de relations canónicas del candidato — **146/146 auditadas, sin muestreo**.
- **Fuente**: `/home/kor/mke/clutifx-ch01-rerun-20261003/run-rerun/claims.jsonl` (records `claim_relation`), corpus por ventana (`corpus/wNNNN.json`) y frames en disco (`/home/kor/mke/clutifx-ch01-20260930/media-run/evidence/objects/`).
- **Detalle fila a fila**: `FULL-RELATION-AUDIT.jsonl` (146 filas, con `engine_publication` y `windows` por relación).
- **Verificación visual**: se inspeccionaron 32 frames citados por relaciones (objetivos 1.15160 / 1.16148 / 1.15803, límites 1.34155 / 1.35843, borrado de rectángulos, diagramas SMT/Power-of-3, rangos 4H/15M); el resto del soporte es transcripcional con evidencia ASR verificada literalmente.

## 1. Distribución de labels (candidato)

| Label | n | % |
|---|---|---|
| CORRECT | 139 | 95.2% |
| UNSUPPORTED | 7 | 4.8% |
| WRONG_TYPE | 0 | 0% |
| WRONG_ENDPOINT | 0 | 0% |
| **Total** | **146** | 100% |

Tipos: DEPENDS_ON 134, EXCEPTION_TO 10, EQUIVALENT_TO 1, CONTRADICTS 1. Ninguna relación con tipo inadecuado ni endpoints equivocados; los 7 UNSUPPORTED fallan por falta de soporte de la fuente (dependencia no enunciada o dirección invertida), no por errores de construcción.

## 2. Old-vs-new (run viejo 130 relations vs candidato 146)

| Métrica | Run viejo | Candidato | Lectura |
|---|---|---|---|
| Relations | 130 | 146 | +12% población |
| CORRECT | 126 (96.9%) | 139 (95.2%) | −1.7 pp, dentro de lo esperable al crecer el pool |
| WRONG_TYPE | 2 | **0** | mejora: desaparece esa clase de error |
| WRONG_ENDPOINT | 0 (implícito) | 0 | estable |
| Precisión del engine al ACEPTAR | 111/112 (99.1%, 1 falso positivo) | **128/128 (100%, 0 falsos positivos)** | **mejora**: no hay regresión escondida entre las SUPPORTED |
| Rechazos del engine | 18 (15 falsos negativos, 83%) | 18 (11 falsos negativos, 61%) | mejora relativa, pero la mayoría de rechazos sigue siendo falsa alarma |
| Rechazo publicado como CONTRADICTED | — | 1 (rel-gbpusd-rango-dep-smt) | **falso negativo claro** (ver abajo) |

**Conclusión old-vs-new**: no hay regresión escondida. El modo de fallo dominante del viejo run (falsos positivos al aceptar + WRONG_TYPE) desaparece en el candidato; el residual se concentra en falsos negativos del revisor automático, mismo patrón cualitativo que el baseline pero en menor proporción.

## 3. Falsos positivos entre las SUPPORTED (128)

**Ninguno.** Las 128 relations publicadas como `SUPPORTED_BY_AUTOMATED_REVIEW` resultaron CORRECT en auditoría fuente-grounded (transcripción verificada literalmente; frames inspeccionados donde citados). Precisión del engine al aceptar: **128/128 = 100%**.

Observación menor (no es error): el par cl-range-opens-below-previous / cl-range-takes-previous-candle-low está cubierto dos veces (una EQUIVALENT_TO y una DEPENDS_ON en dirección inversa) desde el mismo asr-00101. Ambas son sostenibles, pero es duplicación estructural digna de dedup en capas superiores.

## 4. Rechazos del engine (18): 7 correctos, 11 falsos negativos

### 4.1 Rechazos correctos (7) — la relación realmente no está sostenida
1. rel-facilidad-rangos-ligada-a-temporalidad-diaria
2. rel-close-inside-pending-open-context
3. rel-other-candle-pending-open-context
4. rel-comprobar-objetivo-tras-reanalisis
5. rel-smt-config-pair-reverses (dirección de dependencia invertida: el reversal es consecuencia, no fundamento)
6. rel-smt-config-pair-type («ya sea JP o DXY» es incidental)
7. rel-lower-entry-depends-manipulation (pregunta retórica sin respuesta en la fuente)

### 4.2 Falsos negativos (11) — la relación SÍ está sostenida por la fuente
| relation_id | Causa raíz |
|---|---|
| rel-rango-requiere-extremo-vela-anterior | **Citación truncada**: falta asr-00018 («normalmente pasa que nos toma»), que contiene el claim objeto |
| rel-misidentification-error-depends-on-confusion | **Citación truncada**: falta asr-00132 (la apariencia de subida), el revisor solo vio asr-00133 |
| rel-movimiento-tras-rango-bajista | Encadenamiento narrativo subestimado («Pues» + frame del objetivo 1.15160) |
| rel-rango-bajista-tras-rango-alcista | Encadenamiento cíclico («es ir completando los rangos»); borderline |
| rel-pendiente-requiere-objetivo-bullish | Fórmula «Rango a favor, o sea, alcista con el objetivo bullish, rango pendiente» |
| rel-pendiente-requiere-rango-alcista | **Inconsistencia**: misma dependencia aceptada en rel-pendiente-depende-rango-alcista (claims duplicados entre ventanas) |
| rel-smt-config-pair-misses-target | **Inconsistencia**: la condición simétrica sí fue aceptada como rel-smt-divergencia-correlacionado |
| rel-smt-visibility-scope | Construcción relativa única («Este es un tipo de SMT que si no conoces la estrategia no vas a poder ver») |
| rel-reversal-directo-smt | Dirección correcta del anclaje anafórico (a diferencia de rel-smt-config-pair-reverses, bien rechazada) |
| rel-gbpusd-rango-dep-smt | **Publicado UNSUPPORTED_CONTRADICTED y es falso**: «esto es una SMT que nos indica que esto de GIP es un rango también» sostiene directamente la relación; «esto de GIP» = elemento GBPUSD |
| rel-situacion-ideal-depends-creacion-rango | «es lo ideal porque te está creando un rango alcista»; cualificaciones grounded en los claims de los extremos |

Patrón dominante de los falsos negativos: (a) ventanas de citación que cortan el nexo (2 casos idénticos al patrón del run viejo), (b) tratamiento inconsistente de pares de claims duplicados entre ventanas contiguas (el mismo contenido se acepta con un par de claim-ids y se rechaza con el duplicado), (c) conservadurismo ante dependencias anafóricas/encadenadas que sí están explícitas.

## 5. Recomendaciones al engine (resumen)

1. **Expandir la ventana de citación** de evidencia ASR de relaciones a ±1 segmento (los 2 falsos negativos por truncación desaparecerían).
2. **Dedup de claims duplicados entre ventanas** antes del grounding de relaciones: elimina las inconsistencias aceptar/rechazar el mismo par semántico (3 falsos negativos).
3. **Revisar el veredicto UNSUPPORTED_CONTRADICTED** de rel-gbpusd-rango-dep-smt: la relative «que nos indica que» es un conector de soporte directo, no contradicción.
4. Mantener el criterio actual de rechazo para enumeraciones coordinadas sin nexo (funciona: los 7 rechazos correctos son de esa familia o de dirección invertida).

## FEEDBACK (Agents-OS)

Contexto: sesión one-shot de auditoría (subagente P8) sobre el vault `/home/kor/secondbrain/main`. Bootstrap ejecutado conforme (constitución + perfil + nota de continuidad); el resto del flujo fue mecánico sobre datos externos al vault, sin necesidad de routing de entidad adicional.

1. **Bootstrap en subagentes one-shot**: el procedimiento cold-start exige 4+ lecturas antes de trabajar. Para tareas de subagente con instrucción completa del coordinador, sería útil una variante "bootstrap mínimo" (constitución + continuidad, 2 archivos) explícitamente permitida, porque el router de entidad no aporta nada cuando el coordinator ya resolvió paths y procedimiento. Coste actual: bajo pero no cero.
2. **Regla 5 (una fuente canónica por hecho) funcionó bien**: los resultados del audit viven en el proyecto (`10-projects/.../p8-final-audit/results/`) y este informe no duplica procedimiento (queda en el skill si hiciera falta). Sin fricción.
3. **Detección de truncación de citas como antipatrón recurrente** (run viejo y candidato): merece una nota de memoria interna del proyecto MKE para que futuras auditorías verifiquen siempre el pasaje ±1 segmento antes de aceptar un rechazo del engine como correcto; ahorraría re-auditoría.
4. Sin anomalías de vault ni de templates aplicables en esta sesión: no se crearon documentos de Sistema 2 (solo artefactos de resultados del proyecto, que es su ubicación canónica).
