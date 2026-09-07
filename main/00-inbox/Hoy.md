---
type: home
cssclasses:
  - wide
icon: 🎯
tags:
  - home
  - kind/home
created: 2026-06-24
updated: 2026-06-24
---

# 🎯 Hoy

- [x] Revisar RFC hito 2 y compartirlo ✅ 2026-07-16
- [x] Revisar MURA MUDA MURI ✅ 2026-07-01

```dataviewjs
const today = dv.luxon.DateTime.now().startOf('day');
const yesterday = today.minus({days:1});
const in7 = today.plus({days:7});
const sprint = "A26Q2S7";

const all = dv.pages('-"70-templates"').file.tasks.array().filter(t=>!/(^|\s)#owner\/agent(\s|$)/.test(String(t.text)));
const isDone = t => ['x','X'].includes(t.status);
const isOpen = t => !isDone(t) && t.status !== '-';
const inSprint = t => String(t.text).includes('#sprint/'+sprint);

function emojiDate(t, emoji){
  const m = String(t.text).match(new RegExp(emoji+'\\s*(\\d{4}-\\d{2}-\\d{2})'));
  return m ? dv.luxon.DateTime.fromISO(m[1]) : null;
}
function dueOf(t){
  if (t.due){ try { return dv.luxon.DateTime.fromISO(t.due.toISODate()); } catch(e){} }
  return emojiDate(t,'📅');
}
function doneOf(t){
  if (t.completion){ try { return dv.luxon.DateTime.fromISO(t.completion.toISODate()); } catch(e){} }
  return emojiDate(t,'✅');
}

const open = all.filter(isOpen);
const overdue   = open.filter(t => { const d=dueOf(t); return d && d < today; }).sort(t=>dueOf(t));
const dueToday  = open.filter(t => { const d=dueOf(t); return d && d.hasSame(today,'day'); });
const upcoming  = open.filter(t => { const d=dueOf(t); return d && d > today && d <= in7; }).sort(t=>dueOf(t));
const wip       = open.filter(t => ['/','r'].includes(t.status));
const inbox     = open.filter(t => t.path.startsWith('00-inbox'));
const spOpen    = open.filter(inSprint);
const spDone    = all.filter(t => isDone(t) && inSprint(t));
const spTotal   = spOpen.length + spDone.length;
const pct       = spTotal ? Math.round(spDone.length/spTotal*100) : 0;
const doneYday  = all.filter(t => isDone(t) && (()=>{const d=doneOf(t);return d && d.hasSame(yesterday,'day');})());
const doneToday = all.filter(t => isDone(t) && (()=>{const d=doneOf(t);return d && d.hasSame(today,'day');})());

function card(label,val,color){
  return `<div style="background:var(--background-secondary);border-radius:8px;padding:10px 12px;">
    <div style="font-size:12px;color:var(--text-muted)">${label}</div>
    <div style="font-size:22px;font-weight:600;color:${color}">${val}</div></div>`;
}
const head = dv.el('div','');
head.innerHTML = `
<div style="font-size:13px;color:var(--text-muted);margin-bottom:8px;">
  ${today.setLocale('es').toFormat("cccc d 'de' LLLL")} · sprint ${sprint}
</div>
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(96px,1fr));gap:10px;">
  ${card('Atrasadas', overdue.length, 'var(--color-red)')}
  ${card('Vence hoy', dueToday.length, 'var(--color-orange)')}
  ${card('En curso', wip.length, 'var(--color-blue)')}
  ${card('Hechas ayer', doneYday.length, 'var(--color-green)')}
  ${card('Sprint', spDone.length+'/'+spTotal, 'var(--text-normal)')}
</div>
<div style="height:8px;background:var(--background-modifier-border);border-radius:999px;overflow:hidden;margin:10px 0 2px;">
  <div style="width:${pct}%;height:100%;background:var(--color-blue);"></div>
</div>
<div style="font-size:12px;color:var(--text-muted)">Sprint ${sprint}: ${spDone.length} de ${spTotal} (${pct}%) · vence 4 jul</div>
`;

dv.header(3, "🔴 Atrasadas — no postergable");
overdue.length ? dv.taskList(overdue, false) : dv.paragraph("_Nada atrasado._");

dv.header(3, "🟠 Vence hoy");
dueToday.length ? dv.taskList(dueToday, false) : dv.paragraph("_Nada vence hoy._");

dv.header(3, "🔜 Próximos 7 días");
upcoming.length ? dv.taskList(upcoming, false) : dv.paragraph("_Sin vencimientos próximos._");

dv.header(3, "🎯 Sprint " + sprint + " — pendientes");
spOpen.length ? dv.taskList(spOpen, false) : dv.paragraph("_Sin pendientes del sprint._");

dv.header(3, "✅ Completado ayer (para la daily)");
doneYday.length ? dv.taskList(doneYday, false) : dv.paragraph("_Nada cerrado ayer (recuerda marcar done con fecha)._");

dv.header(3, "✅ Completado hoy");
doneToday.length ? dv.taskList(doneToday, false) : dv.paragraph("_Aún nada hoy._");

dv.header(3, "🟢 Proyectos activos");
const projs = dv.pages('"10-projects"')
  .where(p => p.type=="project" && !p.parent && p.status!="done")
  .sort(p => p.priority, 'asc');
projs.length
  ? dv.table(["Proyecto","Estado","Prioridad","Sprint"],
      projs.map(p => [p.file.link, p.status, p.priority, p.sprint]))
  : dv.paragraph("_Sin proyectos activos._");

dv.header(3, "📥 Inbox sin clasificar");
inbox.length ? dv.taskList(inbox, false) : dv.paragraph("_Inbox vacío._");
```
Eliminar la validacion de plataforma y gestionar el comportamiento mediante el experimento.
título y no subtítulo
destaque de precio
pedido de chris

