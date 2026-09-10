#!/usr/bin/env python3
"""Render the AGENTS OS Grid report from its JSON source.

Self-contained by design: no external generator, no network, no CSS/JS
dependencies. Data and presentation stay separate — the JSON travels embedded in
the page and the layout renders from it, so reordering the report can never
change a number.

    python3 build-grid.py [--source FILE] [--output FILE]
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

CSS = """
:root{
  --bg:#0e1117; --panel:#151a24; --panel-2:#1b2130; --border:#262d3d;
  --text:#e7ebf3; --muted:#98a2b8; --faint:#6b7488;
  --green:#3fb950; --amber:#d29922; --red:#f85149; --blue:#58a6ff;
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--text);
  font:15px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Roboto,Helvetica,Arial,sans-serif;
  -webkit-font-smoothing:antialiased}
a{color:var(--blue)}
.wrap{max-width:960px;margin:0 auto;padding:0 20px}
header{border-bottom:1px solid var(--border);background:linear-gradient(160deg,#121722,#0e1117)}
header .wrap{padding:40px 20px 34px}
.kicker{color:var(--green);font-size:11px;font-weight:700;letter-spacing:.14em;text-transform:uppercase}
h1{font-size:31px;line-height:1.15;margin:10px 0 12px;letter-spacing:-.02em}
.lede{color:var(--muted);font-size:15px;max-width:720px;margin:0}
.stamp{margin-top:18px;display:flex;gap:10px;flex-wrap:wrap;align-items:center}
.chip{border:1px solid var(--border);background:var(--panel);color:var(--muted);
  border-radius:999px;padding:4px 12px;font-size:12px}
.basis{margin:16px 0 0;color:var(--faint);font-size:12.5px;max-width:720px}
.metrics{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin:26px 0 0}
.metric{background:var(--panel);border:1px solid var(--border);border-radius:12px;padding:16px 14px;min-width:0}
.metric b{display:block;font-size:26px;line-height:1.1;letter-spacing:-.02em}
.metric span{display:block;color:var(--muted);font-size:12.5px;margin-top:5px}
.metric em{display:block;color:var(--faint);font-size:11.5px;font-style:normal;margin-top:3px}
section{padding:36px 0 0}
h2{font-size:19px;margin:0 0 6px;letter-spacing:-.01em}
.sub{color:var(--muted);font-size:13.5px;margin:0 0 18px;max-width:740px}
.claim{background:var(--panel-2);border:1px solid var(--border);border-left:3px solid var(--green);
  border-radius:10px;padding:16px 18px;margin:0 0 14px}
.claim p{margin:0;font-size:16px}
.claim p+p{margin-top:9px;color:var(--muted);font-size:14px}
.grid2{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
.card{background:var(--panel);border:1px solid var(--border);border-radius:12px;padding:15px 16px;min-width:0}
.card h3{margin:0 0 5px;font-size:14px}
.card p{margin:0;color:var(--muted);font-size:13.5px}
.row{background:var(--panel);border:1px solid var(--border);border-radius:12px;padding:16px 18px;margin-bottom:11px}
.row-top{display:flex;gap:12px;align-items:flex-start;flex-wrap:wrap}
.row-top h3{margin:0;font-size:15.5px;flex:1 1 380px;min-width:0}
.pill{border-radius:999px;padding:3px 11px;font-size:11px;font-weight:700;letter-spacing:.04em;
  text-transform:uppercase;white-space:nowrap;flex:none}
.pill.cumplida{background:rgba(63,185,80,.16);color:var(--green);border:1px solid rgba(63,185,80,.35)}
.pill.parcial{background:rgba(210,153,34,.16);color:var(--amber);border:1px solid rgba(210,153,34,.35)}
.pill.no-cumplida{background:rgba(248,81,73,.14);color:var(--red);border:1px solid rgba(248,81,73,.32)}
.verdict{margin:9px 0 0;font-size:14px;color:var(--text)}
.ev{margin:9px 0 0;color:var(--muted);font-size:13.5px}
.cav{margin:9px 0 0;padding-left:12px;border-left:2px solid var(--border);color:var(--faint);font-size:13px}
.scores{display:flex;flex-direction:column;gap:9px}
.score{display:flex;align-items:center;gap:14px;background:var(--panel);border:1px solid var(--border);
  border-radius:10px;padding:12px 16px;flex-wrap:wrap}
.score .n{flex:1 1 200px;min-width:0;font-size:14px}
.score .bar{flex:1 1 200px;height:7px;border-radius:999px;background:var(--panel-2);overflow:hidden;min-width:120px}
.score .bar i{display:block;height:100%;border-radius:999px}
.score .v{font-variant-numeric:tabular-nums;font-weight:700;font-size:15px;width:44px;text-align:right;flex:none}
.score .t{color:var(--faint);font-size:12px;width:132px;text-align:right;flex:none}
.good i{background:var(--green)} .ok i{background:var(--amber)} .bad i{background:var(--red)}
.good .v{color:var(--green)} .ok .v{color:var(--amber)} .bad .v{color:var(--red)}
.list{list-style:none;padding:0;margin:0}
.list li{background:var(--panel);border:1px solid var(--border);border-radius:12px;
  padding:14px 16px;margin-bottom:10px}
.list li b{display:block;font-size:14.5px;margin-bottom:4px}
.list li span{color:var(--muted);font-size:13.5px}
.list.done li{border-left:3px solid var(--green)}
.list.todo li{border-left:3px solid var(--amber)}
.list.lim li{border-left:3px solid var(--faint)}
footer{margin-top:44px;border-top:1px solid var(--border)}
footer .wrap{padding:20px;color:var(--faint);font-size:12.5px;text-align:center}
@media (max-width:820px){
  h1{font-size:26px}
  .metrics{grid-template-columns:repeat(2,minmax(0,1fr))}
  .grid2{grid-template-columns:1fr}
  .score .t{width:100%;text-align:left}
}
@media (max-width:520px){
  header .wrap{padding:28px 16px 24px}
  .wrap{padding:0 16px}
  .metrics{grid-template-columns:1fr}
}
"""

JS = """
const data = JSON.parse(document.getElementById('data').textContent);
const esc = s => String(s).replace(/[&<>]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
const el = (sel, html) => { document.querySelector(sel).innerHTML = html; };

el('#kicker', esc(data.meta.snapshot));
el('#title', esc(data.meta.title));
el('#lede', esc(data.meta.subtitle));
el('#basis', esc(data.meta.basis));
el('#foot', esc(data.meta.footer));

el('#metrics', data.headline.map(m =>
  `<div class="metric"><b>${esc(m.value)}</b><span>${esc(m.label)}</span><em>${esc(m.note)}</em></div>`
).join(''));

el('#claim', `<p>${esc(data.thesis.claim)}</p><p>${esc(data.thesis.body)}</p>`);
el('#pillars', data.thesis.pillars.map(p =>
  `<div class="card"><h3>${esc(p.title)}</h3><p>${esc(p.text)}</p></div>`
).join(''));

el('#reality', data.reality.map(r => `
  <div class="row">
    <div class="row-top">
      <h3>${esc(r.promise)}</h3>
      <span class="pill ${esc(r.status)}">${esc(r.status.replace('-', ' '))}</span>
    </div>
    <p class="verdict">${esc(r.verdict)}</p>
    <p class="ev">${esc(r.evidence)}</p>
    <p class="cav">${esc(r.caveat)}</p>
  </div>`).join(''));

el('#scores-caption', esc(data.scores.caption));
el('#scores', data.scores.rows.map(s => `
  <div class="score ${esc(s.state)}">
    <div class="n">${esc(s.name)}</div>
    <div class="bar"><i style="width:${(s.value / 5 * 100).toFixed(1)}%"></i></div>
    <div class="v">${s.value.toFixed(2).replace('.', ',')}</div>
    <div class="t">${esc(s.trend)}</div>
  </div>`).join(''));

const listOf = (block, cls) => block.items.map(i =>
  `<li><b>${esc(i.title)}</b><span>${esc(i.text)}</span></li>`).join('');

el('#closed-caption', esc(data.closed.caption));
el('#closed', listOf(data.closed));
el('#open-caption', esc(data.open.caption));
el('#open', listOf(data.open));
el('#limits-caption', esc(data.limits.caption));
el('#limits', listOf(data.limits));
"""

TEMPLATE = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<style>{css}</style>
</head>
<body>
<script type="application/json" id="data">{payload}</script>

<header>
  <div class="wrap">
    <div class="kicker" id="kicker"></div>
    <h1 id="title"></h1>
    <p class="lede" id="lede"></p>
    <div class="stamp">
      <span class="chip">Promesa vs. evidencia</span>
      <span class="chip">Sin cifras estimadas</span>
      <span class="chip">Markdown como fuente de verdad</span>
    </div>
    <p class="basis" id="basis"></p>
    <div class="metrics" id="metrics"></div>
  </div>
</header>

<div class="wrap">
  <section>
    <h2>La tesis</h2>
    <div class="claim" id="claim"></div>
    <div class="grid2" id="pillars"></div>
  </section>

  <section>
    <h2>Promesa vs. estado real</h2>
    <p class="sub">Cada fila declara el veredicto, la evidencia que lo sostiene y la salvedad que lo limita. Ninguna cifra es estimada: sale del agregado de feedbacks o de un gate ejecutable.</p>
    <div id="reality"></div>
  </section>

  <section>
    <h2>Los números</h2>
    <p class="sub" id="scores-caption"></p>
    <div class="scores" id="scores"></div>
  </section>

  <section>
    <h2>Lo que se cerró en esta corrida</h2>
    <p class="sub" id="closed-caption"></p>
    <ul class="list done" id="closed"></ul>
  </section>

  <section>
    <h2>Lo que sigue abierto</h2>
    <p class="sub" id="open-caption"></p>
    <ul class="list todo" id="open"></ul>
  </section>

  <section>
    <h2>Límites honestos</h2>
    <p class="sub" id="limits-caption"></p>
    <ul class="list lim" id="limits"></ul>
  </section>
</div>

<footer><div class="wrap" id="foot"></div></footer>
<script>{js}</script>
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=HERE / "agents-os-grid.source.json")
    parser.add_argument("--output", type=Path, default=HERE / "agents-os-grid.html")
    args = parser.parse_args()

    data = json.loads(args.source.read_text(encoding="utf-8"))
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    html = TEMPLATE.format(
        title=data["meta"]["title"],
        css=CSS.strip(),
        js=JS.strip(),
        payload=payload,
    )
    args.output.write_text(html, encoding="utf-8")
    print(f"source: {args.source.name}")
    print(f"output: {args.output.name} ({len(html.encode('utf-8'))} bytes)")


if __name__ == "__main__":
    main()
