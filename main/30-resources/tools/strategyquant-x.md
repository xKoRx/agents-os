---
type: tool
status: active
scope: tool
area: "[[Echo]]"
lang: C# (core), Java (plugin), CLI invocable
platform: Windows (UI), headless CLI (Linux/Windows)
source_url: https://strategyquant.com
command:
  - sqx
  - sqx-cli
entities:
  - "[[Echo Forge]]"
  - "[[echo-forge]]"
  - "[[sqx-ulab]]"
load_policy: when_tool_loaded
indexable: true
index_priority: medium
aliases:
  - StrategyQuant X
  - SQX
  - StrategyQuant
  - strategyquant-x
  - sqx
tags:
  - area/echo
  - kind/tool
  - trading
  - builder
  - third-party
created: 2026-07-01
updated: 2026-07-01
---

# StrategyQuant X (SQX)

%% Naming: strategyquant-x es el link canónico de la tool; aliases incluye SQX, StrategyQuant, sqx. Tags/slugs no reemplazan links. %%

> [!info]+ StrategyQuant X (SQX)
> **Tipo:** tool comercial (vendor: StrategyQuant s.r.o.) · **Área:** [[Echo]]
> **Lenguaje:** C# (core) + Java (plugin) + CLI invocable
> **Plataforma:** Windows (UI completa) · Headless CLI (Linux/Windows, usado por [[echo-forge]])

## 📝 Descripción

**StrategyQuant X (SQX)** es una plataforma comercial de generación y optimización algorítmica de estrategias de trading. Permite:

- **Builder**: genera estrategias desde cero combinando bloques (entry, exit, filtros, gestión de riesgo).
- **Optimizer**: ajusta parámetros sobre una estrategia semilla.
- **Walk-Forward Analysis (WFM)**: valida robustez out-of-sample.
- **Retester**: re-corre estrategias sobre datos históricos reales (trades de MT4/MT5).
- **Robustness tests**: detecta overfitting y curva de equity inestable.

**En Aranea**, SQX corre dentro de las VMs `sqx-ulab-*` (5 VMs en zeus/hera/kronos, 1 corriendo + 4 en mantenimiento) y es **orquestado por [[echo-forge]]** (programa Go + Java + Python en `xKoRx/symphony`) mediante un plugin Java de exportación física + Temporal workflows.

## 🔧 Datos útiles

- **Vendor:** StrategyQuant (https://strategyquant.com)
- **Licencia:** comercial (per-seat / per-VM, owner gestiona)
- **Modo de uso en Aranea:**
  - **Interactivo (legacy):** Windows VM con UI completa. Útil para investigación manual.
  - **Headless CLI (Echo Forge):** invocado vía línea de comandos con `.cfx` templates. Plugin Java custom escribe databanks en MongoDB/MinIO. Ver [[echo-forge]].
- **Datasets SQX:** residen en `local-sqx-*` SSDs (sagrados, 931 GB × 3). Datos de mercado (forex, CFDs, futuros) descargados por SQX desde providers ( Dukascopy, etc.).
- **Outputs:** databanks de estrategias, reportes HTML, exports `.csv`/`.json`, exports MT5 (`.mq5`).

## 🏗️ Infraestructura en Aranea

| Componente | Ubicación | Detalle |
|---|---|---|
| **VMs SQX (5)** | zeus/hera/kronos | `sqx-ulab-{zeus,kron,hera}-0` + `-1` secondary, 1 running + 4 stopped (en mantenimiento) |
| **SSDs sagrados** | `local-sqx-{zeus,hera,kronos}` | 931 GB WD Green SATA cada uno, exclusivos para datasets SQX. **NO TOCAR**. |
| **Plugin Java** | dentro de cada VM SQX | Exporta databanks físicos a MongoDB + MinIO. Mantenido en repo `xKoRx/symphony/sqx/plugin-java`. |
| **Orquestador** | cluster Go (echo) | [[echo-forge]] invoca SQX CLI, ingiere resultados vía plugin, ejecuta WFM Go evaluator, publica a MT5 demo. |

### Capacidad esperada (cuando todas las VMs operen)

> Owner: "normalmente usarán el 80% de los recursos de su host para procesar y desarrollar nuevas estrategias".

| Nodo | VMs SQX | CPU disponible | RAM disponible | Disco sagrado |
|---|---|---|---|---|
| zeus (32t / 94 GB) | 2 VMs (108 running 28t/75GB, 170 stopped 8t/23GB) | ~80% (25t) | ~80% (75 GB) | `local-sqx-zeus` 931 GB |
| hera (72t / 125 GB) | 1 VM (123 stopped 70t/100GB) | ~80% (57t) | ~80% (100 GB) | `local-sqx-hera` 931 GB |
| kronos (80t / 251 GB) | 2 VMs (111 stopped 76t/137GB, 162 stopped 12t/30GB) | ~80% (64t) | ~80% (200 GB) | `local-sqx-kronos` 931 GB |

Cuando todas las VMs SQX estén activas: **146 vCPU + 275 GB RAM + 2.8 TB SSD** dedicados a SQX en el cluster.

## 🔗 Links

- **[[echo-forge]]** — programa que orquesta SQX (repo `xKoRx/symphony`, módulo `sqx`).
- **[[Echo Forge]]** — proyecto en `10-projects/Echo Forge/`.
- [[../../aranea/02-servicios/ml-ia|sqx-ulab VMs]] — detalle de VMs SQX en Aranea.
- [[../../aranea/01-topologia/nodo-zeus|nodo-zeus]], [[../../aranea/01-topologia/nodo-hera|nodo-hera]], [[../../aranea/01-topologia/nodo-kronos|nodo-kronos]] — detalle de SSDs `local-sqx-*` por nodo.
- [StrategyQuant.com](https://strategyquant.com) — vendor.

## 📝 Notas operacionales

- **Backup**: el plan de backup actual ([[../../aranea/03-storage/DESIGN-PROPOSAL|Design Proposal iter 4]]) considera las VMs SQX como **critical VMs** (vzdump daily a PBS + sync configs a pcloud). Los datasets SQX en sí están dentro de las VMs, no en storage compartido — se respalda via vzdump de la VM completa.
- **Restore drill**: programado mensual rotativo (ver ticket 013 § Fase 5).
- **Known issue**: errores en plantillas `.cfx` del Retester documentados en `80-agents/memory/public/known-error/symphony/sqcli-retester-config-errors.md` (bloquea WFM hasta corregir).
- **Etapa Echo Forge actual**: Etapa 4 WIP (post-optimizer + Robust Run + corrección `.cfx`). Etapas 1-3 completas (cimentación, plugin Java, MongoDB, ranking, WFM Go evaluator).