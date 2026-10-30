---
type: session
schema_version: 1
scope: session
created: "2026-10-30"
updated: "2026-10-30"
area: "[[Personal]]"
project: "[[Polymarket Engine — MVP]]"
application:
entities:
  - "[[Polymarket Engine — MVP]]"
related:
  - "[[Research — Default Suite Isolation W1-nR 2026-10-30]]"
aliases: []
confidence: high
source_session:
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/session
  - scope/session
  - project/polymarket-engine
---

%% Filename: YYYY-MM-DD[-HHMM]-<human-topic>-summary.md. Never use UUIDs/hashes as visible names; put external IDs in source_session. %%

# 2026-10-30-polymarket-w1nr-isolation-summary

> [!info]+ Session summary L1
> Resumen operativo. Para beta queda fuera del corpus normal de Graphify.

## Objetivo

- Corregir la desviación de aislamiento de W1-n: la suite por defecto de `cmd/researchpilot` reanálisis el episodio sellado y sobrescribió el artefacto de revisión W1-m. Un solo disparo correctivo, con gate previo, sin releer ni reanalizar un episodio real.

## Contexto cargado

- Bootstrap AGENTS OS completo en 14/14 ventanas exigidas (AGENTS global, AGENTS del vault, bootstrap, constitución, perfil, memoria global única, catálogo de skills, registro de routers, retrieval) más ventanas de la continuidad Five-POC y documentos W1-n, W1-m, W1-l, W1-e y preregistros W1-g/W1-h.
- Entidad `[[Polymarket Engine — MVP]]` (área `Personal`): cero matches en el registro de routers ⇒ DEFAULT sin router.
- Corrección de una premisa heredada: W1-n afirmó «cero episodio real» cuando su propia suite sí lo invocó. Esta sesión partió de esa rectificación, no de la afirmación.

## Trabajo realizado

- **Aislamiento del test histórico:** opt-in explícito como primera sentencia ejecutable, raíz de entrada explícita sin fallback host-específico, y salida de la revisión a `t.TempDir()` con la metadata leída copiada byte a byte al scratch; el árbol sellado conserva bytes y lista de archivos.
- **Aislamiento de `TestMain`:** guard de opt-out como segunda sentencia; la exportación de recibos requiere opt-in y una raíz nueva, crea directorios propios únicos y rechaza raíces no configuradas, insecuras o ya existentes en vez de sobrescribirlas.
- **Corrección posterior a la revisión de la supervisión (misma sesión, commit `e4d201a`):** la primera entrega había perdido el `if code == 0` que la versión anterior tenía, de modo que con opt-in de exportación una suite **roja** podía acuñar recibos `all_required_cases_passed` cuando los casos requeridos se habían visto. Se añadió el rechazo `code != 0` **antes de cualquier trabajo de recibo o exportación**, conservando las dos primeras sentencias exigidas y el comportamiento por defecto.
- **Regresión negativa de esa garantía:** un subproceso sintético que pre-marca los nueve casos requeridos y falla a propósito, con opt-in de exportación explícito y raíz propia; el padre exige salida con fallo, el mensaje de rechazo y la ausencia de la raíz de exportación. El helper corre sólo con un flag único, sin definir en el camino normal, y no lee ni replica ningún episodio.
- **Regresiones nuevas** con recursos sintéticos: orden del guard, aislamiento entrada/salida, ruta de revisión que escribe sólo bajo su `outDir`, y contrato de la exportación de recibos.
- **Análisis documental de fees** (tabla de identidad, as-of, valor bruto, fuente, disponibilidad y qué puede/no certifica) y **adjudicación de la regla de L** con las citas exactas del prereg v1/v2, el orden de código verificado y la recomendación de preservar la semántica congelada declarándola en el próximo prereg.

## Artifacts creados o modificados

- Repo `polymarket-engine`, dos commits locales sin push: `4acf954407ede3e5bb42d057f35d7b2c7f02c913` (aislamiento de la suite) y `e4d201a391bf97b5f43c5287366deda57242e258` (garantía de corrida verde + regresión negativa): `cmd/researchpilot/economics_test.go`, `cmd/researchpilot/supervisor_test.go`, `cmd/researchpilot/w1nr_isolation_test.go` (nuevo).
- Vault: [[Research — Default Suite Isolation W1-nR 2026-10-30]] (nueva), [[Polymarket Engine — Continuidad Five-POC 2026-09-20]] y [[Polymarket Engine — MVP]] (actualizados), más resumen, feedback, agent run y change log de esta sesión.

## Memoria propuesta o creada

- Ninguna memoria interna nueva: el delta es continuidad y estado de proyecto, que viven en las notas canónicas de `[[Polymarket Engine — MVP]]` y en el informe de research.

## Decisiones

- Preservar la semántica congelada de `L` (`ref` excluye el frame de señal, `L` lo incluye) y **declararla explícitamente** en el próximo preregistro, en vez de cambiar el engine: el código ya no lee frames posteriores al instante de decisión y el artefacto W1-m publicado codifica ambas banderas, así que cambiarlo invalidaría la comparación pineada.
- No tocar `L` ni correr sensibilidad alternativa en este shot; la elección de la regla sigue siendo del Owner por preregistro.
- No proponer cuenta propia, órdenes ni fondos como requisito: la evidencia pública ya capturada basta para el siguiente paso.

## Pendiente

- **Siguiente paso documental ejecutable:** auditar la identidad de fee del mercado objetivo `5784455` y sus 2 assets en lectura offline sobre el journal ya capturado, con `known_at` reales, pasando el conjunto por el `FeeResolverV1` existente; comparar explícitamente con la evidencia W1-e de otros mercados sin transferir tasas ni fechas.
- Decisión del Owner pendiente sobre la regla de L (opción recomendada: preservar y declarar).
- La medición de los 90 hashes sellados y de la lista final de archivos corresponde al supervisor; esta sesión sólo puede afirmar que no escribió en rutas selladas y que el preflight informó `sealed_unchanged: true`.
- El flake de timing preexistente `TestStepSequenceWaitsForAbsoluteSlotStart` (umbral de 200 ms) volvió a aparecer **dos** veces en la suite de esta continuación (199.512005 ms y 199.026946 ms) antes de una tercera corrida registrada en verde; el test que falla no fue tocado por esta corrección.
- `REAL_FEE_READY=false` y OOS/live permanecen desactivados; no hay segundo shot ni relanzamiento.