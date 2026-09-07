---
type: raw_session
schema_version: 1
scope: session
created: 2026-08-15
updated: 2026-08-15
area: "[[Echo]]"
project: "[[Echo Forge]]"
application:
entities:
  - "[[Symphony]]"
related:
  - "[[2026-08-15-cursor-grok-4-6-mt5-mmlots-export]]"
aliases: []
confidence: verified
source_session:
load_policy: never
indexable: false
index_priority: never
tags:
  - kind/raw-session
  - scope/session
---

# 2026-08-15-echo-forge-mt5-mmlots-raw

> [!warning]+ Raw session L0
> Archivo de auditoría y retrofit. Excluido del retrieval normal y de Graphify.

## Contexto

- Agente: [[Cursor]] / Cursor Grok 4.6
- Proyecto o entidad: [[Echo Forge]] / [[Symphony]]
- Objetivo de la sesión: fix `mmLots=0` en export MT5, desplegar, validar, cerrar con feedback.

## Transcript

```
Pedido: corregir export HTM (mmLots=0 por XML temporal), nueva versión, deploy, troubleshooting, feedback y cierre.
Diagnóstico confirmado: SourceCode.generate con .xml pierde lastSettings; FixedSize default Size=0.0.
Fix: EchoForgeMT5Exporter resuelve rg.getFilePath()/.sqx del databank y rechaza mmLots=0; gate Go equivalente.
Deploy falso: user/libs no era el classpath; Snippets.jar sí.
Canary Zeus: mmLots=0.1 sobre XAUUSD_L_H1_example_flow_4 Strategy_7.1.23.k0.
Worker 9.9.12 publicado; stager-runtime falló por state/CURRENT 0600 hasta chmod 644; wave example_flow_5 en builder.
HTM E2E de la wave nueva no se esperó.
```

## Evidencia externa

- Re-export Zeus log: `MT5 code generated from …/databanks/input/…Strategy_7.1.23.k0.sqx`
- `.mq5` canary: `input double mmLots = 0.1`
- Release: `deploy/9.9.12` + wave `example_flow_5`
