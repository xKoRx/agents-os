# OWNER-DECISION-P7C — RESUELTA (sucesora del paquete de opciones)

Fecha: 2026-10-06 · Autoridad: Owner (resolución explícita entregada al Manager de migración) · Sucesora de: `acceptance-campaign/remediation-2/OWNER-DECISION-P7C.md` (paquete de opciones A/B/C, queda como historia intacta).

## Decisión

```text
Option A (esperar retorno stealth) = SUPERSEDED
Option B (modelo sucesor re-certificado + re-baseline) = SELECTED
Option C (congelar P7b con waivers) = REJECTED

Selected provider = Z.AI (adapter canónico: zai)
Selected model    = glm-5.3-flash (multimodal; glm-5.3 text-only descartado por requisitos visuales de Chapter 01)
Reason            = endpoint stealth/space-bunny-alpha retirado >24h (404 "No endpoints found", 2 watchers con 96/96 probes 404 cada uno)
```

Credencial: provista por el Owner para esta corrida; instalada en env protegido externo al repo/vault (`~/.config/mke/zai.env`, chmod 600) cumpliendo el SECRET CONTRACT. El Manager solo verifica `MKE_ZAI_API_KEY is set = YES`; el valor no se imprime, persiste ni audita.

## Consecuencias adjudicadas

- `OWNER_DECISION_REQUIRED = NO` para esta migración: el Manager continúa autónomo hasta `CHAPTER_01_ACCEPTED` y `READY_TO_SCALE_CORPUS`.
- Cambio de modelo = **nuevo baseline semántico** (no "mismo candidato, nuevo transporte"): P7/P8 previos no se resumen; el conocimiento generado se re-certifica desde la fuente (SOURCE_SHA `4de8f12d…`, 130 ventanas canónicas, mismas reglas de aceptación).
- P7b queda como evidencia histórica de resiliencia (L2 26 SKOs/0 wrong; runtime unattended 14.5h) — NO store de aceptación.
- Los watchers stealth se cerraron antes de tocar provider code (`STEALTH-WATCHERS-CLOSED.md`); un retorno del endpoint stealth no relanza corridas obsoletas.
- Si la API general de Z.AI no tuviera entitlement para este workload → `ZAI_GENERAL_API_ENTITLEMENT = BLOCKED` y decisión Owner. **Resuelto: entitlement OK (preflight Z0 autenticó y sirvió completions en api.z.ai/api/paas/v4).**
