# REPAIR-LOG — ch02-time · remediación P1–P10 (2026-10-18)

Mandato del Owner tras revisar la biblioteca publicada. Sin re-procesar el video,
sin re-extraer claims, sin renumerar IDs, sin ASR. Baseline congelado en
`REPAIR-BASELINE.json` (todas las cifras del Owner reproducidas 1:1 desde los
archivos publicados).

## Acciones

### P5 (validador) — primero, para capturar RED
- `course-knowledge-extraction/scripts/validate_library.py` (checks V01–V13) +
  `validate_review.py` (R01–R04) + `make_minute_payload.py` (contexto de
  frontera) + `tests/fixtures_selftest.py` (10 casos red-green).
- RED contra la biblioteca pre-reparación: V07×27, V08×38, V05 (f-170903),
  V10 (README 14/13/11 vs 16/17/11), V11×5 (nombres históricos).

### P1 (provenance visual) — 3 workers ONE-SHOT, verificación física
- 41 claims auditados (27 visual_observation ∪ 38 visual_hint; cada frame leído
  por el worker antes de adjuntarse).
- Resultado: 23 visual_observation con frame en `evidence`; 17 reclasificadas a
  `instructor_statement` en P1 (+c-0066 adjudicada en P4 = 18 en total); de las
  18, 13 conservan frames verificados como contexto y 5 quedan sin frame
  (c-0031, c-0045, c-0055, c-0059, c-0070), cada una documentada en su nota
  (c-0059: f-000926 leído y descartado, no resuelve el deíctico "este low o
  este"; c-0070: f-001104 y f-001110 no muestran el solape).
- 48 referencias f- estructuradas (antes 0). 0 cambios de veredicto: ningún
  SUPPORTED se preservó por comodidad — los visuales indemostrables resultaron
  ser hablados.
- Frames nuevos (naming por fórmula): f-000440, f-000735, f-001110 (este último
  extraído para auditar c-0070 y NO adjuntado al no soportar el statement).

### P2 (naming)
- f-170903.png → f-001703.png (parseaba 17h09m > duración); referencias
  actualizadas. Los 5+1 nombres históricos declarados en
  `.deprecated_frame_names` (un `historical_invalid_name` en los .md es registro
  de auditoría, no cita vigente; el validador los distingue).

### P3 (reporting)
- README reconciliado contra artefactos: rules 16, concepts 17, examples 11;
  frames 18+47=65; referencias visuales sin resolver 0.
- Wall time: OWNER_OBSERVED_ELAPSED = 2h06m (autoridad para el total);
  AGENT_RECONSTRUCTED_ELAPSED ≈ 1h40–1h50 (02:54–04:35 desde mtimes/epoch).
  Diferencia: ventana de observación del owner (inicio/lectura/cierre de sesión)
  vs tramo medido por el agente + overhead de orquestación; se reportan ambas,
  no se sobrescribe ninguna. Tramos: ASR 45,1 min · extracción 8,6 · revisión
  19,8 · integración+publicación ~20 (primera pasada) / ~35 (remediación).

### P4 (semántica)
- c-0066 → **A**: el condicional DXY es proyección hablada del instructor
  (s-001005/s-001010 verbatim) → `instructor_statement`, SUPPORTED por fidelidad
  textual; f-001030 adjunto como contexto del low candidato, no como prueba de
  la proyección.
- c-0056 → **RESOLVED** (región 07:58–08:06): f-000758 (primera caja en curso,
  ancla ~1,5803) vs f-000806 (rango válido persistente 1,4748–1,5803, velas
  17–20 jun en 8H). Identificación del rango válido: alta; del rectángulo
  descartado: borde inferior (~zona 1,52) leído de un still en pleno dibujo —
  matiz conservado en la nota del claim.
- TIMEZONE: c-0012 preserva "New York = UTC-4" como contenido del curso con
  attribution; no se añadió precisión editorial sobre DST (no requerida).

## Contract tests (P9) — evidencia de ejecución

| Caso | Mecánica | Resultado |
|---|---|---|
| A — visual sin frame | fixture `bad-visual-no-frame` → V07+V08 FAIL; base con frame → PASS; biblioteca real: RED 27/38 → GREEN | PASS |
| B — nomenclatura | fixture `f-124400.png` → V05 FAIL; histórico sin declarar → V11 FAIL; declarado en `.deprecated_frame_names` → PASS; real: f-170903 → f-001703 | PASS |
| C — payload de frontera | `make_minute_payload.py` sobre claims reales: minuto 11 incluye s-001201 (c-0067); minuto 12 incluye s-001300+s-001304 (c-0072) | PASS |
| D — cardinalidad reviewer | fixture 8 claims / 7 verdicts → `MINUTE_REVIEW INVALID` (R01); 8/8 → VALID | PASS |
| E — model_inference SUPPORTED | fixture → V13 FAIL (requiere adjudicación); c-0066 real re-adjudicado | PASS |
| F — reporting README 14 vs 16 | fixture V10 FAIL; real: (14,13,11) vs (16,17,11) detectado en RED y reconciliado | PASS |

`fixtures_selftest.py`: 10/10 PASS. Validador sobre biblioteca reparada:
`LIBRARY_VALIDATION = PASS` (findings=0).

## P6/P7/P8 (skills)
- Main skill v1.1: 7 contratos nuevos integrados (evidencia, frontera, naming,
  densidad, glosario, checkpoint doble, validación final) + sección de scripts +
  referencia al worker skill.
- Nueva `course-knowledge-worker/SKILL.md` (EXTRACTOR / MINUTE_REVIEWER /
  DOCUMENTATION_VERIFIER, contrato común, spool-only) registrada en
  `80-agents/skills/INDEX.md` (federadas 18→19).

## P10
Revisión independiente ONE-SHOT sobre los 10 puntos del mandato: ver
`review-notes.md` y el handoff de la sesión (findings y correcciones in-mission
quedan registrados aquí si los hubo).

## Estado post-reparación

CLAIMS = 98 (IDs preservados) · veredictos 98 SUPPORTED · visual_observation 23
(23/23 con frame) · visual_hint 38 (36 con frame; 2 sin frame — c-0059 y
c-0070, instructor_statement con hint contextual documentado en la nota)
material documentado) · refs f- estructuradas 48 · frames 65 (18+47) ·
LIBRARY_VALIDATION = PASS · Chapter 01 intacto.
