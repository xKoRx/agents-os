---
type: change_log
schema_version: 1
scope: session
created: "2026-10-06"
updated: "2026-10-06"
area: "[[Meli]]"
project: "[[SIG-600 — Borrado seguro de Data Products]]"
application: "[[rio-playmaker]]"
entities: ["[[rio-playmaker]]", "[[SIG-600 — Borrado seguro de Data Products]]"]
related: []
aliases: []
confidence: verified
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-10-06-dp-delete-hotfix

## Cambio

- Creado [[Hotfix — Borrado de DP con componentes eliminados]] con aceptación, scope, plan y evidencia.
- Creada [[Descripción PR — rio-playmaker — Hotfix componentes eliminados]] desde el template del repo.
- Actualizado [[SIG-600 — Borrado seguro de Data Products]] en estado actual y bitácora; el proyecto sigue activo. Antes no tenía el hotfix del blocker; ahora registra el commit final sobre master, evidencia repetida sobre esa base y PR draft #1267 autorizado y publicado. El resto de las iniciativas y el estado de PR #1228 se preservan.
- Registrada la versión `0.0.1-delete-dp-fix` solicitada posteriormente por el owner en el estado del proyecto, detalle del hotfix y nota de descripción: `FINISHED`, SHA exacto de la rama y metadata `run_test=false`. La creación no existía previamente; no se sustituyó evidencia local por una afirmación de tests remotos.

## Motivo y fuentes

Solicitud explícita del owner: generar un hotfix para permitir soft delete ante componentes Deleted o con deleted_at. Fuente técnica: repo `melisource/fury_rio-playmaker`, base `6f8ea3d721b1e09da9bb2d70da21ebec311cf6c9`, preparación local `f5a293f248978738520c118f04b9ac1ec6879625`. Después el owner autorizó push y PR, exigiendo master; entrega publicada en [https://github.com/melisource/fury_rio-playmaker/pull/1267](https://github.com/melisource/fury_rio-playmaker/pull/1267), base `7dbc49ccf8bb49a6998f94a55da011e54c53f661`, commit `9118cbe7f953a446b83432a410933ccf89cee0e2`. Es estado actual verificable de la entrega, no una hipótesis ni memoria de comportamiento.

## Validación

- 17 regresiones nuevas; ocho fallas esperadas contra baseline y ninguna con el fix.
- Suite inicial sobre develop: 4.481 tests, sin fallas/errores, 2 skips; line coverage 97,24%. Suite repetida sobre master: 4.400 tests, sin fallas/errores, 2 skips preexistentes; line coverage 97,21%.
- Contratos, focalizados y diff check PASS; source limpio tras commit.
- El rechazo inicial de publicación quedó resuelto por autorización explícita del owner. PR draft #1267 publicado contra master con un único commit y cinco archivos. Sin deploy ni mutaciones de datos remotos; sólo rama y PR publicados.
- Versión [0.0.1-delete-dp-fix](https://web.furycloud.io/rio-playmaker/versions/detail/0.0.1-delete-dp-fix) verificada por `fury versions get --output json`: `FINISHED`, branch `hotfix/dp-delete-ignore-deleted-components-master`, commit `9118cbe7f953a446b83432a410933ccf89cee0e2`, `disabled=false`, `productive=false`; [build #1788](https://rp-builds-java.furycloud.io/blue/organizations/jenkins/rio-playmaker/detail/rio-playmaker/1788/pipeline/). Invocación oficial de creación sin `--no-tests`; metadata final `run_test=false`, discrepancia informada al owner. No se alteró ningún gate, no se repitió la creación ni se desplegó.

## Compartibilidad y rollback

Registro local sin secretos ni payloads reales. Para revertir el hotfix, revertir su commit; para revertir documentación, retirar las referencias y restaurar los bloques previos del proyecto. No hay cambios de schema ni datos.
