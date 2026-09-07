---
type: change_log
scope: project
created: 2026-08-04
updated: 2026-08-04
area: "[[Echo]]"
project: "[[Echo Forge - Cierre de Etapa 4]]"
entities:
  - "[[Echo Forge]]"
  - "[[Echo Forge - Cierre de Etapa 4]]"
  - "[[Echo Forge - Trade List Export Contrato Remoto]]"
source_session: codex-echo-forge-stage4-owner-repriorization-2026-08-04
indexable: true
index_priority: high
tags:
  - kind/changelog
  - project/echo-forge
  - area/echo
---

# Change log — Echo Forge Stage 4 owner reprioritization (2026-08-04)

## Qué cambió

- El owner deprecó `EF-G29` para este ciclo: los `.cfx`/flows actuales son fixtures de prueba y el próximo `config.json` corrige el instrumento. No se implementará ni validará un fix de identidad de chart.
- El owner difirió `EF-G31`: la trazabilidad release→plugin es deuda real de baja prioridad, pero no bloquea el cierre operacional actual.
- `EF-G28` queda resuelto por configuración existente: `05_reretester` con `reretester_test.cfx` se ejecuta después de `04_optimizer_robust` y TradeList ya consume ese `source_folder`; se descartó crear un pips retester adicional.
- Se confirmó `EF-G30` como requisito de integridad del smoke: los defaults del plugin contaminan `scope`, NDJSON y manifest aunque la activity no falle. Se debe completar `exporter.properties` con identidad real.
- `EF-G32` conserva su estado de implementación en Review y queda como precondición de deployment/smoke por su contrato remoto entre workers.
- Se incorporó `H2-PROMPT`, un despacho acotado que preserva Robust Run y EF-G32, excluye EF-G29/31, y exige evidencia de E2E y cuarentena no destructiva.
- Se validó la certificación posterior de Robust Run: código `994ffdb`, tareas 12–14, `VERIFICATION.md`, G6 y el proyecto coinciden en `CLOSED / PASS` sólo para ese subalcance. Posteriormente se comprobó `master` limpio en `8e2f2dd`, que ya contiene la documentación de certificación y es descendiente de `994ffdb` y `2f6708e`; por tanto el roadmap operativo parte directamente en EF-G30 → EF-G32 → smoke → cuarentena.
- Se retiraron de las instrucciones vigentes de EF-G32 los bloqueos ya superados (`EF-G28/29/31`): el plan de ejecución y su verificación E2E ahora parten explícitamente en EF-G30. Las menciones de la investigación anterior se conservaron sólo cuando están rotuladas como contexto histórico.

## Artefactos actualizados

- [[Echo Forge - Cierre de Etapa 4]] — estado, tareas, bitácora y prompt H2.
- [[Echo Forge - Trade List Export Contrato Remoto]] — dependencias operacionales y precondiciones E2E.

## Límites

- No se modificó código, configuración de Symphony, artefactos SQX ni infraestructura.
- No se declaró cerrada la Etapa 4.
