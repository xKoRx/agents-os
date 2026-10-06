# R2c · IMPLEMENTATION REPORT — Ronda 3 remediation loop MKE V2 · Clutifx Ch01

- **Implementador:** one-shot, sesión fresca. Fecha: 2026-10-05.
- **Repo:** `/home/kor/mke/multimodal-knowledge-engine`, branch `feature/v2-layered-knowledge-model`, base `e7bc387` (verificado `git fetch origin` + divergencia 0/0 contra `origin/feature/v2-layered-knowledge-model` antes de tocar; **no se pusheó**).
- **Commits:**
  - `be240f9` — `feat(claims): calibrate relations branch of grounding reviewer to mke.claims-ground.v4 (R-M10)`
  - `1d06ce8` — `fix(sko): tolerate @N suffix drift in composition review outputs (R-M07 parity)`

---

## Fix 1 — Calibración relations v4 (M-10)

**Defecto (evidencia):** el reviewer v3 no aplicaba sus propias cláusulas de enactuación/deixis en la rama relations (16/17 rechazos = FN; `FULL-RELATION-AUDIT.md` §3), era inconsistente ante evidencia idéntica (8 pares gemelos con veredictos opuestos, tabla §3) y usó mal EQUIVALENT_TO (4 FP, §4). En claims, v3 está sano: 0 FN (GROUNDING-AUDIT §2).

**Qué se cambió** (`internal/claims/records.go`, `internal/claims/review.go`):

1. **`PromptVersionGrounding` → `mke.claims-ground.v4`** (superficie de invalidación/fingerprint) y header `review_contract: claims.grounding_review calibration-4` (sin token con forma de schema id, propiedad de v3 conservada).
2. **Nueva constante `groundingRelationsCalibrationV4`**, inyectada SOLO en la rama relations. Cuatro reglas deterministas:
   - **Orientación** (FP2 `rel-cierre-fuera-rango-candidato`): subject a la izquierda del tipo tal como está listado; si la evidencia enactúa el enlace en dirección inversa, la orientación enunciada no está soportada (few-shot real: «el rango viejo se elimina porque la vela cierra fuera, y entonces surge el candidato» enactúa candidato←cierre).
   - **Dependencia enactuada/implícita**: soportada cuando la evidencia enuncia ambos extremos Y cualquier enlace de dependencia/secuencia/causa/habilitación, aunque sea implícito en la narrativa («después de X», «para poder Y», «esto hace que Z», «una vez pasa esto», «y todo esto basado en…», «que ya lo tenemos en 12 horas»), sin exigir las palabras literales «depends on». Few-shots REALES del P8b (los 6 acordados como FN por ambas auditorías, incluidos los 4 nombrados en el encargo): formación←cierre (asr-00105-06), continuación←cierre-fuera (asr-00063-64), no-Turtle-Soup←no-reacción (asr-00130-31), SMT←objetivos-EUR (asr-00196), elimina→reanaliza (asr-00161-73), «todo esto basado en las temporalidades» (asr-00083-84). Se conserva la frase de v3 `even without the literal words "depends on"`.
   - **Co-ocurrencia negativa** (FP1 + TN gemelo): «podemos copiar la selección» no depende de «tres velas blancas seleccionadas» (observaciones coordinadas del mismo estado de pantalla); «pendiente también» es comparación de estados, no dependencia.
   - **Anti-inconsistencia**: mismo enunciado + misma evidencia citada = mismo veredicto, se decida por la proposición y no por la ventana; cita explícitamente el hallazgo de los 8 pares gemelos con el ejemplo formación←apertura soportada vs formación←cierre rechazada sobre los mismos segmentos.
   - **EQUIVALENT_TO restringido** (FP3/FP4): sólo identidad referencial demostrada (mismo contenido proposicional o mismo referente demostrablemente nombrado dos veces); yuxtaposición temática y alias no demostrado = INSUFFICIENT. Few-shots reales: «se denominará reiniciado» vs etiqueta en pantalla «RANGO PENDIENTE» (reclasificación contrastante, no sinonimia); «tartel sub» (alias hablado) vs definición funcional de Turtle Soup.
3. **Intacto a propósito:** la rama claims conserva byte a byte la calibración v3 (guías Identity/Deixis/Causal-definicional + atomicity ATOMIC|COMPOSITE) y el bloque anti-rubber-stamp compartido (`groundingResolutionSafetyBlock`, sin cambios). El conjunto de schema ids de respuesta sigue cerrado en {v1, v2}.

## Fix 2 — Tolerancia @N en composition_review (paridad R-M07)

**Defecto (evidencia):** 7/33 composition reviews de P7b rechazadas mecánicamente porque la respuesta ecoaba el header `target: <id>@<versión>` en `sko_id` y añadía la versión otra vez (`sko-…@1@1` ≠ target `id@1`), quemando el veredicto interno COMPOSITION_SUPPORTED y un reissue cada vez; `sko-range-completion` perdió su review en cascada (L2-SKO-AUDIT §3).

**Qué se cambió** (`internal/sko/closure.go`):
- `ParseCompositionReviewResponse` ahora liga la dirección tras `normalizeSKOAddress`, que elimina **uno o más** sufijos finales `@<dígitos>`. Difiere del normalizador de claims («exactamente uno») por una razón documentada: el header de composition review SÍ lleva versión (`target: id@1`, a diferencia de la línea de record de claims), así que la deriva observada es doblada; y el vocabulario de ids SKO (`sko-` + slug) nunca contiene `@`, por lo que colapsar sufijos no puede fundir dos identidades válidas.
- **Fail-closed intacto:** el campo `version` debe seguir igualando la versión del target; un id genuinamente distinto nunca resuelve; schema id, veredicto, entradas de relación (vacías/duplicadas), datos tras el JSON y campos desconocidos se rechazan igual que antes; los errores preservan el valor crudo para auditoría.
- **Schema id sin tolerancia nueva** (cláusula «conjunto cerrado… si aplica» del encargo: no aplica): el journal P8b muestra 0 deriva de schema en composition reviews —el header `sko.composition_review v1` no lleva token con forma de schema id—, así que añadir tolerancia no observada solo abriría superficie fail-open.

## Tests

Nuevos:
- `internal/claims/review_relations_v4_test.go`:
  - `TestRelationGateAppliesOneStandardToP8bTwinPairs` — 5 de los 8 pares gemelos del audit (mínimo pedido: 3): la respuesta SUPPORTED de cualquiera de los dos gemelos liga y parsea idénticamente por la puerta estructural (una sola vara; la assimetría mecánica que descartó veredictos válidos en v3 no puede distinguir gemelos). Pares: toma-low, timeframes, formación (apertura/cierre), continuación (sin-rango/cierra-fuera), bordes bearish.
  - `TestRelationGateAcceptsSupportedVerdictForP8bCausalRelations` — los 8 causales del Grupo A del audit como fixtures de puerta estructural (el veredicto semántico es del reviewer calibrado; la puerta jamás vuelve a perderlos mecánicamente).
  - `TestRelationsBranchV4PinsRulesAgainstTheFourP8bFalsePositives` — los 4 FP fijados por la regla exacta de v4 que los excluye (lo semántico es del modelo — prompt pineado; chequeo estructural fail-closed añadido donde aplica: respuesta con deriva doblada para esos ids sigue sin ligar).
  - `TestV4RelationsCalibrationDoesNotLeakIntoClaimsBranch` — la rama claims conserva sus guías v3 y no recibe ninguna regla relations-only; el split de atomicity por rama se mantiene.
- `internal/sko/review_tolerance_test.go`:
  - `TestParseCompositionReviewResponseToleratesP7bAddressEcho` — el caso `@1@1` real (`sko-range-completion`, `sko-scalp-range-conditions` del journal) y variantes de sufijo simple/múltiple parsean a su veredicto con payload intacto.
  - `TestParseCompositionReviewResponseToleranceStaysFailClosed` — 10 desviaciones fuera de la tolerancia siguen malformadas (id distinto, mutación de slug, versión incorrecta con y sin eco, schema, veredicto, relaciones, trailing data, unknown field), con el valor crudo en el mensaje.
  - `TestNormalizeSKOAddressStripsTrailingSuffixes` — 10 casos unitarios del normalizador.

Actualizado mínimamente: `TestReviewRequestContractV3Guides` → `TestReviewRequestContractV4Guides` (sólo la versión pineada `mke.claims-ground.v3`→`v4` y el rename; todas sus aserciones intactas). R-M05/R-M06/R-M07 y el resto de ronda 2: sin cambios y en verde.

**Verificación:**
- `go vet ./internal/... ./cmd/...` — OK.
- `go test ./internal/claims/... ./internal/pipeline/... ./internal/sko/... -count=1 -timeout 30m` — verde (pipeline 104s incluido).
- `go test ./... -count=1` repo completo — 20/20 paquetes ok.

## Desviaciones del encargo

1. **Few-shots: 6 en el prompt, no los 8 del Grupo A.** Del grupo causal del audit, `rel-eliminacion-rango-requiere-invalidez` y `rel-falso-turtle-soup-depende-de-reaccion-real` están clasificadas CORRECT_REJECTION (borderline) por GROUNDING-AUDIT §3; pinearlas como soportadas enseñaría sobre-aceptación. El prompt fija los 6 casos que ambas auditorías acuerdan como FN (incluye los 4 nombrados en el encargo). Los 8 aparecen igualmente como fixtures de puerta estructural.
2. **Los 4 FP no son detectables estructuralmente** (relaciones bien formadas entre claims válidos y distintos); según el propio encargo («lo semántico es del modelo — pinnea el prompt») se fijaron por texto de regla en el prompt + fail-closed estructural de la puerta de respuesta donde aplica.
3. **Normalizador SKO con strip múltiple** en vez de «exactamente uno» como claims — justificado arriba (header versionado; deriva observada doblada). El requisito duro del encargo («`id@1@1` parsea a su veredicto») lo exige.
4. **Sin tolerancia de schema ids en composition review** — sin evidencia de deriva en el journal; el «si aplica» del encargo resuelto como «no aplica».

## FEEDBACK (Agents-OS)

1. **El mandato de bootstrap es inaplicable en subagentes de tarea**: el bloque `AGENTS_OS_MANAGED` del workspace ordena invocar `80-agents/skills/agents-os-bootstrap/SKILL.md` al inicio, pero la herramienta Skill no está disponible para subagentes (error literal «Skill is not allowed for subagent»). Es la misma fricción que reportaron los auditores P8 (GROUNDING-AUDIT, FEEDBACK #1). Tercer reporte consecutivo: o el bootstrap se inyecta como capacidad alcanzable por todo agente que vea el marker, o el bloque debe decir explícitamente qué hacer cuando el skill no es alcanzable (hoy: regla muerta en la práctica; esta sesión procedió directo al encargo).
2. **Encargos que dicen «tests intactos» sobre constantes que el fix mueve**: R-M07 pineaba `mke.claims-ground.v3` en `TestReviewRequestContractV3Guides`; el bump a v4 obliga a tocarlo. Lo resolví conservadoramente (sólo la versión pineada + rename, todas las aserciones conservadas). Sugerencia para la plantilla de encargo: «los tests previos deben seguir pasando; actualiza sólo los literales de versión que el propio fix mueve» — evita ambigüedad entre «no tocar el archivo» y «no romper cobertura».
3. **Las auditorías con citas fila a fila son oro para implementar**: los few-shots del prompt v4 y los fixtures de test se transcribieron directamente de las citas asr-*/frame de FULL-RELATION-AUDIT y GROUNDING-AUDIT sin re-verificar el corpus. Mantener el estándar «toda afirmación con su cita» en los audits — es lo que permite a un implementador de contexto fresco trabajar sin releer 200 segmentos.
4. **Diseño ya adjudicado + alcance cerrado funcionó bien**: ninguna decisión de diseño abierta durante la sesión; las 4 desviaciones documentadas son de precisión (qué few-shots, cuánto strip, qué tolerar), no de dirección. El patrón «Manager adjudica desde evidencia, implementador ejecuta acotado» evitó re-litigar el trade-off precisión/recall.

---

*Ronda 3 lista para re-audit: la rama relations tiene reglas deterministas con few-shots reales (M-10), la puerta de composition review ya no quema veredictos por eco de dirección (paridad R-M07), y el fail-closed de ambas capas está pineado por test.*
