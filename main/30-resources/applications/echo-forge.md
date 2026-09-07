---
type: application
schema_version: 1
status: active
area: "[[Echo]]"
lang: Go, Java
github: https://github.com/xKoRx/symphony
path: ~/go/src/github.com/xKoRx/symphony/sqx
aliases:
  - Echo Forge
  - echo-forge
  - sqx
tags:
  - area/echo
  - kind/application
created: 2026-06-27
updated: 2026-08-14
---

# echo-forge

%% Naming: echo-forge es el link canónico de la aplicación; aliases puede incluir repo, nombre viejo o sistema externo; tags/slugs no reemplazan links. %%

> [!info]+ echo-forge
> **Lenguaje:** Go, Java (Gradle) · **Área:** [[Echo]]
> **GitHub:** [xKoRx/symphony](https://github.com/xKoRx/symphony) · **Path local:** `~/go/src/github.com/xKoRx/symphony/sqx`

> **Diferencia con SQX (StrategyQuant X)**: echo-forge es el **programa propio** (Go + Java + Python) que orquesta SQX. SQX es la **tool comercial** que genera las estrategias. echo-forge NO reemplaza a SQX — lo complementa. Ver [[strategyquant-x]].

## 📝 Descripción

- Fábrica y admisor cuantitativo adaptativo E2E de estrategias de trading, posicionado upstream en el ecosistema Echo. Procesa candidatos (Builder), valida mediante optimizaciones y Walk-Forward Analysis (WFM), ejecuta retro-evaluación robusta y compilación en MT5 Demo, y entrega únicamente las estrategias aprobadas (finalistas) a Echo Core mediante su API.

## 🎯 Responsabilidad (estable)

- Orquestar en Temporal el pipeline adaptativo de estrategias y delegar a workers SQX/MT5 las tareas físicas correspondientes.
- Mantener el contrato de ejecución serial de cada worker SQX y publicar los artefactos/resultados por los servicios remotos vigentes.

## 🔌 Contratos e interacciones (semi-estable)

- **Temporal:** workflows distribuyen activities mediante task queues compartidas; cada worker SQX consume una sola activity a la vez.
- **StrategyQuant X:** ejecución local controlada de proyectos fijos y plugins exporter.
- **MongoDB/MinIO:** persistencia y publicación remota de estado y artefactos del pipeline.
- **Echo Core:** destino downstream de estrategias finalistas aprobadas.

## 🚨 Invariante de ejecución SQX

> [!danger]+ Contrato obligatorio
> **1 VM = 1 worker = 1 task en ejecución.** Cada worker procesa una sola activity/task a la vez; la concurrencia solo existe entre VMs/workers distintos.

- No diseñar locks, mutexes, semáforos, slots ni workspaces/scopes para una supuesta concurrencia dentro del worker.
- El fan-out Temporal usa la task queue normal y cada worker consume secuencialmente.
- Cualquier cambio a esta regla exige una decisión arquitectónica separada y aprobación explícita del owner.
- Fuente canónica y consecuencias: [[2026-08-14-echo-forge-one-vm-one-worker-one-task]].

## 🔧 Datos útiles

- **Repo:** `xKoRx/symphony` (módulo `symphony/sqx`)
- **Path local:** `/Users/rjara/go/src/github.com/xKoRx/symphony/sqx`
- **Stack / notas:** Go (Temporal workflows, MongoDB, MinIO) · Java (Plugin de exportación en StrategyQuant) · Python (para scripts/tooling).
- **Tool subyacente:** [[strategyquant-x]] (SQX, tool vendor) corre dentro de las VMs `sqx-ulab-*` (ver [[../../aranea/02-servicios/ml-ia|sqx-ulab VMs]]).

## ✅ Tareas relacionadas

```tasks
sort by priority
not done
description includes echo-forge
short mode
hide task count
```

## 🔗 Links

- **[[strategyquant-x]]** — la tool SQX que echo-forge orquesta (definición de tool vs programa).
- **[[2026-08-14-echo-forge-one-vm-one-worker-one-task]]** — invariante vinculante de serialización por worker.
- [[../../aranea/02-servicios/ml-ia|sqx-ulab VMs]] — infraestructura SQX en Aranea (5 VMs en zeus/hera/kronos, SSDs sagrados `local-sqx-*`).
- [[Echo Forge]] — proyecto en `10-projects/Echo Forge/` (vista de programa).
- [Especificación de Features (SPECS.md)](file:///Users/rjara/go/src/github.com/xKoRx/symphony/specs/SPECS.md)
- [PRD Canónico](file:///Users/rjara/go/src/github.com/xKoRx/symphony/docs/prd/SQX_Adaptive_E2E_Pipeline_PRD.md)
- [RFC Canónico](file:///Users/rjara/go/src/github.com/xKoRx/symphony/docs/prd/SQX_Adaptive_E2E_Pipeline_RFC.md)
