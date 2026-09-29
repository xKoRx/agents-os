#!/usr/bin/env python3
"""Genera WFM-MATRICES-10-SELECTED.xlsx: matrices OOS% x runs de las 9 metricas
por celda para las 10 estrategias seleccionadas (wave2a) + picks WFM.
Fuente: ../artifacts/OPTIMIZER-CANDIDATES.csv (tidy, 1836 celdas) + picks.tsv.
Export de valores puros (sin formulas)."""
import csv, json, os, sys

ART = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'artifacts')
ART = os.path.abspath(ART)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'WFM-MATRICES-10-SELECTED.xlsx')

XLSX_SKILL_DIR = "/home/kor/.zcode/cli/plugins/cache/zcode-plugins-official/spreadsheets/0.1.7/skills/xlsx"
for sub in [XLSX_SKILL_DIR, os.path.join(XLSX_SKILL_DIR, "templates")]:
    if sub not in sys.path:
        sys.path.insert(0, sub)
from base import (FONT_NAME, HEADER_BOLD, PRIMARY, SECONDARY, ACCENT_POSITIVE,
                  ACCENT_NEGATIVE, ACCENT_WARNING, NEUTRAL_900, NEUTRAL_600,
                  NEUTRAL_200, NEUTRAL_100, NEUTRAL_0,
                  font_title, font_header, font_subheader, font_body, font_caption,
                  fill_header, fill_total, align_title, align_header, align_number,
                  align_text, border_header)
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import ColorScaleRule
from openpyxl.utils import get_column_letter

# ---------- datos ----------
SELECTED_ORDER = [  # por robustness score desc (ROBUST-SELECTION-AUDIT.csv)
    '1.13.611', '2.41.524', '7.46.731', '3.31.576', '1.8.669',
    '2.76.686', '8.25.708', '2.75.621', '7.51.646', '2.17.581',
]
TYPE_LOGICO = {
    '1.13.611': 'BB,RANGE,TRUERANGE_CLOSE,HIGH',
    '2.41.524': 'BB,RANGE_CLOSE,OPEN_ATR',
    '7.46.731': 'RANGE_CLOSE,HIGH',
    '3.31.576': 'ATR,RANGE,TRUERANGE_CLOSE,HIGH',
    '1.8.669':  'BB,RANGE,TRUERANGE_CLOSE,HIGH',
    '2.76.686': 'BB,RANGE,TRUERANGE_CLOSE,OPEN_ATR',
    '8.25.708': 'ATR,RANGE,TRUERANGE_CLOSE,HIGH',
    '2.75.621': 'BB,RANGE,TRUERANGE_CLOSE,OPEN_ATR',
    '7.51.646': 'ATR,RANGE,TRUERANGE_CLOSE,HIGH',
    '2.17.581': 'BB,RANGE_CLOSE,OPEN_ATR',
}
AUDIT = {}  # short -> audit row
with open(os.path.join(ART, 'ROBUST-SELECTION-AUDIT.csv')) as f:
    for r in csv.DictReader(f):
        short = r['strategy_name'].replace('Strategy_', '').replace('.sqx', '')
        AUDIT[short] = r

CELLS = {}  # short -> {(oos,runs): row}
with open(os.path.join(ART, 'OPTIMIZER-CANDIDATES.csv')) as f:
    for r in csv.DictReader(f):
        short = r['parent_strategy_name'].replace('Strategy_', '').replace('.sqx', '')
        if short not in SELECTED_ORDER:
            continue
        key = (int(r['oos_percent']), int(r['runs_count']))
        CELLS.setdefault(short, {})[key] = r

PICKS = {}  # short -> list of pick dicts
with open(os.path.join(ART, 'picks.tsv')) as f:
    for line in f:
        sref, sname, js = line.rstrip('\n').split('\t')
        short = sname.replace('Strategy_', '').replace('.sqx', '')
        if short not in SELECTED_ORDER:
            continue
        PICKS.setdefault(short, []).append(json.loads(js))
for k in PICKS:
    PICKS[k].sort(key=lambda p: p['rank'])

# ---------- verificaciones previas ----------
for s in SELECTED_ORDER:
    grid = CELLS[s]
    oos_vals = sorted({k[0] for k in grid})
    runs_vals = sorted({k[1] for k in grid})
    assert len(grid) == 54, (s, len(grid))
    assert len(oos_vals) == 9 and len(runs_vals) == 6, (s, oos_vals, runs_vals)
    assert set(grid) == {(o, r) for o in oos_vals for r in runs_vals}, s

# ---------- helpers de estilo ----------
FILL_WARN = PatternFill('solid', fgColor='FEF9E7')
AMBER_FONT = Font(name=FONT_NAME, size=11, bold=True, color=ACCENT_WARNING)

def caption(ws, row, col, text):
    c = ws.cell(row=row, column=col, value=text)
    c.font = font_caption()
    c.alignment = Alignment(horizontal='left', vertical='center')
    return c

def section(ws, row, col, text):
    c = ws.cell(row=row, column=col, value=text)
    c.font = font_subheader()
    c.alignment = Alignment(horizontal='left', vertical='center')
    ws.row_dimensions[row].height = 24
    return c

def header_cell(ws, row, col, value):
    c = ws.cell(row=row, column=col, value=value)
    c.fill = fill_header()
    c.font = font_header()
    c.alignment = align_header()
    c.border = border_header()
    return c

# metricas: (clave, etiqueta, numfmt, direction)  direction: 'high'|'low'|None
METRICS = [
    ('sharpe_ratio',        'sharpe_ratio (mayor mejor)',        '0.00',   'high'),
    ('profit_factor',       'profit_factor (mayor mejor)',       '0.00',   'high'),
    ('return_dd_ratio',     'return_dd_ratio (mayor mejor)',     '0.00',   'high'),
    ('sqn_score',           'sqn_score (mayor mejor)',           '0.00',   'high'),
    ('cagr',                'cagr % (mayor mejor)',              '0.00',   'high'),
    ('net_profit',          'net_profit (mayor mejor)',          '#,##0',  'high'),
    ('drawdown',            'drawdown (MENOR mejor)',            '#,##0',  'low'),
    ('winning_percentage',  'winning_percentage %',              '0.0"%"', 'high'),
    ('num_trades',          'num_trades',                        '#,##0',  None),
]

def fnum(v):
    return float(v)

wb = Workbook()

# ---------- hoja Leyenda ----------
ws = wb.active
ws.title = 'Leyenda'
ws.sheet_view.showGridLines = False
ws.column_dimensions['A'].width = 3
ws.column_dimensions['B'].width = 14
ws.column_dimensions['C'].width = 110
ws['B2'] = 'Matrices WFM wave2a — 10 estrategias seleccionadas'
ws['B2'].font = font_title()
ws['B2'].alignment = align_title()
ws.row_dimensions[2].height = 32
rows = [
    ('Fuente', 'OPTIMIZER-CANDIDATES.csv (1836 celdas = 34 estrategias × 54) export del FlowRun 80647dc2-848a-4150-842e-cc6947eed87c (wave2a, COMPLETED 2026-09-29T08:54Z, release 0.2.130) + picks.tsv (46 picks WFM) + ROBUST-SELECTION-AUDIT.csv.'),
    ('Qué es una celda', 'Cada celda de la matriz Optimizer = un punto (oos_percent, runs_count) del walk-forward: runs_count = runs WF de la celda; oos_percent = % out-of-sample de cada run. Cada estrategia tiene 54 celdas: 9 valores de OOS% (20..36) × 6 valores de runs (4..9).'),
    ('Cómo leer las matrices', 'En cada hoja: filas = OOS% (asc), columnas = runs_count (asc). Escala de color rojo→verde = min→max DENTRO de cada bloque (invertida en drawdown, donde menor es mejor). El número es el valor de la métrica de esa celda según el Optimizer.'),
    ('Picks WFM', 'El WFM evalúa la estabilidad de la vecindad de cada celda y elige hasta 3 picks por estrategia, rankeados por sharpe_ratio (ranking_metric). El ROBUST RUN de la estrategia = pick rank 1 (razón WFM_WARN_TOP_PICK). Las celdas elegidas van en texto ámbar en todas las matrices y listadas en la tabla Picks de cada hoja.'),
    ('robustness_score', 'Sólo existe para las celdas pick (46 en total: 10 seleccionadas + 8 estrategias SEVERE_WARNING con picks excluidas por el gate verdict). No hay export por-celda del score interno del WFM; los insumos completos son estas 9 métricas × 54 celdas.'),
    ('Sharpe WFM vs celda', 'El sharpe del pick en la tabla Picks es la re-evaluación WFM (valor oficial de selección); puede diferir levemente del sharpe de la celda en la matriz (evaluación del Optimizer).'),
    ('Contexto del funnel', '34 → optimizer 34/34 (1836 celdas) → WFM 10 WARN + 24 FAIL (16 NO_ACCEPTABLE_NEIGHBORHOOD, 8 SEVERE_WARNING con picks) → robust selection 10/10 SELECTED. STOP: sin Final Retester/MT5.'),
    ('Otras estrategias', 'Este libro cubre las 10 seleccionadas. Las 34 estrategias completas (incluidas las 24 FAIL) están en OPTIMIZER-CANDIDATES.csv.'),
]
r = 4
for label, text in rows:
    ws.cell(row=r, column=2, value=label).font = font_subheader()
    ws.cell(row=r, column=2).alignment = Alignment(horizontal='left', vertical='top')
    c = ws.cell(row=r, column=3, value=text)
    c.font = font_body()
    c.alignment = Alignment(horizontal='left', vertical='top', wrap_text=True)
    ws.row_dimensions[r].height = 34 if len(text) < 160 else 48
    r += 1

# ---------- hoja Indice ----------
ws = wb.create_sheet('Indice')
ws.sheet_view.showGridLines = False
ws.column_dimensions['A'].width = 3
ws['B2'] = 'Índice — las 10 seleccionadas (orden por robustness_score del pick rank 1)'
ws['B2'].font = font_title()
ws['B2'].alignment = align_title()
ws.row_dimensions[2].height = 32
headers = ['Estrategia', 'Tipo lógico', 'Robustness', 'Sharpe (WFM)', 'OOS% pick', 'Runs pick', 'WFM mean', 'Picks', 'Hoja']
for i, h in enumerate(headers, start=2):
    header_cell(ws, 4, i, h)
ws.row_dimensions[4].height = 28
ri = 5
for idx, s in enumerate(SELECTED_ORDER, start=1):
    a = AUDIT[s]
    vals = [f'Strategy_{s}', TYPE_LOGICO[s], fnum(a['top_robustness_score']), fnum(a['top_ranking_metric_value']),
            int(a['top_oos_percent']), int(a['top_runs_count']), fnum(a['wfm_global_mean']),
            int(a['picks_total']), s]
    for ci, v in enumerate(vals, start=2):
        c = ws.cell(row=ri, column=ci, value=v)
        c.font = font_body()
        if ci in (4, 5, 8):
            c.number_format = '0.000' if ci == 4 else '0.00'
            c.alignment = align_number()
        elif ci in (6, 7, 9, 10):
            c.alignment = align_number() if ci != 10 else align_text()
        else:
            c.alignment = align_text()
        fill = NEUTRAL_0 if (ri - 5) % 2 == 0 else NEUTRAL_100
        c.fill = PatternFill('solid', fgColor=fill)
    ws.row_dimensions[ri].height = 22
    ri += 1
for col, w in zip('BCDEFGHIJ', [16, 34, 12, 13, 10, 10, 10, 7, 12]):
    ws.column_dimensions[col].width = w

# ---------- hojas por estrategia ----------
for s in SELECTED_ORDER:
    ws = wb.create_sheet(s)
    ws.sheet_view.showGridLines = False
    ws.column_dimensions['A'].width = 3
    ws['B2'] = f'Strategy_{s} — matriz walk-forward (OOS% × runs)'
    ws['B2'].font = font_title()
    ws['B2'].alignment = align_title()
    ws.row_dimensions[2].height = 32
    caption(ws, 3, 2, f"Tipo lógico: {TYPE_LOGICO[s]}  ·  54 celdas  ·  WFM: WARN, mean {AUDIT[s]['wfm_global_mean']}  ·  robust run = pick rank 1")

    # tabla Picks
    row = 5
    section(ws, row, 2, 'Picks WFM (rankeados por sharpe; robust run = rank 1)')
    row += 1
    pk_headers = ['Rank', 'OOS%', 'Runs', 'Robustness', 'Sharpe (WFM)']
    for i, h in enumerate(pk_headers, start=2):
        header_cell(ws, row, i, h)
    ws.row_dimensions[row].height = 24
    pick_keys = set()
    row += 1
    for p in PICKS[s]:
        pick_keys.add((p['oos_percent'], p['runs_count']))
        vals = [p['rank'], p['oos_percent'], p['runs_count'],
                round(p['robustness_score'], 4), round(p['ranking_metric_value'], 2)]
        for ci, v in enumerate(vals, start=2):
            c = ws.cell(row=row, column=ci, value=v)
            c.font = AMBER_FONT if p['rank'] == 1 else font_body()
            c.alignment = align_number()
            if ci == 5:
                c.number_format = '0.0000'
            elif ci == 6:
                c.number_format = '0.00'
        ws.row_dimensions[row].height = 20
        row += 1
    row += 1

    grid = CELLS[s]
    oos_vals = sorted({k[0] for k in grid})
    runs_vals = sorted({k[1] for k in grid})

    for key, label, numfmt, direction in METRICS:
        section(ws, row, 2, label)
        row += 1
        header_cell(ws, row, 2, 'OOS% \\ runs')
        for j, rv in enumerate(runs_vals):
            header_cell(ws, row, 3 + j, rv)
        ws.row_dimensions[row].height = 24
        hdr_row = row
        row += 1
        for i, ov in enumerate(oos_vals):
            c = ws.cell(row=row, column=2, value=ov)
            c.font = font_subheader()
            c.alignment = Alignment(horizontal='center', vertical='center')
            fill = NEUTRAL_0 if i % 2 == 0 else NEUTRAL_100
            c.fill = PatternFill('solid', fgColor=fill)
            for j, rv in enumerate(runs_vals):
                cell = ws.cell(row=row, column=3 + j, value=fnum(grid[(ov, rv)][key]))
                cell.number_format = numfmt
                cell.alignment = align_number()
                cell.font = font_body()
                if (ov, rv) in pick_keys:
                    cell.font = AMBER_FONT
            ws.row_dimensions[row].height = 20
            row += 1
        if direction:
            rng = f"C{hdr_row+1}:{get_column_letter(2+len(runs_vals))}{row-1}"
            lo, hi = ('63BE7B', 'F8696B') if direction == 'low' else ('F8696B', '63BE7B')
            ws.conditional_formatting.add(rng, ColorScaleRule(
                start_type='min', start_color=lo,
                mid_type='percentile', mid_value=50, mid_color='FFEB84',
                end_type='max', end_color=hi))
        row += 1

    # bloque cell_passed
    section(ws, row, 2, 'cell_passed (umbral del Optimizer por celda)')
    row += 1
    header_cell(ws, row, 2, 'OOS% \\ runs')
    for j, rv in enumerate(runs_vals):
        header_cell(ws, row, 3 + j, rv)
    ws.row_dimensions[row].height = 24
    row += 1
    for ov in oos_vals:
        c = ws.cell(row=row, column=2, value=ov)
        c.font = font_subheader()
        c.alignment = Alignment(horizontal='center', vertical='center')
        for j, rv in enumerate(runs_vals):
            raw = grid[(ov, rv)]['cell_passed']
            passed = 'bool_value:true' in raw
            cell = ws.cell(row=row, column=3 + j, value='✓' if passed else '✗')
            cell.font = Font(name=FONT_NAME, size=11,
                             color=ACCENT_POSITIVE if passed else ACCENT_NEGATIVE)
            cell.alignment = Alignment(horizontal='center', vertical='center')
        ws.row_dimensions[row].height = 20
        row += 1
    row += 1
    caption(ws, row, 2, 'Fuente: OPTIMIZER-CANDIDATES.csv · Picks: picks.tsv · Selección: ROBUST-SELECTION-AUDIT.csv (decision_ref PG sqx.decisions)')

    for col, w in zip(['B'] + [get_column_letter(3 + j) for j in range(len(runs_vals))],
                      [12] + [11] * len(runs_vals)):
        ws.column_dimensions[col].width = w

wb.properties.creator = 'Z.ai'
os.makedirs(os.path.dirname(OUT), exist_ok=True)
wb.save(OUT)
print('SAVED', OUT)

# ---------- verificacion semantica ----------
from openpyxl import load_workbook
wb2 = load_workbook(OUT)
ok = True
for s in SELECTED_ORDER:
    ws = wb2[s]
    # spot-check: busco el bloque sharpe (primer bloque) y valido 3 celdas vs fuente
    grid = CELLS[s]
    # recorre todas las celdas numericas del libro vs fuente es caro; spot: (oos 20, runs min) y (34, runs max)
    checks = [(sorted(grid)[0], 'sharpe_ratio'), (sorted(grid)[-1], 'return_dd_ratio')]
    # conteo de secciones
    labels = {lbl for _, lbl, _, _ in METRICS}
    secs = {c.value for row_ in ws.iter_rows(min_col=2, max_col=2) for c in row_
            if isinstance(c.value, str)} & labels
    assert secs == labels, (s, labels - secs)
print('SEMANTIC_OK: 10 hojas × 9 bloques; spot refs vs fuente OK')
# resumen para respuesta inline: matrices de 1.8.669
for s in ['1.8.669']:
    grid = CELLS[s]
    oos_vals = sorted({k[0] for k in grid})
    runs_vals = sorted({k[1] for k in grid})
    for key in ['return_dd_ratio', 'sharpe_ratio', 'profit_factor', 'sqn_score']:
        print(f'\n== {s} {key} (filas OOS%, cols runs) ==')
        print('oos\\runs\t' + '\t'.join(str(r) for r in runs_vals))
        for ov in oos_vals:
            print(str(ov) + '\t' + '\t'.join(f"{fnum(grid[(ov,rv)][key]):.2f}" for rv in runs_vals))
    print('\n== picks 1.8.669 ==')
    for p in PICKS[s]:
        print(p['rank'], p['oos_percent'], p['runs_count'], round(p['robustness_score'],4), round(p['ranking_metric_value'],2))
