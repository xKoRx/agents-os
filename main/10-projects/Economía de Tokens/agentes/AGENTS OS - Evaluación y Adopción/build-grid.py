#!/usr/bin/env python3
"""Build the AGENTS OS Grid report from its JSON source plus the SVG cover."""

import argparse
import base64
import importlib.util
import json
from pathlib import Path


POLISH = """
  /* Local Grid presentation polish */
  html,body{overflow-x:hidden}
  .header{padding:32px max(24px,calc((100vw - 1100px)/2));flex-wrap:wrap}
  .header-meta{flex:1 1 620px;min-width:0}
  .header-meta h1{font-size:30px;line-height:1.15;overflow-wrap:anywhere}
  .header-meta .sub{font-size:14px;max-width:760px}
  .score-ring{margin-left:auto}
  .container{max-width:1100px;margin:36px auto;padding:0 24px}
  .metrics-row{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px}
  .metric-card{min-width:0;padding:18px 14px}
  .section{margin-bottom:20px}
  .section-header{padding:16px 22px}
  .section-header h2{font-size:16px;line-height:1.3}
  .section-body{padding:18px 22px}
  .section-content{font-size:15px;line-height:1.65}
  .finding-body strong{font-size:14px}
  .finding-body span{font-size:13px;line-height:1.55}
  .finding-body span b{color:var(--text);font-weight:600}
  .item-list{margin:8px 0 12px}
  .architecture-cover{margin:0 0 32px;background:linear-gradient(145deg,#151a29,#0f1117);border:1px solid var(--border);border-radius:16px;overflow:hidden;box-shadow:0 18px 44px rgba(0,0,0,.28)}
  .architecture-cover-meta{padding:22px 24px 12px;display:flex;align-items:flex-end;justify-content:space-between;gap:20px;flex-wrap:wrap}
  .architecture-cover-kicker{color:var(--green);font-size:11px;font-weight:700;letter-spacing:.12em;text-transform:uppercase}
  .architecture-cover h2{font-size:21px;line-height:1.25;margin-top:5px}
  .architecture-cover p{max-width:690px;color:var(--muted);font-size:13px}
  .architecture-cover img{display:block;width:100%;height:auto;border-top:1px solid var(--border)}
  .reality-transition{margin:0 0 20px;padding:22px 4px 14px;border-bottom:1px solid var(--border)}
  .reality-transition span{color:var(--orange);font-size:11px;font-weight:700;letter-spacing:.12em;text-transform:uppercase}
  .reality-transition h2{font-size:22px;line-height:1.25;margin-top:5px}
  .reality-transition p{color:var(--muted);font-size:13px;margin-top:5px}
  @media (max-width:820px){
    .header{padding:24px}
    .header-meta h1{font-size:25px}
    .score-ring{margin-left:0}
    .metrics-row{grid-template-columns:repeat(2,minmax(0,1fr))}
  }
  @media (max-width:520px){
    .container{padding:0 14px;margin:20px auto}
    .metrics-row{grid-template-columns:1fr}
    .section-header,.section-body{padding:14px 16px}
  }
"""


def load_generator(path: Path):
    spec = importlib.util.spec_from_file_location("nexus_grid_generator", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--generator", required=True, type=Path)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--svg", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    generator = load_generator(args.generator)
    data = json.loads(args.source.read_text(encoding="utf-8"))
    html = generator.generate_report(data)
    svg64 = base64.b64encode(args.svg.read_bytes()).decode("ascii")

    cover = f"""
  <section class="architecture-cover" aria-labelledby="architecture-title">
    <div class="architecture-cover-meta">
      <div>
        <div class="architecture-cover-kicker">La promesa del sistema</div>
        <h2 id="architecture-title">Un agente que recupera lo justo, aprende de la operación y deja conocimiento reusable</h2>
      </div>
      <p>La Constitución gobierna; el Context Router selecciona contexto; Sistema 1 aprende cómo operar; LLM Wiki compila fuentes en Sistema 2; Graphify conecta sin reemplazar la fuente de verdad.</p>
    </div>
    <img src="data:image/svg+xml;base64,{svg64}" alt="Mapa de componentes y flujo de aprendizaje de AGENTS OS">
  </section>
  <div class="reality-transition">
    <span>Estado real y evidencia</span>
    <h2>Qué está listo, qué todavía no y dónde conviene invertir</h2>
    <p>La arquitectura es prometedora; la adopción de equipo depende ahora de evidencia comparativa, gobernanza y operación medible.</p>
  </div>
"""

    html = html.replace("</style>", POLISH + "\n</style>", 1)
    html = html.replace('<div class="container">\n  ', '<div class="container">\n' + cover + '  ', 1)
    footer_start = html.index('<div class="footer">')
    footer_end = html.index('</div>', footer_start) + len('</div>')
    html = html[:footer_start] + '<div class="footer">Baticoders · vis-nexus · 14 julio 2026</div>' + html[footer_end:]
    args.output.write_text(html, encoding="utf-8")


if __name__ == "__main__":
    main()
