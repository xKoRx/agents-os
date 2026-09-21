---
type: doc
schema_version: 1
status: active
area: "[[Personal]]"
related:
  - "[[Ecosistema Personal — Exploración e Integración]]"
aliases:
  - Radar GitHub Trending septiembre 2026
  - Oportunidades por proyecto
  - Backlog de herramientas externas
tags:
  - kind/doc
  - area/personal
created: "2026-09-20"
updated: "2026-09-20"
---

# Radar de Herramientas — 2026-09-20

## Propósito

Conservar **todo** el contexto del análisis de herramientas externas para que un agente nuevo retome el portafolio sin reabrir 30 repositorios ni confundir recomendaciones con instalaciones. Esta ficha es investigación/inventario; el estado, autorizaciones y tareas viven exclusivamente en [[Ecosistema Personal — Exploración e Integración]] y las SPECs de cada proyecto destinatario. Los candidatos son ideas, **no componentes instalados ni aprobados**. Fecha de referencia: 2026-09-20; verificar HEAD, licencia, API, disponibilidad, términos y seguridad justo antes de una POC. La posición del trending no prueba calidad: diario contrastado directamente; semanal/mensual contrastados parcialmente con recopilatorios externos, sin rankings oficiales exhaustivos.

## Contenido

### Leyenda de decisión

- `TEST`: candidato a POC directa aislada tras aprobación del owner y gates del proyecto receptor.
- `STUDY`: examinar diseño, código, contrato o UX; no integrar framework completo.
- `PARK`: útil solo si aparece trigger verificable; no gastar esfuerzo ahora.
- `REJECT-SCOPE`: excluido del alcance vigente, **no rechazo definitivo del usuario**. Reabrir si cambia el problema o recibe mandato explícito.
- `OVERLAP`: alternativa mutuamente excluyente o solapada; seleccionar solo una tras benchmark.
- Estado de TODOS los candidatos al crear la nota: *evaluación no iniciada*. Ninguna de estas etiquetas equivale a instalación, licencia validada o certificación de producto.

### Matriz integral de candidatos (repo → sistemas → acción → límite/reapertura)

| Repositorio oficial | Sistemas relacionados | Tratamiento inicial | Hipótesis / límite / trigger |
|---|---|---|---|
| [supermemoryai/supermemory](https://github.com/supermemoryai/supermemory) | Agents-OS, Hermes, MKE | TEST / OVERLAP | POC de memoria temporal, contradicciones y RAG con 30–50 preguntas/corpus congelado; plugin Hermes/Codex y modo local declarados. Fuente Markdown NO cambia; validar retención, secretos, deployment y claims del autor; comparar vs OpenViking/WeKnora, no coexistir sin contrato. |
| [volcengine/OpenViking](https://github.com/volcengine/OpenViking) | Agents-OS, Hermes, Loom | STUDY / OVERLAP | Filesystem `viking://`, L0/L1/L2, compilación de sesiones, SDK Go y Hermes documentado. Alternativa única a benchmark Supermemory; AGPL-3.0 y requerimientos de modelos. No replicar jerarquía ya gobernada sin medir valor. |
| [Tencent/WeKnora](https://github.com/Tencent/WeKnora) | MKE, Agents-OS, Loom | STUDY / OVERLAP | RAG multimodal documental, BM25/denso/GraphRAG, Auto-Wiki, citas, MCP, pgvector/OpenSearch/MinIO. Su auto-wiki NO escribe el canon; no equivalente al pipeline visual independiente de video de MKE. Integración únicamente tras comparación memoria/retrieval. |
| [mksglu/context-mode](https://github.com/mksglu/context-mode) | Agents Hub, Hermes, Forge, Argus | TEST aislado / OVERLAP | Capturar logs/respuestas enormes fuera del contexto, FTS5/BM25, hooks y continuidad. Medir cuota REAL GLM, tokens, precisión, latencia y fallos. Hermes no tiene soporte integral verificado; subproceso hereda credenciales y no equivale a sandbox OS. Licencia Elastic 2.0, no MIT. |
| [affaan-m/ECC](https://github.com/affaan-m/ECC) | Agents-OS, Agents Hub | STUDY / OVERLAP | Extraer AgentShield, aprendizaje continuo, verificación; no instalar segundo OS de agentes ni segunda memoria/hook global. Integraciones varían por harness. |
| [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | Agents-OS, Echo/Forge, Polymarket | STUDY / OVERLAP | Inspeccionar constraint-/source-/doubt-driven development, reviewer adversarial y TDD; seleccionar skill individual, adaptar autorización de revisores externos; cuidado con `references/` ausentes en instalación parcial. No imponer otro lifecycle. |
| [obra/superpowers](https://github.com/obra/superpowers) | Agents-OS, Agents Hub | STUDY / OVERLAP | Plan→spec aprobada→subagentes→TDD/review. Comparar procedimientos con AGENTS OS; NO segundo gobierno paralelo ni activación automática sin control. |
| [max-sixty/worktrunk](https://github.com/max-sixty/worktrunk) | Agents Hub, Polymarket, Forge | TEST | Git worktrees/ramas por agente, estado, hooks; sandbox de cuatro agentes, sin autopush/automerge. Git worktree NO aísla credenciales, red, DB, puertos ni procesos. |
| [kunchenguid/firstmate](https://github.com/kunchenguid/firstmate) | Agents Hub, Hermes | STUDY / OVERLAP | Watcher event-driven/tokenless, secondmates SSH, recuperación tras reinicio y delegación. Ya existe orquestación propia: no segundo coordinador completo; observar autorización de merges. |
| [stablyai/orca](https://github.com/stablyai/orca) | Agents Hub, Daedalus, Loom | STUDY / OVERLAP | UI multiagente, SSH worktrees, móvil, diffs/comentarios. Referencia de UX; descartar implementación completa si Agents Hub + tmux cumplen; no dar acceso a llaves productivas por conveniencia. |
| [coder/coder](https://github.com/coder/coder) | Aranea, Agents Hub, Daedalus | PARK | Workspaces aislados provisionados con Terraform; probar solo cuando worktrees/VMs actuales no satisfagan requisitos, y verificar licencias/recursos; no levantar control plane adicional por moda. |
| [cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill) | Aranea, Hermes, Echo, Forge, Polymarket | TEST | Auditoría seis fases, coverage ledger, `confirmed/needs_validation/rejected`, revisor independiente; objetivo read-only, código peligroso únicamente en sandbox OS sin red, environment allowlist y scratch aislado; jamás tocar servicios PROD. |
| [alibaba/open-code-review](https://github.com/alibaba/open-code-review) | Forge, Polymarket, Echo | TEST | Review determinístico de diff, reglas por archivo, contextos aislados, JSON y modo delegado. Comparar defectos reales/false positives/costo sobre un PR autorizado; claims de benchmark del proveedor NO verificados. Reviewer no decide merge ni sustituye gates. |
| [Tencent/BrowserSkill](https://github.com/Tencent/BrowserSkill) | Hermes, investigación, vida | PARK / STUDY | CLI + extensión, reutiliza sesión de navegador y presta pestaña explícitamente; posible automatización con intervención humana. Trigger: tarea web repetitiva imposible con APIs públicas. Browser/credenciales separados de administración Aranea/MELI. |
| [Panniantong/Agent-Reach](https://github.com/Panniantong/Agent-Reach) | MKE, Hermes, investigación | STUDY | Capas de adquisición YouTube/RSS/GitHub/Reddit/X y `doctor`; documentar ToS, dependencias, cookies, límites y fallos. No instalar integraciones que requieren sesión privada en gateway administrativo ni prometer disponibilidad estable de terceros. |
| [microsoft/markitdown](https://github.com/microsoft/markitdown) | MKE, Agents-OS, documentación | PARK → TEST si materiales | Conversión PDF/PPTX/Word/Excel/audio/YouTube a Markdown; adaptador aislado futuro, no parte de M0 de un video. I/O con permisos del proceso y formatos de fidelidad variable. |
| [browser-use/video-use](https://github.com/browser-use/video-use) | MKE, creatividad | STUDY | Timeline transcript+filmstrip visual bajo demanda, EDL, validación del render; no asumir que audio cubre contenido visual. Integra edición de video, no adquisición científica de evidencia. ElevenLabs/servicios terceros pueden tener costo y datos salientes. |
| [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) | MKE downstream, Echo docs, vida | PARK | HTML/CSS/animación→MP4 determinista, videos de PR/producto; salida/publicación del conocimiento, NO video→conocimiento. Trigger: necesidad de producir piezas audiovisuales periódicas. |
| [THU-MAIC/OpenMAIC](https://github.com/THU-MAIC/OpenMAIC) | MKE downstream, cursos, vida | PARK | Generación de cursos, clases interactivas, cuestionarios, agentes; trigger: publicación educativa tras validar calidad del conocimiento MKE. No crear un proyecto de cursos paralelo ahora. |
| [debpalash/VoiceStudio](https://github.com/debpalash/VoiceStudio) | MKE downstream, Hermes, vida | PARK | TTS/voz local, doblaje, API/MCP. Trigger: salida hablada propia; verificar consentimiento para voces y requisitos de hardware/licencias. |
| [cathrynlavery/diagram-design](https://github.com/cathrynlavery/diagram-design) | Loom, Project Lens, diagramas técnicos | STUDY | Patrones editoriales HTML/SVG, accesibilidad, densidad, visualización de arquitectura; UX solamente, no clonar framework ni añadir diseño decorativo. |
| [tt-a1i/archify](https://github.com/tt-a1i/archify) | Loom, Project Lens, Agents-OS | STUDY | Typed JSON IR→HTML/SVG determinista; snapshots Before/Delta/After, trazabilidad de rutas y topologías. Verificación de aristas contra fuente canónica; no permitir al agente inventar conexiones. |
| [asciimoo/hister](https://github.com/asciimoo/hister) | Investigación personal, Loom, Agents-OS | PARK / STUDY | Índice privado de navegador y archivos en Go, CLI/MCP; trigger: pérdida repetida de fuentes investigadas que no resuelve vault/buscador actual. Evitar capturar portales de trabajo, sesiones privadas o datos sensibles; AGPL. |
| [blader/humanizer](https://github.com/blader/humanizer) | Comunicación, vida | PARK / OVERLAP | Skill elimina patrones de prosa IA manteniendo hechos/voz; comparar con No AI Slop en textos propios y elegir UNO. No aplicar transformaciones a contratos SPEC sin diff de invariantes. |
| [petergyang/no-ai-slop](https://github.com/petergyang/no-ai-slop) | Comunicación, vida | PARK / OVERLAP | Alternativa a Humanizer, detección + edición explicable; trigger: publicaciones recurrentes. No detector fiable de autoría. |
| [danny-avila/LibreChat](https://github.com/danny-avila/LibreChat) | Aranea, Hermes, vida | PARK / OVERLAP | UI self-hosted multimodelo/MCP/agentes; trigger: carencia real del dashboard Hermes/cliente actual. No duplicar identidad, gateway, logs ni control de permisos; workspaces de código marcados experimentales. |
| [TencentCloud/Octop](https://github.com/TencentCloud/Octop) | Aranea, Hermes, vida | PARK / OVERLAP | Assistant self-hosted multicliente/multiusuario, ACP, shell/browser remoto, memoria; otro control plane y credenciales de alto riesgo. Reabrir solo ante necesidad de uso familiar multiusuario que Hermes no cubre. |
| [rustfs/rustfs](https://github.com/rustfs/rustfs) | Aranea, Backup/DR, MinIO | PARK / REJECT-SCOPE migración | S3/Rust alternativa, Apache 2.0; compatibilidad de formato MinIO en preview y objetos cifrados no legibles directamente. Laboratorio S3 aislado si la estabilidad/licencia de MinIO exige evaluación; **no** migrar discos/datos/servicios hoy. |
| [AlexsJones/llmfit](https://github.com/AlexsJones/llmfit) | Aranea, inferencia, Hermes, MKE | TEST | Detecta hardware/VRAM/RAM, cuantizaciones, tok/s estimados y benchmarks. Medir en equipo autorizado con Ollama/LM Studio; no confundir fit/speed con calidad del modelo. |
| [google-research/timesfm](https://github.com/google-research/timesfm) | Echo, Polymarket (solo estudio) | PARK / REJECT-SCOPE PROD | Forecasting series temporales; benchmark offline separado de estrategia. Pesos TimesFM 3.0 restringidos no comercial/no producción según README; no usar en trading real ni afirmar edge por accuracy. |
| [tradesdontlie/tradingview-mcp](https://github.com/tradesdontlie/tradingview-mcp) | Echo, investigación trading | PARK / REJECT-SCOPE MVP | Puente CDP local TradingView Desktop/Pine/indicadores, interfaz no documentada vulnerable a updates, requiere app/suscripción. No ejecución de trades; no parte del core Echo ni Polymarket MVP. |
| [tamaratran/fast-jev-compaction](https://github.com/tamaratran/fast-jev-compaction) | Agents Hub, economía tokens | STUDY / PARK | Compactación selectiva de tool calls sin reescribir textos; Jev/API externa + feature flag Claude Code anticipada. Trigger: compaction actual pierde comandos, decisiones, rutas o errores; evaluar privacidad/costo antes de enviar transcripciones. |
| [bilawalsidhu/gods-eye-view](https://github.com/bilawalsidhu/gods-eye-view) | Aranea, Loom, vida | PARK | Inspiración de visualización espacial/operativa; validar propósito real, stack y privacidad antes de proponer integración; no sustituye observabilidad ni inventario. |
| [ayghri/i-have-adhd](https://github.com/ayghri/i-have-adhd) | Productividad personal, Loom | PARK | Referencia de interacción orientada a foco/tareas; revisar funciones y accesibilidad antes de afirmar beneficio. Nada de inferir información de salud ni imponer workflows. |
| [xKoRx/agents-os](https://github.com/xKoRx/agents-os) | Todos | AUTHORITY | Sistema propio existente: fuente Markdown de estado y gobernanza, no herramienta externa candidata. |
| [xKoRx/loom](https://github.com/xKoRx/loom) | Loom | AUTHORITY | Front actual; validar baseline/estado reciente desde su nota/repositorio en vez de asumir v0.4 o v0.6 productiva. |

### Oportunidades precisas por proyecto

**Polymarket Engine:** primero cerrar contratos compartidos y POCs PE-001 Sports, PE-004 Maturation, PE-030 Weather y NegRisk conforme al roadmap canónico, sin reabrir metodología ni desplazar pruebas read-only. Open Code Review para diffs con riesgo de divergencia SCREEN/REPLAY/SHADOW, Security Audit para lectura y fronteras de credenciales/protocolo; Context Mode para logs/datasets; TimesFM/TradingView/TradingAgents quedan `PARK/REJECT-SCOPE` por no validar mecanismos de edge. No órdenes, saldos ni credenciales de trading en experimentos.

**MKE:** preservar M0 audiovisual: adquisición original→ASR y cobertura visual independiente→evidencia con timestamps→investigación y validación. video-use aporta representación temporal; MarkItDown documentos complementarios; Agent Reach conectores; WeKnora recuperación posterior; OpenMAIC/HyperFrames/VoiceStudio salida creativa posterior. No añadir estas dependencias al M0 ya congelado.

**Echo:** seguridad de infraestructura/secretos y revisiones de cambios en Go, concurrencia y persistencia; TimesFM SOLO en investigación offline con licencia y evaluación fuera de muestra, sin tocar señales productivas.

**Echo Forge:** Open Code Review en diff de una rama aprobada con verificador independiente y medición de hallazgos; Security Audit para privilegios/certificados y Context Mode para logs MT5 enormes. Ninguno reemplaza gates, certificación o producción aprobada.

**Agents-OS:** memoria comparativa Supermemory vs OpenViking vs baseline, seleccionar una sola alternativa; ECC, Superpowers y Agent Skills como procedimientos puntuales sin constitución paralela. Retención, contradicción, procedencia y autoridad documental son gates.

**Agents Hub:** Worktrunk para worktrees; Firstmate watcher, delegación y recovery; Orca interfaz y revisión; Coder si se justifica sandbox/workspace completo. Cuatro worktrees NO son cuatro sandbox de seguridad.

**Hermes/Ariadna:** memoria local bajo scoping, herramientas web públicas con credenciales separadas, browser en perfil no administrativo y revisión de IAM. No habilitar shells globales ni permisos root por comodidad. Context Mode para salidas; soporte de hooks Hermes pendiente de prueba.

**Loom:** antes leer nota actual, respetar read-only o laboratorio experimental según gate vigente. Human Action Center/Project Command Center/Resume Context como posibles UX; Archify/Diagram Design/Hister como referencias. No duplicar editor, Graphify, búsqueda o segundo backend de estado; el último estado de F3 debe leerse de Loom, no de este radar.

**Aranea:** Security Audit de permisos y fronteras; llmfit hardware; Coder/RustFS solo laboratorio. Ceph/MinIO/PBS y DR preservan ownership/gates y no reciben mutaciones automáticas.

**Backup/DR:** auditoría de contratos y pruebas de recuperación conforme proyecto canónico; RustFS no es sustituto in-place de MinIO ni backup de sí mismo.

**Argus:** compactación/filtrado manteniendo trace IDs, ventana, logs y fuente cruda; no aceptar diagnósticos LLM sin evidencia.

**MELI/RIO/Project Lens:** únicamente inspiración abstracta UI/arquitectura; jamás copiar contenido corporativo hacia cuentas/proyectos personales, servicios cloud ni vault no permitido. Respetar veto Obsidian e infraestructura autorizada.

**Vida y creatividad:** priorizar necesidad concreta: Hister (investigación personal), Humanizer O No AI Slop (redacción), LibreChat/Octop (UI/chat familiar si hace falta), HyperFrames/OpenMAIC/VoiceStudio (generación de contenido tras conocimientos validados), God's Eye View (inspiración visual), i-have-adhd (patrones de productividad). Privacidad y tiempo de mantenimiento son gates.

### Descartes/proyectos que NO deben desaparecer

- **Frameworks duplicados:** ECC/Superpowers/Agent Skills/OpenSpec/Firstmate/Orca/Octop/LibreChat se conservan como `STUDY/PARK/OVERLAP`. Motivo: ya existen Agents-OS/Agents Hub/Hermes y duplicar hooks, memorias y políticas genera dos autoridades. Reapertura: problema sin solución + baseline + un responsable.
- **TradingAgents y TimesFM para estrategias productivas:** `REJECT-SCOPE` por ausencia de hipótesis causal, licencia/validación y riesgo de desplazar POCs congeladas. Reapertura: mandato de research offline con datasets con tiempos de disponibilidad reales, benchmark y licencias.
- **RustFS como migración inmediata:** `REJECT-SCOPE` mientras existan gates Ceph/MinIO/Backup-DR y compatibilidades limitadas. Reapertura: caso contractual específico, migración por S3, restauración y rollback verificados.
- **MarkItDown, WeKnora, HyperFrames, OpenMAIC y VoiceStudio en M0:** `REJECT-SCOPE` dentro de M0, `PARK` para futuras fases. M0 no debe convertirse en un producto universal antes de probar un video.
- **Hister/segunda memoria en Loom:** `REJECT-SCOPE` como backend duplicado; solo UX/retrieval probado contra índices existentes. Reapertura: problema de búsqueda demostrado.
- **Más de una skill de estilo:** Humanizer o No AI Slop; no ambas sin necesidad diferenciada.
- **Captura de navegador/sesiones:** BrowserSkill/Agent Reach pendientes por privilegios, ToS y fuga de cookies, especialmente en MELI y Aranea.
- **OpenSpec:** discutido como representante de frameworks adicionales, pendiente verificar URL/versión/función específica antes de cualquier selección; no se lo atribuye como analizado individualmente.
- **Costos de cloud/marketing:** toda afirmación de ahorro porcentual, benchmark o soporte de plataforma se verifica con casos propios; no convertir marketing en gate.

### Protocolo mínimo de POC, resultado y rollback

Para cada candidato seleccionado añadir una ficha corta en esta nota o enlace a subproyecto autorizado: `problema actual; baseline medido; sistema; repo+versión+licencia; datos/secretos/red/escritura; diseño aislado; fixtures y métricas; evidencia; riesgos; costo operativo; ADOPT/ADAPT/PARK/REJECT; condición de reapertura; dueño; rollback`. Si afecta código/infra, el subproyecto dueño requiere branch, SHA base, SPEC funcional y técnica ANTES de ejecutar. No crear diez fichas especulativas vacías.

### Primeras pruebas candidatas

1. Cloudflare Security Audit de repo de agente autorizado, con sandbox OS y sin secretos.
2. Alibaba Open Code Review sobre un PR existente (no implementar cambios en la prueba).
3. Worktrunk: cuatro agentes, cuatro worktrees, sin conflictos ni auto-merge.
4. Supermemory **o** OpenViking contra baseline retrieval de Agents-OS: 30–50 preguntas con información vigente y desactualizada y enlaces a fuentes.
5. llmfit en hardware de desarrollo/inferencia para estimaciones y mediciones verificables.

### Fuentes y método

Los enlaces del catálogo apuntan a repos oficiales inspeccionados en esta conversación salvo `gods-eye-view`, `i-have-adhd`, `TradingAgents` y `OpenSpec`, cuyos detalles deben revalidarse; nombres incompletos o análisis previo no equivalen a auditoría técnica. README no acredita instalaciones, calidad real, seguridad ni estabilidad; verificar documentación, licencia, commits y releases actuales. Los datos de GitHub Trending de septiembre son efímeros y no se usan como criterio de adopción.

Retomar desde [[Ecosistema Personal — Continuidad]] y después [[Ecosistema Personal — Exploración e Integración]], no releer todo el catálogo salvo al seleccionar un candidato.
