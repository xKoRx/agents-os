# MKE — PREWORK M0-R1

# ARIADNA — WHISPER LOCAL RUNTIME EN DAEDALUS

## ROLE 

Actúa como **Senior Linux / AI Runtime / Homelab Infrastructure Engineer** para preparar una dependencia local de MKE.

Trabajas directamente sobre **Daedalus** y tienes autoridad para:

- inspeccionar hardware y sistema;
    
- instalar dependencias;
    
- crear entornos Python si corresponde;
    
- instalar y configurar un runtime Whisper local;
    
- crear servicios systemd si es la opción correcta;
    
- probar CPU/GPU y seleccionar la configuración práctica;
    
- revisar logs, puertos, recursos y persistencia;
    
- hacer cambios operacionales necesarios en Daedalus.
    

Tu responsabilidad NO es implementar MKE.

Tu responsabilidad es dejar **Whisper local instalado, estable, persistente, observable y directamente consumible por el contrato ASR que MKE ya posee**.

No modifiques arquitectura ni código de MKE salvo que encuentres una incompatibilidad demostrable que haga imposible cumplir el contrato existente. En ese caso, NO la soluciones silenciosamente: documéntala para el Manager.

---

# OBJECTIVE

Dejar en Daedalus un runtime local de Whisper que MKE pueda consumir directamente mediante su adapter existente:

`internal/providers/whisper/whisper.go`

El resultado esperado es que posteriormente un agente de implementación MKE sólo tenga que configurar el endpoint/modelo y usar el `ASRProvider`.

No queremos otro script especial ni una integración paralela.

Queremos una **dependencia operacional local reusable**.

---

# CURRENT MKE AUTHORITY

Repositorio:

`xKoRx/multimodal-knowledge-engine`

Branch actual:

`fix/m0-live-readiness`

Baseline publicada:

`f522cbe55ca51f8617cd81f928b175407872a124`

Antes de decidir nada relacionado con compatibilidad, inspecciona en esa baseline:

- `internal/providers/asr.go`
    
- `internal/providers/whisper/whisper.go`
    
- `internal/providers/whisper/whisper_test.go`
    
- `scripts/asr_transcribe.py`
    
- `docs/runbooks/m0-live-certification.md`
    
- `docs/certification/m0-live-2026-09-28/README.md`
    

No asumas el contrato desde este prompt si el código dice algo más preciso.

El código es la autoridad técnica.

---

# CONTEXT

La primera certificación real de M0 ya utilizó ASR local sobre Daedalus.

Para el source certificado se utilizó:

- `faster-whisper`
    
- modelo `large-v3`
    
- CPU
    
- `compute_type=int8`
    

El helper actual es:

`scripts/asr_transcribe.py`

y produjo un transcript válido `mke.transcript.v1` para el source real.

Eso prueba que **faster-whisper puede funcionar en Daedalus**, pero no resuelve el requerimiento operacional actual.

M0-R1 necesita que Whisper quede detrás del `ASRProvider`, no como un helper Python especial utilizado fuera del runtime normal de MKE.

---

# EXISTING MKE ASR CONTRACT

MKE YA TIENE una abstracción neutral:

`providers.ASRProvider`

con:

`Transcribe(ctx, providers.TranscribeRequest)`

y YA TIENE un adapter Whisper-compatible HTTP.

Por tanto, tu instalación debe buscar compatibilidad con el contrato existente antes de proponer cambios de código.

## HTTP contract expected by MKE

El adapter consume un servicio Whisper/OpenAI-compatible.

Default endpoint:

`POST /v1/audio/transcriptions`

Request:

- `multipart/form-data`
    
- campo `file`
    
- campo `model`
    
- campo `response_format=verbose_json`
    
- campo `language` cuando corresponde
    

MKE espera una respuesta `verbose_json` compatible que permita obtener segmentos temporales.

Los segmentos relevantes contienen conceptualmente:

- `id`
    
- `start`
    
- `end`
    
- `text`
    

y la respuesta puede además contener:

- `language`
    
- `duration`
    
- `text`
    
- `model`
    

El adapter MKE transforma timestamps a milisegundos y después aplica sus propias invariantes de orden y plausibilidad.

No reemplaces esas validaciones por lógica del servidor.

---

# MKE RUNTIME CONFIGURATION

El adapter existente utiliza:

`MKE_WHISPER_BASE_URL`

`MKE_WHISPER_MODEL`

Opcionales:

`MKE_WHISPER_ENDPOINT`

`MKE_WHISPER_LANGUAGE`

`MKE_WHISPER_AUDIO_TYPE`

Defaults conocidos:

- endpoint: `/v1/audio/transcriptions`
    
- audio: `audio/wav`
    

No agregues innecesariamente nuevos requisitos operacionales.

Particularmente, revisa que la solución elegida no obligue a MKE a implementar autenticación sólo para consumir un servicio local.

---

# PRIMARY TASK

Inspecciona Daedalus y selecciona el runtime Whisper local **más simple y robusto que satisfaga el contrato real de MKE**.

Puedes considerar faster-whisper u otra implementación compatible, pero NO elijas por moda ni por features que MKE no utiliza.

Evalúa en la máquina real:

- CPU;
    
- RAM;
    
- GPU disponible;
    
- VRAM si existe GPU compatible;
    
- almacenamiento libre;
    
- versiones relevantes;
    
- capacidad real de inferencia.
    

Prioriza:

1. compatibilidad exacta con MKE;
    
2. estabilidad;
    
3. facilidad operacional;
    
4. rendimiento suficiente;
    
5. baja complejidad;
    
6. reproducibilidad.
    

KISS / YAGNI.

No introduzcas Docker, Kubernetes, CUDA, proxies, colas, bases de datos ni infraestructura adicional si no aportan una ventaja concreta para este caso.

Si una solución simple con systemd y un runtime local basta, eso es preferible.

---

# MODEL SELECTION

`large-v3` ya fue utilizado satisfactoriamente en la certificación inicial y constituye una referencia válida.

Sin embargo, no asumas automáticamente que es la configuración operacional óptima.

Inspecciona la máquina y decide con evidencia:

- modelo;
    
- device;
    
- compute type;
    
- cantidad relevante de threads/workers;
    
- parámetros necesarios para estabilidad.
    

La calidad del transcript importa.

MKE trabaja con material técnico, cursos y narración que puede contener vocabulario inglés dentro de discurso español.

No optimices rendimiento destruyendo materialmente la calidad.

Registra la selección final y por qué fue elegida.

---

# SERVICE REQUIREMENTS

El runtime debe quedar disponible como un **servicio local estable**, no como un comando que el usuario tenga que levantar manualmente cada vez.

Debe sobrevivir:

- cierre de terminal;
    
- logout;
    
- reinicio de Daedalus.
    

Debe poder:

- iniciar;
    
- detenerse;
    
- reiniciarse;
    
- consultar estado;
    
- consultar logs.
    

Usa el mecanismo nativo que tenga más sentido en Daedalus; systemd es válido si corresponde.

No expongas Whisper públicamente a Internet.

Por defecto prefiere loopback/local host si eso permite que MKE lo consuma.

Sólo amplía el bind a otra interfaz si existe una necesidad real y explícita del runtime MKE, y documenta la razón.

No abras servicios externos innecesarios.

---

# SECURITY / HYGIENE

No:

- publiques el endpoint a Internet;
    
- abras puertos en firewall sin necesidad;
    
- registres secretos;
    
- copies material privado a repositorios;
    
- subas audio/video/transcripts privados a servicios externos;
    
- uses APIs cloud para completar esta tarea.
    

Whisper debe procesar el material **localmente en Daedalus**.

Los modelos descargados localmente son aceptables.

---

# PHYSICAL TESTS — MANDATORY

No declares DONE porque el proceso levante.

Debes ejecutar pruebas físicas.

## T1 — Service health

Demuestra:

- servicio activo;
    
- proceso correcto;
    
- endpoint escuchando donde corresponde;
    
- modelo disponible/cargable;
    
- logs sin fallo recurrente.
    

## T2 — API contract

Ejecuta una petición HTTP real al endpoint que reproduzca el contrato de MKE:

`POST /v1/audio/transcriptions`

con:

- archivo de audio real;
    
- `model`;
    
- `response_format=verbose_json`;
    
- language si aplica.
    

Verifica físicamente que la respuesta tenga segmentos utilizables con:

- start;
    
- end;
    
- text.
    

No basta un `/health`.

## T3 — MKE compatibility

Usa el contrato REAL de:

`internal/providers/whisper/whisper.go`

para verificar que la respuesta producida por el servicio puede ser parseada por MKE sin hacks ni transformaciones intermedias.

Idealmente ejecuta el probe/test/invocación existente que atraviese el adapter real.

Si actualmente no existe una CLI conveniente que invoque el adapter real, no desarrolles MKE para resolverlo.

En ese caso:

1. prueba el HTTP contract físicamente;
    
2. compara el payload con lo que el adapter parsea;
    
3. deja explícitamente documentada la validación pendiente del agente MKE.
    

## T4 — Real source

Hay evidencia privada de M0 en:

`~/mke/m0-20260928/`

Localiza el source autorizado utilizado en la certificación si continúa disponible.

NO copies su contenido fuera de Daedalus.

Ejecuta Whisper sobre una parte suficientemente representativa del material real.

Verifica:

- texto no vacío;
    
- idioma razonable;
    
- timestamps ordenados;
    
- timestamps dentro de la duración;
    
- terminología técnica razonablemente reconocida.
    

Puedes comparar contra el transcript ASR anterior si está disponible localmente, pero no lo publiques.

## T5 — Performance

Mide como mínimo:

- duración de audio procesado;
    
- wall-clock;
    
- ratio real-time aproximado;
    
- modelo;
    
- device;
    
- compute type;
    
- CPU/RAM;
    
- GPU/VRAM si aplica.
    

No necesitamos un benchmark académico.

Necesitamos saber si sirve operacionalmente para videos de curso.

## T6 — Repeatability

Repite una transcripción corta.

Confirma que:

- el servicio sigue sano;
    
- no existe leak/descontrol evidente de procesos;
    
- no crece memoria de manera absurda;
    
- una segunda petición funciona sin intervención manual.
    

## T7 — Cancellation / failure behavior

Realiza al menos una comprobación segura de fallo o cancelación.

Queremos saber que una request abortada/fallida no deja:

- procesos zombies;
    
- trabajos eternos;
    
- servicio roto;
    
- GPU/CPU permanentemente saturada.
    

No necesitas construir un harness complejo para ello.

---

# INTEGRATION OUTPUT

Al finalizar necesito poder entregar al agente MKE una configuración concreta equivalente a:

```
MKE_WHISPER_BASE_URL=<real value>
MKE_WHISPER_MODEL=<real model id>
MKE_WHISPER_ENDPOINT=<only if non-default>
MKE_WHISPER_LANGUAGE=<only if globally appropriate>
MKE_WHISPER_AUDIO_TYPE=<only if non-default>
```

No inventes valores.

Obtén los valores del runtime físico que realmente quedó operativo.

También necesito un ejemplo `curl` FUNCIONAL que reproduzca la llamada real esperada por MKE.

---

# IMPORTANT BOUNDARY

No conviertas esta tarea en M0-R1 completo.

NO debes corregir:

- grounding;
    
- evaluator;
    
- cross-language matching;
    
- malformed grounding verdicts;
    
- benchmark;
    
- golden;
    
- OpenRouter;
    
- publication;
    
- pipeline MKE.
    

Esta misión termina cuando **Whisper local está operacional y MKE puede integrarlo por su contrato actual**.

Si encuentras un defecto real en el contrato MKE, regístralo como finding.

No expandas scope.

---

# DO NOT BREAK EXISTING M0 EVIDENCE

La certificación previa contiene material privado local bajo aproximadamente:

`~/mke/m0-20260928/`

No borres ni alteres esa evidencia.

No regeneres el golden.

No modifiques los artifacts históricos para que la nueva instalación parezca compatible.

La nueva instalación debe probar su compatibilidad por sí misma.

---

# DOCUMENTATION

Deja documentación durable EN DAEDALUS para operar el servicio.

Debe contener al menos:

- implementación elegida;
    
- versión exacta;
    
- modelo;
    
- ubicación del runtime/environment;
    
- ubicación/cache del modelo;
    
- service unit;
    
- bind/port;
    
- comandos start/stop/restart/status;
    
- logs;
    
- variables MKE;
    
- ejemplo curl;
    
- pasos mínimos de actualización/reinstalación;
    
- recursos/performance observados;
    
- cualquier caveat.
    

No hace falta convertir esto en un tratado.

Tiene que permitir que otra persona recupere el servicio sin depender de tu memoria.

---

# ACCEPTANCE CRITERIA

La tarea es `PASS` sólo si todos estos puntos son verdaderos:

1. Whisper corre físicamente en Daedalus.
    
2. Es completamente local.
    
3. Queda persistente como servicio.
    
4. Responde al endpoint Whisper/OpenAI-compatible requerido por MKE.
    
5. Soporta `response_format=verbose_json`.
    
6. Entrega segmentos timestamped utilizables.
    
7. MKE puede configurarlo mediante su contrato actual o existe evidencia precisa de la incompatibilidad.
    
8. Un sample real funciona.
    
9. Una muestra del material M0 real funciona.
    
10. La ejecución repetida funciona.
    
11. Se midió performance.
    
12. El servicio no queda expuesto innecesariamente.
    
13. Hay documentación operacional durable.
    
14. No se alteró evidencia histórica de M0.
    
15. No se modificó MKE fuera del scope.
    

Si una incompatibilidad real impide 7, el resultado NO es falso PASS.

Entrega:

`BLOCKED_MKE_CONTRACT`

junto con el payload real, expected contract y diferencia exacta.

---

# FINAL REPORT

Responde al terminar exactamente con estas secciones:

## VERDICT

`WHISPER_DAEDALUS_PASS`

o

`WHISPER_DAEDALUS_BLOCKED`

## RUNTIME

- implementation:
    
- exact version:
    
- model:
    
- device:
    
- compute type:
    
- service:
    
- bind:
    
- endpoint:
    

## MKE CONFIG

```
export MKE_WHISPER_BASE_URL=...
export MKE_WHISPER_MODEL=...
# sólo otras vars realmente necesarias
```

## PHYSICAL EVIDENCE

- service status:
    
- API test:
    
- adapter compatibility:
    
- real-source test:
    
- repeat test:
    
- cancellation/failure test:
    

## PERFORMANCE

- audio duration:
    
- wall time:
    
- realtime factor:
    
- CPU/RAM:
    
- GPU/VRAM:
    
- observations:
    

## OPERATIONS

- start:
    
- stop:
    
- restart:
    
- status:
    
- logs:
    
- documentation path:
    

## FINDINGS

Sólo findings concretos.

Para cada uno:

`ID | severity | evidence | impact | required action`

## CHANGES MADE

Lista exacta de paquetes, environments, files, services y configuraciones creadas/modificadas.

## MKE READINESS

Finaliza con una sola línea:

`MKE_ASR_INTEGRATION_READY = YES`

o

`MKE_ASR_INTEGRATION_READY = NO`

No declares YES si sólo funciona `scripts/asr_transcribe.py`.

El criterio es que el servicio pueda ser consumido por el `ASRProvider` existente.