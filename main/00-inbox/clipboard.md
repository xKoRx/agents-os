STATUS: `M1_DESIGN_FROZEN`

OWNER:

- OD-1: `APPROVED`
- OD-2: `APPROVED`
- OD-3: `APPROVED`

AUDIT:

- contradicciones materiales encontradas: ownership de cuenta simulada y alcance del gate de imports transitivos.
- correcciones finales: owner único, gate realizable, retención privada aprobada, alcance/M4 alineados y handoff actualizado. Auditoría documental aprobada; historial FABLE/ASTRA-2 preservado.
- blockers restantes: ninguno para M1/M2.

SCOPE:

- FOUNDATIONAL NOW: núcleo read-only/replay/shadow, simulación, persistencia, observabilidad y backup/restore local consistente y medido.
- IMPLEMENT LATER: live, capacidades opcionales, optimizaciones y DR off-host; contratos fundamentales definidos.

GATES:

- architectural contracts: `FROZEN`; se conserva `BLOCKED_BY_PROTOCOL` donde corresponde.
- physical tests: `NOT_RUN`.
- live: `NOT_CERTIFIED / LIVE_DISABLED`.

NEXT:

- M2 TOP implementation plan, sin rediseñar. Plan no redactado en este shot.