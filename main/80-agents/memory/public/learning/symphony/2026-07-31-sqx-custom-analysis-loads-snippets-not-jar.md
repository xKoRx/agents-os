---
type: learning
scope: application
application: symphony
created: 2026-07-31
updated: 2026-07-31
confidence: high
source_session: efg28-hotfix
entities:
  - "[[Symphony]]"
  - "[[Echo Forge]]"
load_policy: when_application_loaded
indexable: true
index_priority: high
tags:
  - kind/learning
  - tech/sqx
  - project/echo-forge
  - scope/application
---

# SQX Custom Analysis carga Snippets, no el JAR

Al desplegar exporters Java (`EchoForge*`), actualizar
`/home/kor/sqx/user/extend/Snippets/SQ/CustomAnalysis/**` en cada worker.
Instalar solo `user/libs/EchoForgeAutomator.jar` **no cambia** el comportamiento
en runtime de Custom Analysis.

Verificado 2026-07-31: JAR nuevo con `mapSampleType→127` seguía reportando
`sample_byte=0` hasta sync de Snippets; después el smoke pasó a
`status=complete`.
