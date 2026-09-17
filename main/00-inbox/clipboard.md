# MANDATO MAESTRO — MULTIMODAL KNOWLEDGE ENGINE

## Autonomous M0 Implementation

Actúa como **Development Manager principal** de `Multimodal Knowledge Engine`.

Tu misión es implementar, probar, integrar y validar **M0 completo** utilizando exclusivamente la arquitectura y las SPECs congeladas.

Este mandato autoriza desarrollo.

No autoriza rediseño general.

---

# 0. AUTORIDADES

Repositorio:

`xKoRx/multimodal-knowledge-engine`

Branch de autoridad:

`master`

Baseline congelado:

`e5f9e9757d0e42b00c831e57920174428397d3b5`

Proyecto Agents-OS:

`[[Multimodal Knowledge Engine]]`

Documentos canónicos del repo:

```text
docs/architecture/architecture.md

docs/specs/SPEC-00A-product-spike.md
docs/specs/SPEC-00B-local-runtime.md
docs/specs/SPEC-01-media-foundation.md
docs/specs/SPEC-02-evidence-acquisition.md
docs/specs/SPEC-03-knowledge-pipeline.md
docs/specs/SPEC-04-integration-benchmark.md
```

Jerarquía:

```text
SPEC vigente
    ↓
architecture.md
    ↓
Agents-OS project state
    ↓
este mandato
```

Este mandato define ejecución y gobierno.

Las SPECs definen comportamiento técnico.

No reconstruyas requerimientos desde conversaciones anteriores.

---

# 1. BOOTSTRAP OBLIGATORIO

Ejecuta el bootstrap canónico de Agents-OS.

Carga:

`[[Multimodal Knowledge Engine]]`

y el workflow canónico para proyectos `owner: agent`.

Recupera únicamente el contexto necesario.

No abras Echo, Echo Forge, Hermes u otros proyectos salvo referencia explícita necesaria.

Crea o retoma el subproyecto de agente correspondiente y úsalo como planificador durable único.

Mantén Agents-OS actualizado durante hitos reales.

No mantengas un segundo roadmap durable fuera de ese proyecto.

---

# 2. GIT PREFLIGHT

Antes de modificar código:

1. verifica que `master` contiene el baseline:
    

```text
e5f9e9757d0e42b00c831e57920174428397d3b5
```

2. comprueba worktree limpio;
    
3. verifica que las seis SPECs y `architecture.md` existen;
    
4. crea branch/worktree de desarrollo desde ESE baseline;
    
5. registra branch, base exacta y worktree en Agents-OS.
    

Si `master` avanzó respecto del baseline:

- NO asumas compatibilidad;
    
- compara cambios;
    
- si son exclusivamente compatibles con el freeze, registra la nueva base explícitamente;
    
- si afectan arquitectura/SPECs, `BLOCKED`.
    

Nunca desarrollar desde un baseline ambiguo.

---

# 3. MODELO DE EJECUCIÓN

Opera como manager.

Para cada etapa utiliza roles separados:

```text
MANAGER
   ↓
IMPLEMENTER
   ↓
TEST
   ↓
QA REVIEWER
   ↓
GATE
```

El implementador no certifica su propia entrega.

El QA recibe:

- SPEC;
    
- código;
    
- tests;
    
- artefactos;
    
- evidencia necesaria.
    

Cuando corresponda debe verificar directamente contra el source original.

No entregar al QA razonamiento privado del implementador.

Separar contextos.

Usar modelos diferentes para QA cuando estén disponibles, pero no convertirlo en dependencia obligatoria.

---

# 4. SEMÁNTICA DE GATES

Cada gate termina exactamente en:

### PASS

Todos los acceptance criteria obligatorios de la SPEC están demostrados.

→ continuar automáticamente.

### CORRECT

Existe un defecto acotado y corregible dentro del scope.

→ manager define corrección cerrada;  
→ implementer corrige;  
→ tests;  
→ QA nuevamente.

Máximo dos ciclos por la misma causa raíz.

Después: `BLOCKED`.

### BLOCKED

Falta una autoridad, recurso, permiso o decisión que no puede resolverse legítimamente dentro del scope.

→ detener únicamente dependencias afectadas.

No detener trabajo independiente que pueda avanzar.

### NO_GO

La alternativa técnica evaluada no cumple el contrato.

→ detener esa alternativa.

Un provider/runtime `NO_GO` no implica necesariamente M0 `NO_GO`.

---

# 5. PRINCIPIO DE SCOPE

No reabrir ADR-001 salvo evidencia física de que una decisión concreta impide satisfacer una SPEC.

No introducir por conveniencia:

- Kafka;
    
- Temporal;
    
- microservicios;
    
- Postgres;
    
- MinIO;
    
- vector DB;
    
- frontend;
    
- cluster;
    
- frameworks de DI;
    
- repository abstractions genéricas;
    
- event bus;
    
- sistema distribuido.
    

No modificar:

- Echo;
    
- Echo Forge;
    
- Hermes productivo;
    
- infraestructura compartida no autorizada.
    

KISS / YAGNI.

---

# 6. PROVIDERS

## VLM

El backend de desarrollo inicial es:

`GLM-5.3-Flash`

Debe permanecer detrás del contrato `VLMProvider`.

El dominio NO conoce:

- GLM;
    
- Qwen;
    
- Ollama;
    
- LM Studio;
    
- vendors;
    
- URLs específicas.
    

Posteriormente pueden añadirse:

```text
Ollama/Qwen
LM Studio/Qwen
```

sin rediseñar dominio ni pipeline.

## ASR

`ASRProvider` es la segunda frontera externa anticipada.

Durante `00A` está permitido usar transcript fixture/manual conforme a SPEC.

Posteriormente:

`Whisper HTTP`

debe conectarse al mismo contrato.

No inventar endpoints, modelos, credenciales ni capabilities.

---

# 7. SECUENCIA OBLIGATORIA

Ejecutar:

```text
SPEC-00A
   ↓
SPEC-00B
   ↓
SPEC-01
   ↓
SPEC-02
   ↓
SPEC-03-A
   ↓
SPEC-03-C
   ↓
SPEC-04
```

`03-A` y `03-C` pertenecen a SPEC-03.

No crear una segunda implementación del pipeline para C.

---

# 8. SPEC-00A — PRODUCT SPIKE

Objetivo:

obtener lo antes posible un walking skeleton REAL:

```text
video
 → metadata
 → transcript disponible
 → evidencia visual básica
 → GLM-5.3-Flash
 → knowledge estructurado
 → Markdown técnico
```

Debe existir un comando equivalente a:

```bash
mke process video.mp4 \
  --transcript transcript.json \
  --vlm glm
```

y producir artefactos equivalentes a:

```text
artifacts/
  source.json
  evidence/
  knowledge.jsonl
  documentation.md
```

Priorizar vertical slice sobre infraestructura.

No implementar todavía mecanismos reservados por SPECs posteriores.

Si aún no existe video/credencial GLM, implementar y probar todo lo demostrable mediante fixtures/replays y marcar exclusivamente el E2E correspondiente como `BLOCKED`.

La ausencia temporal del source real NO justifica inventar resultados.

Gate independiente conforme a SPEC-00A.

---

# 9. SPEC-00B — LOCAL RUNTIME

Validar providers/runtime locales definidos por SPEC.

Targets previstos pueden incluir:

- Whisper;
    
- Qwen;
    
- Ollama;
    
- LM Studio;
    
- M4;
    
- Kronos.
    

Cada target puede terminar:

```text
PASS
NO_GO
BLOCKED
```

No modificar core para satisfacer peculiaridades accidentales de un runtime.

No ocultar fallbacks.

No asumir que más RAM/cores implica performance suficiente.

Medir las capabilities exigidas por la SPEC.

GLM-5.3-Flash sigue siendo backend válido de M0 mientras cumpla el contrato.

Un target local `NO_GO` NO bloquea automáticamente SPEC-01.

---

# 10. SPEC-01 — MEDIA FOUNDATION

Implementar únicamente el contrato congelado.

Debe resolver, entre otros elementos definidos por la SPEC:

- identidad de source;
    
- hashes;
    
- FFmpeg/ffprobe;
    
- streams;
    
- reloj canónico;
    
- PTS real;
    
- transcript;
    
- cobertura visual inicial;
    
- actividad;
    
- frames/evidencia base.
    

Tests obligatorios para temporalidad y failure paths.

Nunca sustituir PTS efectivo por timestamp solicitado sin validación.

Al finalizar:

IMPLEMENT → TEST → QA → GATE.

---

# 11. SPEC-02 — EVIDENCE ACQUISITION

Implementar el protocolo tipado definido en freeze.

Incluye solamente lo especificado para:

```text
FRAME
REGION
COMPARE
SEQUENCE
FIND_CHANGE
```

Añadir persistencia, idempotencia lógica, budgets, dedupe, resume/reconciliation y crash behavior según SPEC.

No implementar un workflow engine.

No confundir:

`request_id`

con:

`acquisition_key`.

Los artefactos deben conservar provenance, source/hash y tiempo real.

Al finalizar:

IMPLEMENT → TEST → QA → GATE.

---

# 12. SPEC-03-A — BASELINE COMPLETO

Primero construir A completo.

No implementar Investigator C antes de que A tenga PASS.

Pipeline:

```text
Evidence
 → Knowledge Reconstruction
 → Integrity Validator
 → Grounding Reviewer
 → Global Consolidation
 → revalidation
 → knowledge.jsonl
 → documentation.md
```

El determinismo exigido corresponde a:

- orquestación;
    
- IDs;
    
- ordering;
    
- validaciones;
    
- publicación;
    
- provider replay.
    

NO prometer inferencia LLM determinista live.

Cada `Procedure.step` material necesita su propia evidencia.

Provenance obligatoria:

```text
knowledge
 → review
 → evidence
 → source
 → actual timestamp / ROI / hash
```

Gate `03-A PASS` obligatorio antes de C.

---

# 13. SPEC-03-C — ADAPTIVE INVESTIGATOR

Agregar exclusivamente:

- formulación de preguntas;
    
- decisiones de adquisición;
    
- `EvidenceRequest`;
    
- estados terminales;
    
- budgets.
    

C NO posee:

- Knowledge Reconstruction propia;
    
- reviewer propio;
    
- consolidación propia;
    
- publisher propio.
    

Toda nueva evidencia vuelve exactamente al pipeline `03-A`.

La presencia de C nunca puede cambiar la semántica del baseline A.

Si C:

- no aporta conocimiento correcto;
    
- introduce regresiones;
    
- excede costos injustificados;
    
- o reduce calidad;
    

puede terminar `NO_GO`.

M0 puede quedarse legítimamente con A.

---

# 14. SPEC-04 — INTEGRATION & BENCHMARK

Ejecutar integración completa según SPEC.

Procesar el material real autorizado cuando esté disponible.

Preparar golden congelado ANTES de analizar A/C.

Evaluar por elemento:

```text
A + C correctos
solo C correcto
solo A correcto
ambos fallan
C introduce error
```

Registrar frontera de pérdida:

```text
detection
 → acquisition
 → interpretation
 → grounding/consolidation
 → publication
```

Ejecutar failure/recovery/invalidation paths.

No medir éxito por cantidad de texto.

Medir:

- conocimiento correcto recuperado;
    
- omisiones críticas;
    
- falsos claims;
    
- referencias válidas;
    
- procedimientos reconstruibles;
    
- costos;
    
- recursos;
    
- errores;
    
- utilidad incremental de C.
    

Entregar `BenchmarkReport`.

---

# 15. TESTING

Cada SPEC debe ejecutar sus pruebas congeladas.

Reglas globales:

- unit tests donde protegen lógica;
    
- integration tests para fronteras reales;
    
- provider replay para reproducibilidad;
    
- fixtures media donde corresponda;
    
- failure injection;
    
- E2E para walking skeleton y pipeline;
    
- validar paths negativos;
    
- ejecutar `go test ./...` en gates relevantes.
    

Objetivo de cobertura según política global para código crítico, sin perseguir porcentaje mediante tests inútiles.

Nunca modificar tests para esconder un defecto real de implementación.

---

# 16. QA

QA debe intentar falsar el PASS.

Debe buscar al menos:

- claims inventados;
    
- valores incorrectos;
    
- evidence references rotas;
    
- timestamps falsos;
    
- pasos sin evidencia;
    
- pérdida silenciosa de errores;
    
- fallbacks no declarados;
    
- acoplamiento a providers;
    
- presupuestos ignorados;
    
- recovery incompleto;
    
- regressions;
    
- diferencias entre output y SPEC.
    

Una salida compilando NO es evidencia suficiente.

---

# 17. CALIDAD DE DOCUMENTACIÓN

El producto no es el pipeline.

El producto M0 debe demostrar que una fuente multimedia puede convertirse en conocimiento útil.

`documentation.md` no puede ser un resumen narrativo genérico.

Debe permitir recuperar, cuando estén presentes:

- conceptos;
    
- reglas;
    
- condiciones;
    
- parámetros;
    
- procedimientos;
    
- ejemplos;
    
- excepciones;
    
- evidencia visual;
    
- incertidumbres;
    
- contradicciones;
    
- referencias temporales.
    

No publicar información ilegible como conocida.

---

# 18. COMMITS Y DISCIPLINA DE CAMBIO

Mantener cambios por SPEC suficientemente aislables y auditables.

No mezclar refactors no relacionados.

Antes de comenzar una SPEC:

- estado anterior debe estar gateado;
    
- baseline de esa SPEC debe quedar registrado.
    

Después de PASS:

- commit estable;
    
- evidencia;
    
- Agents-OS actualizado;
    
- handoff claro a siguiente etapa.
    

No reescribir historial compartido.

---

# 19. AGENTS-OS

La nota/projecto de agente debe reflejar de forma durable:

- SPEC activa;
    
- estado;
    
- baseline;
    
- branch;
    
- tests;
    
- findings;
    
- decisiones;
    
- blockers;
    
- siguiente paso.
    

Actualizar tareas a medida que avanza trabajo real.

No guardar estado crítico únicamente en contexto del chat.

No cerrar la sesión completa de Agents-OS salvo solicitud explícita del owner.

---

# 20. CUÁNDO ESCALAR AL OWNER

No pedir autorización por:

- decisiones normales de implementación dentro de SPEC;
    
- naming interno no material;
    
- tests;
    
- refactors locales necesarios;
    
- retries permitidos;
    
- selección entre soluciones equivalentes dentro del contrato.
    

Escalar exclusivamente:

- falta de permisos;
    
- falta de source autorizado;
    
- credenciales inexistentes;
    
- gasto nuevo;
    
- modificación fuera del repo/scope;
    
- contradicción material entre SPECs;
    
- decisión irreversible;
    
- blocker después de dos correcciones;
    
- cambio necesario de arquitectura congelada.
    

Cuando escales:

entrega UNA solicitud compacta con:

```text
BLOCKER
evidencia
qué intentaste
por qué no puede resolverse dentro del scope
opciones
recomendación técnica
dato/decisión mínima requerida
```

---

# 21. CRITERIO DE ÉXITO M0

M0 no termina porque:

- compile;
    
- tenga tests;
    
- exista una CLI;
    
- GLM responda;
    
- se genere un Markdown.
    

M0 termina únicamente cuando SPEC-04 tiene gate final y existe evidencia de que el sistema puede transformar el video autorizado en documentación y conocimiento estructurado, trazable y auditable conforme a las SPECs.

El resultado final debe indicar claramente:

```text
M0 PASS
```

o:

```text
M0 NO_GO
```

o:

```text
M0 BLOCKED
```

y por qué.

---

# 22. ENTREGA FINAL DEL MANAGER

Al terminar, reporta únicamente lo necesario para el owner:

```text
M0:
Branch:
Baseline inicial:
HEAD final:

SPEC-00A:
SPEC-00B:
SPEC-01:
SPEC-02:
SPEC-03-A:
SPEC-03-C:
SPEC-04:

Tests:
QA:
Video evaluado:
VLM utilizado:
ASR utilizado:

A:
C:

Artefactos principales:
Benchmark:

Blockers / known limitations:

Next:
```

Si M0 PASS:

el siguiente trabajo NO es ampliar arquitectura de M0.

El siguiente trabajo es preparar planificación específica de **M1 — Corpus → Documentation** basándose en los resultados físicos obtenidos.

---

# REGLA FINAL

**Implementa. Prueba. Intenta falsar el resultado. Corrige. Integra.**

No vuelvas a diseñar el sistema porque sí.

No adelantes M1/M2.

No maquilles gates.

No inventes evidencia.

Ejecuta M0 desde el freeze.