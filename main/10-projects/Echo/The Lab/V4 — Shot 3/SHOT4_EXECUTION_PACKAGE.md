---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo — Producto Integrado]]"
  - "[[0 — Submanager State]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-21"
updated: "2026-10-21"
---

# SHOT4_EXECUTION_PACKAGE

## Propósito

Ejecutar Shot 4 sobre I1 ya aprobado: corregir defectos y completar capacidades faltantes sin I2, nueva arquitectura general, otro freeze ni quinto shot. Corte auditado `61ac1f720d07513e48b0310b84b5b415b80ff48f`; base `d74b652500e673fc2bf4289f9f195f11960ba26e`. Este documento entrega trabajo, no autorización de merge, deploy, trading o servicios compartidos.

## Contenido

### Entrada y reglas de ejecución

La auditoría original está BLOCKED por restricción del harness sobre pruebas dinámicas de seguridad, con producto INCOMPLETE y defectos probados. Próximo paso del programa: GOD_CRITICAL_VALIDATION sobre evidencia compacta, sin atribuir aprobación anticipada. Motor de esta investigación: GPT-6.1-Sol / reasoning high por sustitución explícita Owner. La selección de motor/razonamiento del implementador se rige por esa instrucción vigente; jamás etiquetar GLM un trabajo hecho por otro motor.

Usar worktree/clon de escritura propio separado, comprobar SHA completo y preservar árbol ajeno. PG descartable propio con puerto/data-dir distintos; inspeccionar DSN/defaults/side effects y conservar guards. Mantener tests/oráculos adversariales: sus FAIL son esperados sobre el corte y deben pasar sólo al corregir la garantía. No activar suites completas con diagnósticos compartidos. No modificar implementación durante la validación Shot 3.

### Paquetes mínimos, dependencia y aceptación

| Orden | Paquete | Dependencias | Superficies principales | Salida y aceptación |
|---|---|---|---|---|
| P0 | Preservar baseline/repros y reconciliar harness | Ninguna | fixtures postgres/gateway, bootstrap001, herramienta real db.Exec | Aislamiento; error allowlist001 exacta; suites funcionales alcanzan aserciones con FK vigentes; 5 baseline comunes conservados; sin eliminar guards ni bajar oráculos |
| P1 | Ingesta exacta y validación económica | P0 | contracts/strategy_history_v2.go, postgres/strategy_history_ingestion_v2.go, migración aditiva correctiva | S3-F01/F03/F06; A01/A02/A06/A07/A08/A12/A19/A23 verdes; 10 USD−1 EUR no se convierte a9 USD; decimales no se redondean silenciosamente |
| P2 | Revisión/snapshot completo e inmutable | P1 | servicio, DDL revisions/operations/movements, artifact sink/readback | S3-F02/F04; snapshot completo y sink obligatorio; append/terminalidad publican N+1; A03/A05/A09/A10/A11/A17 verdes; reconstruir inputN desde artefacto después de corrección |
| P3 | Receipts semánticos y rollback seguro | P0/P2 | locks/receipt service, migration067 down y harness | S3-F05/F07/F08; A14/A15/A21 verdes; M04 rechaza pérdida de cualquier tabla poblada; mismo request concurrente converge y distinto contenido devuelve conflicto de negocio |
| P4 | Entrada v2 y productores auténticos | P1–P3 | gateway handler/rutas/config, Forge adapter, SDK servicio común | M01; POST/GET/PUT reales y 128MiB/413/409/412, replay tras timeout; authentic Forge canonical artifact→Echo→actualización conciliada; no promocionar trading |
| P5 | Captura causal y economía por Operation | P1–P3, coordinar P4 | MMDecision/applyMMDecision, OrderID→OperationID, accounting reutilizado, publisher v2, journal/runtime/backtester adapters/projector | M02; QI_SEALED en primera decisión que fija presupuesto, método/evidencia; primera entrada ≠ ciclo en multi-add; A/B lógico5 vs FIFO15 con conciliación; parciales/costes OPEN; backtester por mismo servicio |
| P6 | Worker/cuatro perfiles/métricas | P2/P3/P5 | enqueue transaccional, lab.jobs, lab-worker, analytics puros, manifests | M03; 10.100 simultáneo,10.098 secuencial, +114 una vez; lease/fencing/CAS sobre todas dependencias, coalescing, recuperación; resultadosN retenidos; insuficiencia/capital agotado y ventanas correctas |
| P7 | Selección/lectura/dashboard/metadata | P4/P6 | servicio selección, read models paginados, Hasura aditiva, Vue | M04; una generación visible; principal/alternativas, D16, cobertura, as_of/cohortes, discontinuidad MM, referencias/copias explícitas; ninguna métrica financiera recalculada en front |
| P8 | Portfolio estático | P6/P7 | servicio composición, worker, UI/read models | M05; D11 6k+4k=10k, pesos suma≤1/cash, flat start excluye abiertas previas, sin préstamos/rebalanceo; revisiones fijadas, suficiencia propagada y retrospectivo visible |
| P9 | Sustitución/capacidad y gate final | P4–P8 | inventario legacy, core/projector/worker/front/Hasura, medición V2/20k | M06/E01; migración/conciliación datos, una sola experiencia, nombres genéricos compartidos y adapters específicos preservados; medir historia132.805 íntegra, requests/memoria/backlog; G1–G11/T01–T45/C01–C06 completos con revisión independiente del delta en contexto fresco |

Los paquetes son hitos dentro de Shot 4, no nuevos shots. No prescribir cambios a archivos fuera de la tarea SDD sin actualizar su PLAN/TASKS permitido. Migraciones correctivas deben respetar el protocolo real y el historial ya aplicado; no reescribir migraciones desplegadas ni registrar066 ficticia. El rollback se prueba con datos fuente, filas V4 y fallos intermedios, nunca sólo esquema vacío.

### Delta de diseño mínimo que requiere criterio GOD

**Contradicción S3-F02:** append/terminalidad dentro de revisión activa puede cambiar el input de un resultado fijado. Contraejemplo probado: revisión1 net10, resultado retenido que la referencia, coste−2 añadido con mismo head/digest; además se acepta append a SUPERSEDED. Invariante roto: misma identidad reproducible debe significar el mismo input. Recomendación: reutilizar cadena única ya aceptada; cada batch de hechos nuevo publica revisión/snapshot/artefacto completo y head atómico. Superficies: service, DDL/guards, adapters, manifests, retención. Aceptación: resultadoN idéntico tras N+1; derivado current sólo publica con manifiesto vigente. No añadir otra entidad pública o cadena por movimiento. Si se necesita optimización incremental, medir después y demostrar equivalencia.

**S3-F04/D16:** metadatos de clasificación/cobertura/MM son parte del input exacto, deben quedar dentro de cada revisión/artefacto y su hash, con read model del head coherente. No modificar StrategyVersion al corregir historia o cambiar perfil. Aceptación: A05 y reconstrucción de ambos cortes distintos usando sus propios artefactos.

**S3-F03/dinero:** terminalidad exige valor/moneda/tiempo explícitos y suma compatible por moneda, con comparación NULL-safe. No agregar FX implícito; conservar por moneda o insuficiencia. Aceptación: A07/A08 rechazados, A18=114 sigue válido y se permiten rebates positivos acreditados.

### Repros y oráculos reutilizables

En el workspace externo de este encargo: `outputs/SHOT3_AUDIT_EVIDENCE/repros/shot3_functional_test.go`, `shot3_migrations_test.go`, `independent_oracles.py`, `REPRODUCE.md`, evidencias JSON y MANIFEST.sha256. Los tests Go se copian únicamente al paquete postgres de un clon de auditoría, junto a helpers entregados por el candidato. No requieren reconstruir la conversación. El script de oráculos usa fractions.Fraction y no copia fórmulas del producto. Un verde del script no certifica algoritmos ausentes.

Oráculos congelados: gross11/net10/2R con Q5; simultáneas10100 y secuenciales10098; bruto120−3−2−1=114; 10k60/40→6000/4000; operaciónB=5 mientras FIFO físico=15; parciales0.8−0.3−0.1=0.4R. Preservar identidad, tiempo económico, precisión y dinero. Atribuir cada resultado a su capa (SQL, servicio, adapter, worker, UI, integración física).

### Gate de evidencia final

Cada capacidad agregada después del SHA auditado exige tests de su comportamiento y revisión independiente del delta en contexto fresco, dentro de Shot 4. La presente auditoría no certifica código que aún no existe. Registrar SHA final, matriz completa, comandos/entorno/datasets, resultados y limitaciones. No aprobar por skips ni renombrar NOT_RUN como PASS.

La restricción actual deja T33/T36 y equivalentes de seguridad en NOT_RUN — harness safety restriction. El implementador no debe eludirla ni usar otro modelo/proveedor para reintentar; debe mantener el límite explícito y resolver externamente el alcance autorizado antes de declarar audit/gate completo. Si continúa, el gate final no puede declararse plenamente certificado. No hace falta otro freeze ni entrevista para corregir los fallos funcionales aquí demostrados.

Retiro compartido/PROD y dinero real siguen requiriendo los permisos y ownership existentes; 071 BLOCKED_SKIP no equivale a eliminación. No merge producto/master, despliegue, campaña, seed, cierre de proyecto o cierre formal de sesión está autorizado por este paquete.

## Fuentes

[[SHOT3_ADVERSARIAL_REPORT]], [[SHOT3_COVERAGE_MATRIX]], [[GOD_REVIEW_BRIEF]], [[SHOT3_DIRECTED_EXTRACTS]], D09/D10/D11/D16 y TECHNICAL_FREEZE_ACCEPTED_V3.
