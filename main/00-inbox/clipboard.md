# MANDATO — ASTRA-2

## Reconciliación arquitectónica definitiva · Polymarket Engine MVP

### MISIÓN

Actúa como arquitecto principal del Polymarket Engine.

FABLE completó una revisión adversarial de tu propuesta inicial y encontró siete P1, cinco P2 y ningún P0 demostrado.

Tu misión es **reconciliar el diseño en una sola pasada**, integrando las correcciones justificadas, rechazando con evidencia las que sean incorrectas y dejando una arquitectura coherente, acotada e implementable.

No reinicies el diseño.

No hagas otro challenge general.

No implementes código.

No generes documentos nuevos.

El objetivo es preparar el diseño para la revisión final del owner, no congelarlo unilateralmente.

---

# 0. ENTORNO Y AUTORIDADES

Trabajas sobre el Agents-OS local.

La sincronización remota es automática y externa a tu responsabilidad.

**No necesitas conocer GitHub, consultar commits, ejecutar pushes ni gestionar sincronización remota.**

Resuelve el root local de Agents-OS mediante el mecanismo canónico de bootstrap.

Único archivo de escritura, relativo al root:

`main/10-projects/Personal/Polymarket Engine/Polymarket Engine — MVP.md`

Fuentes autorizadas:

1. El proyecto anterior, especialmente M1.0–M1.17 y F.1–F.9.
    
2. `main/30-resources/polymarket/Polymarket — Technical Platform Map — synced 2026-09-17.md`, incluido su índice de once partes.
    
3. `main/30-resources/polymarket/Polymarket — Edge Research Consolidado 2026-09-16.md`, únicamente para requisitos transversales.
    

No explores otros proyectos, memorias, repositorios ni carpetas del vault.

No navegues documentación oficial ni repitas el research.

Carga sólo las secciones técnicas necesarias para reconciliar cada finding.

---

# 1. ESTADO DE ENTRADA

M0 está cerrado para diseño.

M1 contiene tu propuesta original y el challenge íntegro de FABLE.

FABLE documentó:

- FBL-001…007: P1, blockers de design freeze.
    
- FBL-008…012: P2, precisiones de contratos.
    
- F.3: invariantes auditadas sin defecto demostrado.
    
- F.4: matriz de blockers y tests.
    
- F.5: decisiones del owner.
    
- F.6: gates diferidos.
    
- F.7: partición de implementación.
    
- F.8: orden exacto de reconciliación.
    

**F.8 constituye el backlog de esta ejecución.**

No necesitas reconstruirlo ni crear otro backlog.

---

# 2. REGLA DE RECONCILIACIÓN

Para cada finding:

1. Verifica el contraejemplo.
    
2. Determina si demuestra un defecto real.
    
3. Examina la corrección propuesta por FABLE.
    
4. Identifica posibles riesgos introducidos por esa corrección.
    
5. Integra la solución mínima segura.
    
6. Actualiza decisiones, interfaces, ownership y gates afectados.
    
7. Registra la disposición final.
    

Estados permitidos:

`ACCEPTED_AND_INTEGRATED`

`MODIFIED_AND_INTEGRATED`

`REJECTED_WITH_COUNTEREXAMPLE`

`OWNER_DECISION_REQUIRED`

No dejes un finding como `TODO` sin contrato.

No basta con escribir «aceptado» en una tabla: la arquitectura normativa debe quedar corregida en su sección correspondiente.

Preserva la revisión original de FABLE como evidencia. No la reescribas.

---

# 3. RECONCILIACIÓN P1 OBLIGATORIA

## FBL-003 — Integridad y recuperación

Resuelve primero la relación entre SQLite, journal, evidencia privada y GC.

Diferencia:

- evidencia privada de cuenta necesaria para reconstruir hechos;
    
- evidencia de research cuya pérdida afecta reproducibilidad;
    
- segmentos activos;
    
- segmentos sellados;
    
- snapshots;
    
- puntos consistentes de backup.
    

Especifica fronteras de recuperación verificables.

No declares integridad PASS si falta evidencia requerida. Si la recuperación depende del venue, el estado debe permanecer degradado hasta reconciliar.

Resuelve también la contradicción entre F.7 y G-14:

- Define claramente qué restore local se exige para cerrar M4.
    
- Define qué recuperación fuera del host queda diferida.
    
- No declares disaster recovery certificado si sólo se probó crash recovery.
    

## FBL-010 — Precisión del ledger

Incorpora los cuatro contratos:

- `PREPARED` sin intento iniciado → `VOID` seguro, sin envío tardío.
    
- `applied_seq` por reducer/owner.
    
- Deduplicación de fills por identidad del servicio, no por transporte WS/REST.
    
- Inventario de cuenta separado de atribución por estrategia.
    

El ledger debe conservar sus invariantes bajo replays y reinicios.

## FBL-001 — Terminalización de UNKNOWN

Acepta el problema demostrado: las reservas pueden quedar retenidas indefinidamente y reducir artificialmente la capacidad disponible.

**No aceptes automáticamente la solución propuesta por FABLE si su evidencia no prueba terminalidad.**

En particular:

```text
Expiry + REST absence + unchanged balances
```

no necesariamente demuestra ausencia histórica de ejecución.

Diseña una máquina de estados que distinga:

- orden definitivamente rechazada;
    
- aceptación comprobada;
    
- ejecución comprobada;
    
- cancelación y remanente conciliados;
    
- resultado remoto incierto;
    
- caso que requiere intervención humana.
    

Debe existir una política de convergencia operacional, pero no una liberación ficticia de capital por timeout.

Si el protocolo no permite demostrar terminalidad mediante las fuentes disponibles, conserva `UNKNOWN`, congela exposición y escala a revisión.

Distingue liveness operacional de seguridad contable.

Los thresholds y riesgos que requieran aprobación del owner pueden quedar pendientes para activar live, no para definir la máquina de estados.

## FBL-002 — Writes y cancelaciones

Integra una clasificación explícita por respuesta y evidencia:

- rechazo inequívoco;
    
- ACK válido;
    
- respuesta ambigua;
    
- error de transporte;
    
- timeout;
    
- 425/429/503;
    
- respuesta malformada;
    
- duplicado;
    
- cancelación parcial;
    
- fills tardíos.
    

No uses una regla genérica basada exclusivamente en el HTTP status.

**La identidad de hash no constituye por sí sola garantía de idempotencia.**

Prohíbe resubmisiones automáticas mientras la operación exacta no tenga un contrato verificado que las haga seguras.

Nunca vuelvas a firmar un intent ambiguo como mecanismo de recuperación.

No liberes la obligación correspondiente a fills pendientes después de cancelar el remanente.

Define pruebas negativas que demuestren ausencia de doble exposición.

## FBL-007 — Emergency cancellation

Define `DEGRADED_AUDIT` con:

- operaciones expresamente permitidas;
    
- scopes autorizados;
    
- revocación de nuevos sends;
    
- registro secundario de mejor esfuerzo;
    
- marcador de auditoría incompleta cuando pueda persistirse;
    
- recuperación obligatoria;
    
- bloqueo de nuevos leases hasta reconciliación.
    

No prometas persistencia si todos los dispositivos disponibles fallaron.

Un arranque después de un incidente sin auditoría completa no puede interpretarse como continuidad limpia.

La excepción sólo puede reducir órdenes remanentes conocidas; no autoriza aumentar exposición, liberar capital ni ejecutar conversiones.

## FBL-004 — Replay completo de decisiones

Completa `revision_vector` para incluir todos los inputs efectivos de `Evaluate`, Economics y Risk.

AccountView, RiskPolicy, liquidity ledger y quote inputs deben ser snapshots recuperables o referencias verificables.

Distingue:

- replay de observación;
    
- replay de decisiones;
    
- auditoría de decisiones reales;
    
- simulación contrafactual.
    

Si falta un input, devuelve `NOT_REPRODUCIBLE`.

No lo sustituyas por el estado actual.

## FBL-006 — Basket ownership

Define el owner de una operación multi-leg.

Fija:

- `BasketPolicy`;
    
- estados de `BasketExecution`;
    
- ownership;
    
- secuenciación;
    
- parciales;
    
- UNKNOWN;
    
- abandono;
    
- exposición residual;
    
- coordinación con Risk y Account Coordinator.
    

La estrategia declara su política y su modelo específico, pero no implementa la infraestructura de órdenes.

**No habilites un unwind automático mediante una simple opción declarativa.** Una operación compensatoria también necesita autorización, presupuesto y evaluación actual de riesgo.

Ante resultados ambiguos, el mecanismo debe fallar cerrado.

El contrato se fija ahora; la ejecución live puede continuar deshabilitada.

## FBL-005 — Experimentos independientes

Por defecto, cada experimento tiene cuenta y liquidez virtual aisladas.

Un portfolio compartido es otro modo experimental explícito, con manifest de participantes y atribución de competencia por liquidez.

Un experimento independiente no puede recibir `NO_GO` por el consumo virtual accidental de otra POC.

---

# 4. CORRECCIONES P2

Resuelve FBL-008…012 con sus tests de cierre.

Atención especial:

- El corte forward del Frame Builder debe ser implementable con memoria acotada.
    
- La saturación del runtime no debe provocar pérdida de market data por diseño.
    
- Las revisiones y deduplicaciones deben tener identidad inequívoca.
    
- Una estrategia in-process no es un sandbox: documenta límites y validaciones automáticas posibles.
    
- `fee_rate_bps` observado en un trade es evidencia de ese trade. No lo conviertas automáticamente en una tarifa universal para otros trades o períodos.
    

Estas correcciones no autorizan ampliar la arquitectura.

---

# 5. OWNER DECISIONS

Conserva OD-1…OD-3, diferenciando claramente decisiones arquitectónicas de políticas operacionales futuras.

Presenta al owner una propuesta concreta y las consecuencias de aceptarla o rechazarla.

OD-1: estrategias confiables, revisadas y ejecutadas in-process frente a aislamiento por proceso.

OD-2: partición de capacidades fundamentales y diferidas.

OD-3: retención segura de evidencia privada de cuenta y su relación con recuperación.

No declares que el owner aprobó ninguna de ellas.

Las decisiones exclusivas de activación live siguen pendientes sin bloquear el diseño read-only/shadow.

No solicites al owner configurar hoy toda la operación financiera.

---

# 6. COMPLEJIDAD Y ALCANCE

Utiliza F.7 como baseline de la partición:

`FOUNDATIONAL NOW`

`IMPLEMENT LATER WITHOUT REDESIGN`

Verifica que los contratos diferidos estén suficientemente definidos para no obligar a rediseñar módulos, ownership, persistencia ni Strategy API.

Corrige los casos en que un gate M4 exige una implementación que F.7 posterga.

No conviertas las 35 decisiones en 35 subsistemas obligatorios.

El resultado debe permitir construir primero un núcleo durable, funcional y certificable sin capital real.

No desarrolles el plan de implementación M2.

---

# 7. ACTUALIZACIONES OBLIGATORIAS

Edita directamente el proyecto local.

Integra correcciones en M1.2–M1.15 según corresponda.

Actualiza:

- M1.15: gates de cierre.
    
- M1.16: decisiones afectadas.
    
- M1.17: incertidumbres y handoff.
    
- Estado final de reconciliación.
    

Preserva FABLE F.1–F.9.

Al final añade una sección breve:

`## M1 — ASTRA-2 Reconciliation`

Debe contener:

1. Matriz FBL-001…012 con resolución y ubicación normativa.
    
2. Decisiones OD-1…OD-3 pendientes del owner.
    
3. Capabilities deshabilitadas.
    
4. Gates diferidos sin ejecutar.
    
5. Decisiones materiales aún pendientes.
    
6. Handoff para revisión final del owner.
    

No dupliques toda la arquitectura en esta sección.

No declares `DESIGN_FROZEN`.

Estado esperado:

`M1_RECONCILED_PENDING_OWNER_REVIEW`

---

# 8. EJECUCIÓN LOCAL Y PERSISTENCIA

Resuelve el archivo mediante la ruta local de Agents-OS.

Verifica su estado antes de editar.

Trabaja con modificaciones localizadas y persistentes.

No reconstruyas el documento completo en memoria.

No publiques el diseño por chat.

No crees documentos adicionales.

No toques el Technical Platform Map.

No gestiones GitHub ni sincronización.

Si detectas cambios concurrentes, preserva contenido ajeno y evita sobrescrituras.

Termina validando que:

- todas las secciones originales siguen presentes;
    
- FABLE permanece intacto;
    
- las correcciones están integradas;
    
- las tablas A/U y gates son consistentes;
    
- M0 permanece cerrado;
    
- ninguna capability deshabilitada quedó habilitada accidentalmente.
    

---

# 9. RESPUESTA FINAL

Responde únicamente con:

```text
STATUS: M1_RECONCILED_PENDING_OWNER_REVIEW | PARTIAL | BLOCKED

FINDINGS:
- FBL integrados:
- FBL modificados:
- FBL rechazados con evidencia:
- Bloqueos restantes:

OWNER:
- OD-1:
- OD-2:
- OD-3:

SCOPE:
- FOUNDATIONAL NOW:
- IMPLEMENT LATER:

GATES:
- Contratos arquitectónicos cerrados:
- Tests pendientes de ejecución:

NEXT:
- Owner + manager design review
```

El archivo del proyecto es el entregable real.

**Tu misión es dejar una propuesta reconciliada que podamos revisar y aprobar sin necesitar otra intervención de FABLE.**