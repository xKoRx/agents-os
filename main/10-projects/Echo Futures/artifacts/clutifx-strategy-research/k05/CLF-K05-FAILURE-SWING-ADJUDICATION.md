# CLF-K05 — FAILURE SWING ADJUDICATION (FASE 3 · P0)

Misión: CLF-K05 · Fecha: 2026-10-26 · Host: Daedalus · Código auditado: `xKoRx/echo` @ `e8c2e47e` (rama `experiment/clutifx-s01`, worktree limpio) · Fuente: `knowledge-library/clutifx/ch06-failure-swing/` (CLAIMS `9b001973…`, rules, compiled `05-failure-swing.md`, frames 31) + usos en ch07 (c-0197–c-0206), ch08 (c-0072–c-0074), ch09 (c-0028).

Método: los 64 claims de ch06 leídos completos (incluida la evidencia de frames ya integrada en cada claim), confrontados claim-a-claim contra `detectors/failureswing.go`, `decision.go::entryFailureSwing`, `config.go` y `pipeline.go`. El audio del vídeo no es accesible desde Daedalus; la evidencia audiovisual disponible son los frames extraídos y las transcripciones ASR ya resueltas en los claims (garbles `fellow/pelo/Fearless swing` normalizados por el propio payload). Las dudas que SOLO el audio/vídeo pueden cerrar van a la cola de vídeo con minuto exacto.

## Veredicto

```text
FAILURE_SWING_VERDICT = EXTRA_RESTRICTION_CONFIRMED_PARCIAL
  La conjunción implementada (reacción AND order block AND motivo, strict = 1 vela)
  es MÁS ESTRICTA que la fuente en DOS ejes adjudicables por texto y deja un tercio
  genuinamente ambiguo:
    (1) Order block   : OPCIONAL en la fuente  → implementado OBLIGATORIO   [EXTRA_RESTRICTION]
    (2) Reacción      : "creando rango opuesto" en la fuente → implementada
        "cierre más allá del nivel fallido"                        [WRONG_PREDICATE]
    (3) Ventana       : la fuente NO acota a 1 vela (multi-vela hasta
        invalidación; OB esperable "si quieres")                   [EXTRA_RESTRICTION]
    (4) Puerta de motivo : FIEL (R9 respetada: sin motivo no hay FS)
    (5) Stop/objetivo : stop NOT_IN_SOURCE (declarado); objetivo = rango de la
        vela fallida (c-0007/c-0063)                              [MATCH_SOURCE]
  Consecuencia: la frecuencia 0-setups observada (69+9 sesiones NQZ6/NQU6 y
  trimestre completo) NO puede atribuirse a rareza genuina mientras (1)-(3)
  persistan: KRR-003 pasa de REVIEW_VIDEO a FIX_CODE (adjudicado por fuente) +
  REVIEW_VIDEO residual (2 preguntas acotadas).
```

## 1. Las siete preguntas del mandato

### 1.1 ¿El order block es obligatorio o opcional?

**OPCIONAL.** Cadena de evidencia: el procedimiento canónico de identificación en vivo, `ch06 c-0029` (06:03–06:31, kind=procedure), NO incluye el OB: «va subiendo y, cuando veis que reacciona ya para abajo creando algún rango bajista y veis que hay alguno de los motivos comentados, ahí es donde dices 'failure swing' y puedes entrar». La opcionalidad queda explícita en `c-0047` (09:52–09:55): «En el gráfico de 15 minutos es un poco igual; **puedes esperar si quieres** al order block». El OB aparece como confirmación observada en los DOS ejemplos trabajados en espejo (`c-0038` «se te crea ya un order block que **podría ser** el cambio en la tendencia» — lenguaje probabilístico dicho; `c-0041`; `c-0046` «vemos la reacción alcista, vemos cómo se crea un order block, y ahí decimos»), todos de la mano de la definición ch01 `c-0107` (cierre por fuera de la última vela de color contrario), que es la que el código implementa correctamente como predicado.

Residuo honesto: `c-0046` es también kind=procedure y enuncia el OB dentro de la frase de identificación del caso espejo; un lector puede sostener «OB requerido en el espejo». La lectura dominante es la opcionalidad (c-0047 se dice EN el mismo ejemplo del espejo), pero esta tensión concreta va a la cola de vídeo (minuto 9:37–9:55). La definición de OB del código (`orderBlockConfirmed`, espejo de ch01 `c-0107`) es fiel; lo que excede la fuente es EXIGIRLA.

### 1.2 ¿Qué constituye exactamente una reacción?

La fuente la define dos veces con el mismo predicado: «reacciona **ya** para abajo **creando algún rango bajista**» (`c-0012` 02:49–03:05; `c-0029` 06:03–06:31; espejo `c-0045`/`c-0046` reacción alcista). Es decir: reacción = la formación de un RANGO en dirección contraria al extremo fallido (el átomo rango de ch01 `c-0005`: toma del extremo contrario + cierre adentro). El código implementa otra cosa: `reactionClose` = cierre de la vela más allá del nivel fallido (`failureswing.go:321–326`). Los dos predicados no son ni superconjunto ni subconjunto: un cierre bajo el nivel fallido puede no crear rango bajista alguno, y un rango bajista puede formarse con cierres todavía por encima del nivel fallido si el rango es local. **El predicado implementado NO es el predicado enseñado**; es una operacionalización sustituta congelada sin declarar la sustitución en esos términos. Corrección: reacción = `EventRangeCreated` con side opuesto al extremo fallido sobre la cadena del TF de observación (1h, `c-0040`).

### 1.3 ¿Cuáles son las condiciones suficientes para entrar?

`reacción (creación de rango opuesto) + UNO de los tres motivos` (`c-0029`, «alguno de los motivos»), con el contexto del sistema global: rangos a favor para operar el trade (`c-0058`–`c-0059`; regla transversal ch04 `c-0044` y ch07 `c-0214`) y la preferencia personal declarada pendientes > reiniciados (`c-0060`, «a mí me gustan más» — preferencia dicha, no condición). El OB es confirmación opcional (§1.1). La entrada puede además refinarse a 30/15 sin esperar la activación clásica (`c-0013`, `c-0019`, R6). La implementación exige reacción+OB+motivo Y además proxiza «rangos a favor» SOLO por el bias nativo 1d, sin exponer los rangos adversos de su propia cadena al evaluador de red flags (`decision.go:376–382` pasa `AdverseRanges` vacío; el comentario lo declara) — ver F-K05-05.

### 1.4 ¿Qué motivos son alternativos?

Los tres son alternativos en OR: SMT (`c-0008`/`c-0009`), extremo hecho al final de vela/hora (`c-0010`/`c-0014`/`c-0052`/`c-0054`/`c-0056`), feed de otro broker (`c-0021`/`c-0023`/`c-0024`, «muy pocas veces» `c-0032`). Con un solo feed, los motivos 1 y 3 son inaplicables: el seam externo (`Motive func`) es nil en V1 y el detector reporta `MOTIVE_UNAVAILABLE` y re-arma (fail-closed, fiel). Sólo el motivo 2 es computable — correcto. La puerta R9 (`c-0011`/`c-0015`: extremo-de-final-de-vela SOLO no anticipa FS) está respetada por diseño: sin motivo no hay veredicto.

### 1.5 ¿Qué secuencia temporal exige el instructor?

(1) El motivo EXISTE antes del fallo: el extremo quedó hecho al final de la vela ANTERIOR (`c-0010`, `c-0044`: «para el algoritmo, este low ya está como en la siguiente vela»), o la SMT del par correlacionado ya ocurrió, o el otro feed ya lo tomó. (2) La vela nueva sube hacia el extremo y FALLA sin tomarlo. (3) La reacción aparece «ya» — durante la vela en curso del fallo o en las velas inmediatas — creando el rango opuesto (`c-0041`: a las 6:00 abre, baja un poquito, reacciona fuerte y crea el OB — mismo tramo). (4) Identificación y entrada sobre la marcha (`c-0063`), refinables a 30/15 (`c-0013`). El código respeta (1) correctamente: `motiveEndOfCandle` examina la composición 1m de la VELA DE REFERENCIA (la del extremo), no de la vela del intento — objeto correcto. Falla en (3) por la ventana de 1 vela strict (§1.6) y por el predicado de reacción (§1.2).

### 1.6 ¿La confirmación cabe en una vela o puede atravesar varias?

PUEDE ATRAVESAR VARIAS. La fuente no acota la confirmación a una vela: el OB puede esperarse explícitamente después (`c-0047`), el ejemplo del espejo desarrolla reacción + OB a lo largo de varias velas de 5m tras la apertura (`c-0041`), y el estado natural del FS es «vive hasta que el extremo fallido es finalmente tomado» (`c-0048`: «el algoritmo respeta el failure swing y no hace un nuevo low» — la invalidación es la toma posterior del extremo, no el paso del reloj). La ventana strict = exactamente la vela siguiente (y la conjunción reacción+OB en ESA MISMA vela, `failureswing.go:280–318`) es una restricción numérica sin fuente. La ventana wide = N=3 velas es igualmente arbitraria (default sin fuente). Ambas son ejes OP declarados como tolerancias; NINGUNA es la semántica fuente. Corrección: ventana por defecto = hasta invalidación (toma del extremo fallido / eliminación del rango de reacción), con strict/wide conservados como variantes experimentales pre-declaradas.

### 1.7 ¿Las tolerancias numéricas implementadas aparecen en el curso?

NO. `ApproachTicks` (≥1 tick, REQUIRED fail-closed), `EndMinutes` (1..60), `WideReactionBars` (default 3), `FSTolerance strict|wide` — ninguno existe en el curso. Están declarados honestamente como OP congelados (`failureswing.go:30–45`). Dos observaciones de fidelidad: (a) el curso sí da UNA pista fraccional para el motivo 2 en ch07 `c-0202` («8:30 es muy cerca del final de la vela de 4h… como en el **15%** del final de la vela») — sugiere semántica FRACCIONAL de vela (4h×15% = 36 min) en lugar de minutos absolutos; la cifra es de un ejemplo visual no verbalizado como regla ⇒ parámetro Owner, no fuente; (b) `ApproachTicks` con N pequeño (p.ej. 1 tick en NQ = 0,25) hace el disparador casi imposible y con N grande lo degrada a «cualquier vela en la zona»; es el parámetro de máxima sensibilidad del detector y no tiene ancla en el curso (la «aproximación» dibujada en `f-000059` es visual).

### 1.8 ¿Qué configuraciones son fieles y cuáles son hipótesis?

| Config | Estado | Fundamento |
|---|---|---|
| Motivo 2 como único motivo computable, seam externo nil fail-closed | FIEL | `c-0008`/`c-0021` requieren datos externos ausentes; KRR-006 |
| OB como predicado (definición ch01 c-0107 espejo) | FIEL como predicado | `c-0107`; lo infiel es EXIGIRLA (§1.1) |
| Stop = extremo fallido | OP declarada (NOT_IN_SOURCE) | espejo de stop-en-TS ch01 `c-0067`; documentado |
| Objetivo = rango de la vela fallida (extremo opuesto) | FIEL | `c-0007`/`c-0028`/`c-0063` |
| TF de observación 1h | FIEL (creencia dicha) | `c-0040` «yo creo» — hedge preservado |
| strict/wide, ApproachTicks, EndMinutes, WideReactionBars | OP/HIP | sin fuente; sensibles |
| Conjunción reacción+OB+motivo | NO FIEL | §1.1/§1.2 — adjudicada |
| S14 (strict) como control y S15 (wide) como variante | EJE MAL ESPECIFICADO | el eje real de la fuente es OB opcional + predicado de reacción + ventana; S14/S15 varían un parámetro que no es la ambigüedad de la fuente |

## 2. Reconciliación con el estado previo

Q04/KRR-003 dejaron la duda abierta («rareza genuina vs conjunción excedida»), por prudencia correcta. K05 la cierra EN PARTE por texto: los ejes (1) OB y (2) predicado de reacción y (3) ventana son decidibles desde `c-0029`/`c-0047`/`c-0012` sin audio; queda abierto por vídeo sólo si el instructor en el espejo (9:37–9:55) exige el OB en 1h, y la fracción «15%» (`c-0202`, ch07). Por tanto: **no se declara SOURCE_PASS del detector actual**; se declara `EXTRA_RESTRICTION_CONFIRMED` con corrección lista para Hefesto (`CLF-K05-HEFESTO-IMPLEMENTATION-HANDOFF.md`, F-K05-02/03/04/05) y re-gateo G2A/G2C propio de C06/S15/T04 tras el fix. La relajación SIN el fix sigue prohibida (regla KRR-003 vigente).

## 3. Frecuencia esperable post-fix

Ninguna cifra del curso permite prometer frecuencia; lo declarado es cualitativo: el propio instructor desaconseja obsesionarse (`c-0002`/`c-0062`), el caso broker «pasa muy pocas veces» (`c-0032`), y el capítulo entero construye un trade real encadenando 3 FS en 1h+8h (`c-0061`) — es decir, el instructor los encuentra en un día concreto de EURUSD, no son eventos de una por trimestre. Con la conjunción excedida, 0 en 78 sesiones medidas no infiere nada; tras el fix, el funnel G2A dirá. La lección económica Q04 sigue aplicando: aun operando, FS necesitaría ~7 ejecuciones limpias/trimestre para ser aprobable en el diseño de cuenta GAU50 1:1 target $3.000.
