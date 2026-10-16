# Change Log consolidado — 2026-10-16 (Certificación integral SQX 144, sesión ZCode/GLM-5.3-Flash)

## Vault

- `10-projects/Echo Forge — Operación Real V2/Echo Forge — Operación Real V2.md` — bitácora 2026-10-16 (`SQX144_FULL_CAMPAIGN_IN_PROGRESS`): config histórica recuperada (ForgeCampaign 0ce72173), campaña V2 despachada (569c152c / wave1 34b95fd6), remediaciones de flota, adaptación de CFX dukascopy_UTC02, probes 3/3 y pendientes.
- `10-projects/Echo Forge — Operación Real V2/artifacts/sqx144-full-campaign-20261016/` (nuevo): SQX144-FULL-CAMPAIGN-CERTIFICATION.md, SQX144-WORKER-CAPABILITY-MATRIX.csv, SQX144-CAMPAIGN-FUNNEL-BY-GROUP.csv, SQX144-FINALISTS-BY-GROUP.csv, SPEC-camp-ndx144.json (8335d72a), ADAPTATION-REPORT.json, HISTORICAL-E2E-BASE-SPEC-cert-f05-02.json, SHA256SUMS-bundle-20261016.txt.
- `80-agents/journal/agent-runs/2026-10-16-zcode-glm53-echo-forge-sqx144-full-campaign-dispatch.md` (nuevo).
- `80-agents/journal/feedback/` — ver feedback del mismo día (fricciones de transporte y fail-open de SQX).

## Infraestructura (fuera del vault, con evidencia en el bundle)

- Zeus/Hera/Kronos: datasets `USATECHIDXUSD{,_darwinex}` copiados root→144 tree; filas DATA insertadas en `/home/kor/sqx/144/user/data/data.db` (IDs 213/214; backup `data.db.bak-20261016-precfix`); `chmod -R a+rwX /home/kor/sqx/144/internal/testfiles` (sudo kor).
- Kronos: `Build_BR_G1_H1.cfx` propagado desde Zeus (SHA 786cdaea verificado).
- Residuos documentados: 3 CFX sobrantes movidos a `processed/` del paquete watcher; `custom/project.cfx.preprobe-sqx144-20261016` (backup de probe en Zeus) sin restaurar por diseño (el worker stages su propio project.cfx por task).

## Repos de producto

- `xKoRx/symphony`: SIN delta (master = origin/master = 5a66bb65; helpers efímeros creados y eliminados: ephemeral-cfgread, ephemeral-validate, ephemeral-pollers).
