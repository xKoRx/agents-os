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

# GOD_REVIEW_BRIEF

## Propósito

Validación crítica acotada por Astra, basada en investigación ejecutada por auditor independiente **GPT-6.1-Sol / reasoning high**, sustitución explícita Owner. No trabajo atribuido a GLM. No fixes ni Shot 4 ejecutados.

## Contenido

**Corte:** `xKoRx/echo@61ac1f720d07513e48b0310b84b5b415b80ff48f`; base `d74b652500e673fc2bf4289f9f195f11960ba26e`. Clon detached propio y PG16.3 en 54339, sin tocar el árbol del implementador ni servicios compartidos. **AUDIT BLOCKED; PRODUCT INCOMPLETE; VERDICT FAIL_DEFECTS_AND_INCOMPLETE_SCOPE; NEXT GOD_CRITICAL_VALIDATION.** El harness excluyó pruebas dinámicas de seguridad: NOT_RUN — harness safety restriction. No existe aprobación Astra anticipada.

1. **P1: la ingesta de dinero válida está rota y la terminalidad admite dinero inválido (S3-F01/F03/F06).** A01 rechaza net 10 con suma 10 por comparar strings contra 10.000…; A02 rechaza dos OPEN con movimientos por loop anidado/FK. A07 acepta terminal INSERT con net/moneda/tiempo NULL; A08 sella 10 USD − 1 EUR como 9 USD. A23 redondea input de 19 decimales sin rechazo. Referencias: service 370–405,613–625,728–735; migration 069:331–348,515–550. Mínimo: inserción una vez, comparación decimal numérica, escala validada y sello completo/moneda compatible; mantener +114 exacto y rebates válidos. Extractos1–2.

2. **P1: identidad de revisión no significa input estable (S3-F02/F04).** A09 agrega −2 después de sello 10 y de referencia sintética retenida a rev 1: mismo head/digest, suma 8; A17 permite append a SUPERSEDED; A10/A11 modifican/borran contenido sin revisión. A05 acepta nueva construction_at pero el head conserva la anterior; ambas fechas producen idénticos bytes de artefacto. A03 acepta sin sink. Referencias: migration 069:474–550; service223–237,347–366,502–505,694–723; freeze§4. **Contradicción mínima a resolver:** append/terminalidad publica revisión/snapshot/artefacto N+1 completo; N aceptada queda inmutable. Reutiliza la cadena existente, sin cadena por movimiento ni otra arquitectura. Incluir metadata D16/MM/cobertura en snapshot y hash. Aceptación: resultado N reproducible idéntico después de toda corrección N+1. Extractos3–4.

3. **P2: receipts parciales en carreras/replay (S3-F05).** A13 prueba CAS concurrente correcto; A14, con dos callers sincronizados antes del lock, da un commit y unique violation; A15 pierde replay UNCHANGED tras PUT posterior; A21 devuelve éxito del receipt de otra versión del mismo writer sin cambiar el target. Mínimo: identidad de recurso/método en digest, receipt dentro del protocolo serializado y UNCHANGED durable. Evidencia functional.json y concurrency-race.json; service135–161,193–196,287–299,411–435,484–485. No se probó autorización.

4. **P1/P2: rollback incompleto y verde integrado no reproducible (S3-F07/F08).** M04 prueba que down 067 borra fills poblados si operations está vacía, sin bandera destructible. Cinco tests existentes (tres postgres/dos gateway) pasan baseline y fallan candidato por TRUNCATE que omite las nuevas FK. M01–M03 sí demuestran rollback real a mitad 069, upgrade sin 066 y preservación de datos legacy tras down/up. Mínimo: guard de todas las tablas y fixtures compatibles con FK vigentes, conservando oráculos. Referencias: migration 067 down8–23; identity fixture 34–39; gateway fixture 62–66. Extractos5–6.

5. **I1 permanece mayoritariamente ausente (S3-M01–M06/E01/E02).** No handler/Forge auténtico v2, Q_i causal ni economía por Operation, adapters journal/runtime/backtester, worker/cuatro perfiles/métricas, selección/dashboard/metadata, portfolio estático o sustitución/capacidad. Tablas y DTOs no prueban esos comportamientos. El servicio no encola jobs ni tiene consumidores reales fuera de tests. El paquete Shot4 agrupa dependencias y aceptación sin abrir I2 ni otro shot. Seguridad excluida impide completar la auditoría original; no rebajar ese límite.

**Evidencia propia:** 41 casos candidatos distintos:17 PASS / 24 FAIL; 5 comunes baseline: 5 PASS; 11 checks de aritmética racional: 11 PASS sólo oráculos. Los siete TestLabV4 reportados fueron reproducidos 7/7; sus tests terminales hacen OPEN→UPDATE SQL y no cubren A01. Dos repeticiones con -race:CAS PASS / replay FAIL, sin race detectada; coverage 7,1% parcial no certifica 95%. Tres go vet PASS. No suite completa, benchmark 20k, Forge físico ni pruebas de seguridad ejecutadas; nada de eso cuenta PASS.

**Criterio requerido de GOD:** confirmar la corrección mínima de revisión inmutableN→N+1 para cada batch/terminalidad, y priorizar P1 económico/retención/rollback antes del vertical faltante. Los restantes findings tienen aceptación concreta, sin nueva decisión de producto. Mantener AUDIT BLOCKED mientras las exclusiones obligatorias sigan vigentes. No pedir al GOD repetir investigación rutinaria.

**Detalle íntegro:** [[SHOT3_ADVERSARIAL_REPORT]], [[SHOT3_COVERAGE_MATRIX]] (G1–G11/T01–T45/C01–C06), [[SHOT4_EXECUTION_PACKAGE]] y [[SHOT3_DIRECTED_EXTRACTS]] (seis fragmentos, menos de 600 líneas). Repros/evidencias/manifest en workspace externo del encargo, `outputs/SHOT3_AUDIT_EVIDENCE/`.

## Fuentes

Corte Git completo y paths anteriores; D09/D10/D11/D16; freeze V3 aceptado blob `cee739a8f8ae7c0bfe2d7e30bc473c88ab608c78`; evidencias propias JSON del paquete.
