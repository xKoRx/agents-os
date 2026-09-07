---
type: dashboard
icon: 📊
tags:
  - kind/dashboard
created: 2026-07-08
updated: 2026-07-08
cssclasses:
  - wide
---

# Echo Forge WFM Dashboard

> [!tip] Panel de control interactivo para auditoría de Walk-Forward Matrix (WFM). Haz clic en el comando CLI para copiarlo al portapapeles y descargarlo con un solo clic.

```dataviewjs
const basesPath = "30-resources/dashboards/echo-forge/bases";
const pages = dv.pages(`"${basesPath}"`).where(p => p.type === "strategy_evaluation");

// Contenedor principal
const mainContainer = dv.container.createEl("div", { cls: "wfm-dashboard-container" });

// Estilos premium
const styleEl = mainContainer.createEl("style");
styleEl.textContent = `
  .wfm-dashboard-container {
    font-family: var(--font-interface, 'Inter', sans-serif);
    color: var(--text-normal);
    padding: 0.5rem;
  }
  .wfm-filters-panel {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    background: var(--background-secondary);
    padding: 1.2rem;
    border-radius: 12px;
    border: 1px solid var(--border-color);
    margin-bottom: 2rem;
    box-shadow: var(--shadow-s);
  }
  .wfm-filter-group {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    min-width: 150px;
  }
  .wfm-filter-group label {
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }
  .wfm-filter-group select {
    background: var(--background-primary);
    border: 1px solid var(--background-modifier-border);
    border-radius: 6px;
    padding: 0.5rem;
    color: var(--text-normal);
    font-size: 0.9rem;
    outline: none;
    transition: border-color 0.2s;
  }
  .wfm-filter-group select:focus {
    border-color: var(--interactive-accent);
  }
  .wfm-grid-list {
    display: flex;
    flex-direction: column;
    gap: 2rem;
  }
  .wfm-card {
    display: grid;
    grid-template-columns: auto 1fr;
    gap: 2rem;
    background: var(--background-secondary);
    border: 1px solid var(--border-color);
    border-radius: 16px;
    padding: 1.5rem;
    box-shadow: var(--shadow-m);
  }
  @media (max-width: 768px) {
    .wfm-card {
      grid-template-columns: 1fr;
    }
  }
  .wfm-matrix-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
  }
  .wfm-matrix-title {
    font-size: 0.8rem;
    font-weight: bold;
    color: var(--text-muted);
    text-transform: uppercase;
  }
  .wfm-table-grid {
    border-collapse: separate;
    border-spacing: 4px;
    margin: 0 auto;
  }
  .wfm-cell {
    width: 44px;
    height: 44px;
    border-radius: 6px;
    text-align: center;
    vertical-align: middle;
    font-size: 0.75rem;
    font-weight: bold;
    color: #ffffff;
    cursor: pointer;
    position: relative;
    transition: transform 0.15s, box-shadow 0.15s;
  }
  .wfm-cell:hover {
    transform: scale(1.1);
    z-index: 10;
  }
  .wfm-cell-pass {
    background-color: #1b4332;
    border: 1px solid #2d6a4f;
  }
  .wfm-cell-warn {
    background-color: #7f5539;
    border: 1px solid #9c6644;
  }
  .wfm-cell-fail {
    background-color: #5f0f0f;
    border: 1px solid #8c1c1c;
  }
  .wfm-cell-selected {
    border: 3px solid #06b6d4 !important;
    box-shadow: 0 0 14px #06b6d4;
    transform: scale(1.12);
    z-index: 5;
  }
  .wfm-cell-tooltip {
    display: none;
    position: absolute;
    bottom: 125%;
    left: 50%;
    transform: translateX(-50%);
    background: #000000;
    color: #ffffff;
    padding: 0.4rem 0.6rem;
    border-radius: 4px;
    font-size: 0.7rem;
    white-space: nowrap;
    z-index: 20;
    box-shadow: 0 4px 6px rgba(0,0,0,0.3);
  }
  .wfm-cell:hover .wfm-cell-tooltip {
    display: block;
  }
  .wfm-details-panel {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    gap: 1rem;
  }
  .wfm-details-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    border-bottom: 1px solid var(--border-color);
    padding-bottom: 0.5rem;
  }
  .wfm-strat-title {
    font-size: 1.2rem;
    font-weight: 700;
    margin: 0;
    color: var(--text-normal);
  }
  .wfm-badge {
    padding: 0.25rem 0.6rem;
    border-radius: 20px;
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
  }
  .badge-pass {
    background-color: rgba(16, 185, 129, 0.12);
    color: #10b981;
    border: 1px solid rgba(16, 185, 129, 0.25);
  }
  .badge-warn {
    background-color: rgba(245, 158, 11, 0.12);
    color: #f59e0b;
    border: 1px solid rgba(245, 158, 11, 0.25);
  }
  .badge-fail {
    background-color: rgba(239, 68, 68, 0.12);
    color: #ef4444;
    border: 1px solid rgba(239, 68, 68, 0.25);
  }
  .wfm-meta-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
    gap: 0.8rem;
  }
  .wfm-meta-item {
    display: flex;
    flex-direction: column;
  }
  .wfm-meta-label {
    font-size: 0.65rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }
  .wfm-meta-value {
    font-size: 0.85rem;
    font-weight: 600;
  }
  .wfm-warnings-section {
    background: rgba(255,255,255,0.02);
    padding: 0.8rem;
    border-radius: 8px;
    border-left: 4px solid var(--interactive-accent);
  }
  .wfm-warnings-title {
    font-size: 0.75rem;
    font-weight: bold;
    color: var(--text-muted);
    margin-bottom: 0.3rem;
    text-transform: uppercase;
  }
  .wfm-warnings-list {
    margin: 0;
    padding-left: 1.2rem;
    font-size: 0.8rem;
  }
  .wfm-action-bar {
    display: flex;
    justify-content: flex-end;
    align-items: center;
    gap: 0.8rem;
    margin-top: 1rem;
  }
  .wfm-download-btn {
    background-color: var(--interactive-accent);
    color: var(--text-on-accent);
    padding: 0.5rem 1rem;
    border-radius: 6px;
    font-weight: 600;
    text-decoration: none;
    font-size: 0.8rem;
  }
  .wfm-download-btn:hover {
    background-color: var(--interactive-accent-hover);
  }
  .wfm-cmd-box {
    font-family: var(--font-monospace);
    font-size: 0.75rem;
    background: rgba(0, 0, 0, 0.2);
    padding: 0.4rem 0.8rem;
    border-radius: 4px;
    cursor: pointer;
    border: 1px solid var(--border-color);
    transition: background-color 0.2s;
  }
  .wfm-cmd-box:hover {
    background: rgba(0, 0, 0, 0.3);
  }
`;

// Recuperar filtros únicos
const uniqueWaves = [...new Set(pages.map(p => p.wave_key).filter(Boolean))].sort();
const uniqueInstruments = [...new Set(pages.map(p => p.instrument).filter(Boolean))].sort();
const uniqueDirections = [...new Set(pages.map(p => p.direction).filter(Boolean))].sort();
const uniqueVersions = [...new Set(pages.map(p => p.version).filter(Boolean))].sort();
const uniqueVerdicts = ["ALL", "PASS", "WARN", "FAIL"];

// Renderizar panel de filtros
const filtersPanel = mainContainer.createEl("div", { cls: "wfm-filters-panel" });

function createFilter(label, options, defaultValue) {
  const group = filtersPanel.createEl("div", { cls: "wfm-filter-group" });
  group.createEl("label").textContent = label;
  const select = group.createEl("select");
  
  if (label !== "Verdict" && label !== "Wave") {
    const optAll = select.createEl("option");
    optAll.value = "ALL";
    optAll.textContent = "ALL";
  }
  
  options.forEach(opt => {
    const option = select.createEl("option");
    option.value = opt;
    option.textContent = opt;
    if (opt === defaultValue) option.selected = true;
  });
  return select;
}

const waveSelect = createFilter("Wave", uniqueWaves, uniqueWaves[uniqueWaves.length - 1]);
const instSelect = createFilter("Instrument", uniqueInstruments, "ALL");
const dirSelect = createFilter("Direction", uniqueDirections, "ALL");
const verSelect = createFilter("Version", uniqueVersions, "ALL");
const verdictSelect = createFilter("Verdict", uniqueVerdicts, "ALL");

const listContainer = mainContainer.createEl("div", { cls: "wfm-grid-list" });

function renderDashboard() {
  listContainer.innerHTML = "";
  
  const selectedWave = waveSelect.value;
  const selectedInst = instSelect.value;
  const selectedDir = dirSelect.value;
  const selectedVer = verSelect.value;
  const selectedVerdict = verdictSelect.value;
  
  const filteredPages = pages.filter(p => {
    if (p.wave_key != selectedWave) return false;
    if (selectedInst !== "ALL" && p.instrument !== selectedInst) return false;
    if (selectedDir !== "ALL" && p.direction !== selectedDir) return false;
    if (selectedVer !== "ALL" && p.version !== selectedVer) return false;
    if (selectedVerdict !== "ALL" && p.verdict !== selectedVerdict) return false;
    return true;
  });
  
  if (filteredPages.length === 0) {
    listContainer.createEl("p").textContent = "No se encontraron estrategias que cumplan con los filtros activos.";
    return;
  }
  
  filteredPages.forEach(p => {
    const card = listContainer.createEl("div", { cls: "wfm-card" });
    
    // Contenedor de Matriz
    const matrixWrapper = card.createEl("div", { cls: "wfm-matrix-wrapper" });
    matrixWrapper.createEl("div", { cls: "wfm-matrix-title" }).textContent = "Walk-Forward Matrix";
    
    const table = matrixWrapper.createEl("table", { cls: "wfm-table-grid" });
    const cells = p.matrix && p.matrix.cells ? p.matrix.cells : [];
    
    const runsList = [...new Set(cells.map(c => c.runs))].sort((a,b) => b-a);
    const oosList = [...new Set(cells.map(c => c.oos))].sort((a,b) => a-b);
    
    // Cabecera OOS
    const headerRow = table.createEl("tr");
    headerRow.createEl("th").textContent = "R\\O";
    oosList.forEach(oos => {
      headerRow.createEl("th", { attr: { style: "font-size:0.65rem; color:var(--text-muted); font-weight:normal;" } }).textContent = oos + "%";
    });
    
    // Filas Runs
    runsList.forEach(runs => {
      const row = table.createEl("tr");
      row.createEl("td", { attr: { style: "font-weight:bold; font-size:0.7rem; text-align:right; padding-right:6px;" } }).textContent = runs;
      
      oosList.forEach(oos => {
        const cellData = cells.find(c => c.runs === runs && c.oos === oos);
        const cell = row.createEl("td");
        
        if (cellData) {
          const passClass = cellData.passed ? "wfm-cell-pass" : "wfm-cell-fail";
          cell.className = `wfm-cell ${passClass}`;
          cell.textContent = cellData.ret_dd.toFixed(1);
          
          const tooltip = cell.createEl("div", { cls: "wfm-cell-tooltip" });
          tooltip.textContent = `Runs: ${runs} | OOS: ${oos}% | Passed: ${cellData.passed} | Ret/DD: ${cellData.ret_dd.toFixed(2)}`;
          
          const isSelected = p.selected_run === `${runs}_${oos}`;
          if (isSelected) {
            cell.classList.add("wfm-cell-selected");
          }
        } else {
          cell.className = "wfm-cell";
          cell.textContent = "-";
        }
      });
    });
    
    // Panel de detalles
    const details = card.createEl("div", { cls: "wfm-details-panel" });
    
    const dHeader = details.createEl("div", { cls: "wfm-details-header" });
    const titleGroup = dHeader.createEl("div");
    titleGroup.createEl("h3", { cls: "wfm-strat-title" }).textContent = p.strategy_id;
    
    const badgeColor = p.verdict === "PASS" ? "badge-pass" : (p.verdict === "WARN" ? "badge-warn" : "badge-fail");
    dHeader.createEl("span", { cls: `wfm-badge ${badgeColor}` }).textContent = p.verdict;
    
    const metaGrid = details.createEl("div", { cls: "wfm-meta-grid" });
    
    function addMeta(label, val) {
      const item = metaGrid.createEl("div", { cls: "wfm-meta-item" });
      item.createEl("span", { cls: "wfm-meta-label" }).textContent = label;
      item.createEl("span", { cls: "wfm-meta-value" }).textContent = val || "-";
    }
    
    addMeta("Instrumento", p.instrument);
    addMeta("Dirección", p.direction);
    addMeta("Timeframe", p.timeframe);
    addMeta("Tipo Lógico", p.logical_type);
    addMeta("Versión", p.version);
    addMeta("Selected Run", p.selected_run);
    addMeta("Selection Score", p.selection_score ? p.selection_score.toFixed(4) : "0.0000");

    // Warnings
    const fileWarnings = p.warnings ? p.warnings : [];
    if (fileWarnings.length > 0) {
      const warnSec = details.createEl("div", { cls: "wfm-warnings-section" });
      warnSec.createEl("div", { cls: "wfm-warnings-title" }).textContent = "Estabilidad / Warnings";
      const warnList = warnSec.createEl("ul", { cls: "wfm-warnings-list" });
      fileWarnings.forEach(w => {
        warnList.createEl("li").textContent = w;
      });
    }
    
    // Acciones
    const actionBar = details.createEl("div", { cls: "wfm-action-bar" });
    
    const cmdText = `symphony download-wave --wave ${p.wave_key} --dest ~/Desktop/SQX`;
    const cmdBox = actionBar.createEl("code", { 
      cls: "wfm-cmd-box",
      attr: { 
        title: "Haz clic para copiar el comando de descarga"
      }
    });
    cmdBox.textContent = `symphony download-wave --wave ${p.wave_key}`;
    cmdBox.addEventListener("click", () => {
      navigator.clipboard.writeText(cmdText);
      new Notice("Comando de descarga copiado al portapapeles");
    });
    
    const fileLink = actionBar.createEl("a", { 
      cls: "wfm-download-btn", 
      attr: { 
        href: `obsidian://open?vault=${encodeURIComponent(app.vault.getName())}&file=${encodeURIComponent(p.file.path)}`
      } 
    });
    fileLink.textContent = "Ver Reporte Completo";
  });
}

// Bindeo de eventos
waveSelect.addEventListener("change", renderDashboard);
instSelect.addEventListener("change", renderDashboard);
dirSelect.addEventListener("change", renderDashboard);
verSelect.addEventListener("change", renderDashboard);
verdictSelect.addEventListener("change", renderDashboard);

// Render inicial
renderDashboard();
```
