---
type: doc
schema_version: 1
status: active
area: "[[Trading]]"
related: ["[[Estrategias IMOX — Forex y CFD con Echo Forge]]", "[[IMOX — NDX - Frente inicial]]", "[[Echo Forge — Operación Real V2]]", "[[IMOX — Cobertura de investigación]]"]
aliases: ["rescate 142", "inventario SQX 142 flota", "recovery IMOX 2026-10-25"]
tags:
  - kind/doc
  - topic/imox
  - area/trading
created: "2026-10-25"
updated: "2026-10-25"
---

# IMOX — Rescate 142 en flota Forge (2026-10-25)

## Propósito

Registro canónico de la recuperación forense del material NDX creado en SQX 142 sobre la flota operacional de Echo Forge (Zeus, Hera, Kronos), su clasificación por grupo (G1/G2/G4) y su preservación verificada en almacenamiento privado. Cierra la tarea de inventario del material 142 que el proyecto tenía diferida. Alcance: solo lectura de orígenes, copia conservadora; no se lanzaron builders, retesters, optimizers ni waves de Forge.

## Contenido

### Dónde estaba el material

Las estrategias 142 viven en el árbol compartido `/home/kor/sqx/user` de cada worker (enlazado como `user/` de la instalación 142; la 144 tiene su propio árbol con proyectos más recientes del owner, fuera de este rescate). Los databanks de `projects/Retester/databanks/` son directorios de `.sqx`, y `user/strategies/` guarda las estrategias salvadas con sufijo de job (`.z0` Zeus, `.h0` Hera, `.k0` Kronos).

**«Highprecision» no es un nombre de artefacto:** es la marca física `Results/CrossCheck_HigherPrecision/` embebida dentro de cada `.sqx` retesteado con el cross-check de precisión alta. Las «retesteadas con highprecision» son los databanks `in retest cross` de cada host (6.878 de 7.080 archivos inspeccionados la llevan).

### Tres pools distintos, clasificados por bloques (no por nombre)

| Pool | Ubicación origen | Archivos | Grupo (evidencia) | Uso Forge |
|---|---|---|---|---|
| A — Cohort 001 | Zeus `in retest cross` | 727 | **G1** (727/727 ⊆ universo `Build_BR_G1_H1.cfx`, 40 bloques; corrobora el análisis 15/15 de Forge) | Ya ingestado y procesado (FlowRun `1a4d66d6`, wave1c 727/727, TopProjection 34 → optimizer → 10 robust en `Results`/`selected`) |
| B — Cohorte Hera | Hera `in retest cross` | 555 | **G2** (555/555 ⊆ universo `Build_G2_BR_H1.cfx`, 24 bloques; 149 con bloques G2-exclusivos Fractal/Pivots) | Nunca ingestado |
| C — Pool NDX_W3 | Kronos `in retest cross` | 1091 | **G4 dominante** (1091/1091 ⊆ universo `Build_G4_BR_H1.cfx`, 60 bloques; 597 con bloques G4-exclusivos ADX/Aroon/HMA/KAMA) | Nunca ingestado |

- Los tres pools son disjuntos byte-a-byte (0 SHA256 compartidos entre pools). Pool C es el agregado de los tres workers: 427 `.z0` + 302 `.h0` + 362 `.k0`; las copias de `strategies/` de Kronos son byte-idénticas a las de Zeus (427) y a 302 de las 383 de Hera (81 sin sufijo existen solo en Hera).
- Kronos además retesteó el pool en cadena: `in retest full` 1000 → `passed` 200 → `selected` 98. Hera conserva `passed` 291, `fail` 158, `test` 97, `selected` 57, `in retest full` 14.
- **7.080/7.080 archivos** (incluidos derivados): símbolo `USATECHIDXUSD_darwinex`, H1, LONG, `AppVersion="SQX Build 142.2399"` ⇒ creación en 142 demostrada por contenido. Los builders G1/G2/G4 existen idénticos en los tres hosts (G1 y G4 byte-idénticos; G2 difiere en bytes con el mismo universo habilitado).
- No se encontró ningún grupo G3/G5/G6 materializado (sin builders ni pools con esos universos); si existieron, están perdidos o fuera de estos hosts.

### Preservación verificada

Destino privado autorizado: bucket **`sqx-strategies`** (MinIO 192.168.31.92:9000, el mismo almacenamiento de evidencias de Forge), prefijo nuevo `recovery-imox-142/20261025/` — 15 tars (~1,71 GB) + 10 manifiestos, subidos por URL prefirmada y **verificados en destino: tamaño exacto y ETag == MD5 de origen en 15/15**; SHA256 por tar en `manifests/SHA256SUMS-*.txt` y SHA256 por archivo en `manifests/classify_*.jsonl`. Orígenes intactos; temporales de sesión eliminados de los hosts.

No preservado (declarado, no perdido): derivados intermedios por volumen — Zeus `passed/fail/filter/filtered/filtrando*` (528), Hera `passed/fail/test` (506), Kronos `passed/filtrando*` (225). Quedan intactos en origen.

### Disponibilidad para Forge y frontera con Echo

`manifests/staging-forge-import-manifest.json` deja Pools B y C **READY_FOR_IMPORT** (mismo patrón Watcher Import que Cohort 001) y el Pool A marcado ALREADY_INGESTED. Despachar la wave es decisión del owner: la cadena completa hasta Echo requiere campaña C6+ de Forge e Integration V2 Forge→Echo→The Lab, que no está construida; hoy `promotion_records=0` y `strategy_versions=0` en Echo PROD (RO 2026-10-25) — nada de Forge ha entrado aún a Echo.

### Cambio de alcance respecto del pedido original

El mandato hablaba de «otros dos workers» con retesteadas highprecision y de grupos G1/G3/G4: los datos muestran que los tres workers participan de los tres pools y que los grupos reales materializados son **G1, G2 y G4** (G3/G5/G6 sin evidencia). El documento canónico de grupos «SQX — BR H1 LONG — Grupos, Builders y continuidad Forge-Echo.md» no existe en el vault; la clasificación de esta nota se derivó de los `.cfx` reales de flota.

## Fuentes

- Manifiestos y evidencia completa: MinIO `sqx-strategies/recovery-imox-142/20261025/` (INVENTORY-REPORT.md, classify_zeus/hera/kronos.jsonl, universes-builders.json, staging-forge-import-manifest.json).
- Vault: [[Echo Forge — Operación Real V2]] (Cohort 001, FlowRun `1a4d66d6`, C5.2 con 34 optimizadas + 10 robust en Zeus) · [[IMOX — NDX - Frente inicial]] · [[IMOX — Cobertura de investigación]].
- Configs de flota: `/home/kor/sqx/user/configs/` por host (`Build_BR_G1_H1.cfx` sha256 `786cdaea…`, `Build_G2_BR_H1.cfx` `1ae31bc7…`(Hera/Kronos)/`9b5d952d…`(Zeus), `Build_G4_BR_H1.cfx` `92968795…`).
