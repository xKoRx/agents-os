---
type: doc
schema_version: 1
status: final
created: "2026-10-27"
area: "[[Echo]]"
project: "[[Echo Forge — Operación Real V2]]"
application: "[[xKoRx/symphony]]"
tags:
  - kind/doc
  - area/echo
  - sqx144
  - infraestructura
---

# SQX 144 — Sincronización de datos Kronos Windows → flota Linux (2026-10-27)

Referencia compacta. Evidencia detallada: skill `sqx-windows-data-sync` v1.0.0
en `xKoRx/symphony` (commit `a4d7968`, local sin push), logs en
`hefesto:/home/kor/sqx-win-sync-logs/`, manifests por corrida en
`hefesto:/home/kor/sqx-win-sync/<run-id>/`.

## Operación

- **Fuente única autorizada**: Kronos Windows (`worker-kronos`, 192.168.31.128),
  `C:\Users\KoR\Desktop\SQX144\user\data` — 22 archivos, 18 dirs,
  6,170,381,475 bytes, `data_futures.version=202610251316` (una semana más
  nueva que la flota, que estaba en `202610181215`).
- **Destinos**: `/home/kor/sqx/144/user/data` en zeus/hera/kronos/hefesto
  (resolución etcd `sqx_version=144` + `exec_base_path=/home/kor/sqx`).
  `~/sqx/user` (árbol 142) intacto.
- **Veredicto: PASS_4OF4 al momento del reemplazo.**

| Host | Build 144 | Archivos | Bytes | SHA manifest | Igualdad | SQX funcional |
|---|---|---:|---:|---|---|---|
| Kronos Windows | SQX144 (portable) | 22 | 6,170,381,475 | `f599ffb8c4645b00…` | SOURCE | n/a (origen quiescente) |
| Zeus Linux | 144.2953 | 22 | 6,170,381,475 | `f599ffb8c4645b00…` | EQUAL (at-rest) | PASS (worker registrado) |
| Hera Linux | 144.2953 | 22 | 6,170,381,475 | `f599ffb8c4645b00…` | EQUAL (at-rest) | PASS (worker registrado) |
| Kronos Linux | 144.2953 | 22 | 6,170,381,475 | `f599ffb8c4645b00…` | EQUAL (at-rest) | PASS (worker registrado) |
| Hefesto Linux | 144.2953 | 22 | 6,170,381,475 | EQUAL al reemplazo; delta post-arranque en 5 archivos runtime | DIVERGENT at-rest (documentado) | PASS (SQX abrió las H2 nuevas) |

## Estado y rollback

- **Backups**: depot central `hefesto:/home/kor/sqx-backups/sqx144-win-sync-<run>/<host>/data`
  (verificados EQUAL contra el pre-estado de cada host) + copias locales
  `data.old.<run>` en cada host. Runs: zeus `20261027_005541`,
  hera/kronos/hefesto `20261027_010500`. Rollback documentado en la skill
  (`rollback <host>`); viable y verificado.
- **Delta post-arranque hefesto** (esperado, no defecto): la sonda
  `sqcli --version` abrió las H2 en el único host donde la licencia pasa en
  manual; SQX reescribió `data.db`, ambas H2 y ambas `.version` al
  abrir/cerrar. La igualdad certificada es la del post-swap (logs por host).
- **Anomalía preexistente, fuera de alcance**: licencia SQX anclada a
  `/etc/machine-id` (pinned por `proactiva-set-machine-id.sh`);
  `sqcli help` manual falla con "License is invalid" en zeus/hera/kronos
  mientras las corridas del worker verifican OK (marcador en log del worker).
  `internal/license.db` no forma parte del árbol sincronizado.

## Skill reutilizable

`sqx-windows-data-sync` (repo `xKoRx/symphony`, `.agents/skills/`): modos
`manifest-win / stage / audit / verify / sync / state / rollback / cleanup /
selftest`, manifests SHA-256 deterministas, staging aislado con guard de
`--delete`, backup central verificado, swap atómico con worker drenado,
normalización de modos/ownership al pre-estado, verificación funcional H2.
Frontera con `sqx-instrument-sync`: fuente Windows → esta skill; fuente Zeus
(árbol `~/sqx/user/data` = 142) → skill v3.0.0 intacta.
