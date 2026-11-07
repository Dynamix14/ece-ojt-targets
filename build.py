#!/usr/bin/env python3
"""Builds index.html for the ECE OJT targets site from data.json."""
import html, json, pathlib

HERE = pathlib.Path(__file__).parent
ROWS = json.loads((HERE / "data.json").read_text(encoding="utf-8"))


def esc(s):
    return html.escape(str(s), quote=True)


def badge(fit):
    cls = "b-high" if fit in ("HIGH", "MED-HIGH") else "b-mid" if fit == "MEDIUM" else "b-low"
    label = {"HIGH": "strong ECE fit", "MED-HIGH": "good ECE fit",
             "MEDIUM": "partial fit", "LOW-MED": "thin fit", "LOW": "weak fit"}[fit]
    return f'<span class="badge {cls}">{label}</span>'


def career_label(r):
    c = r["careers"]
    if "kalibrr" in c:
        return "Kalibrr listings"
    if "linkedin.com" in c:
        return "LinkedIn jobs"
    return "careers / contact"


def bar(km):
    w = min(100, max(5, (km / 26) ** 0.5 * 100)) if km <= 26 else 100
    return f'<span class="bar" aria-hidden="true"><i class="{"far" if km > 20 else ""}" style="width:{w:.0f}%"></i></span>'


def row(i, r):
    roles = "".join(f"<li>{esc(x.strip())}</li>" for x in r["roles"].split(";") if x.strip())
    links = [f'<a href="{esc(r["site"])}" target="_blank" rel="noopener">website</a>']
    if r["linkedin"]:
        links.append(f'<a href="{esc(r["linkedin"])}" target="_blank" rel="noopener">LinkedIn</a>')
    links.append(f'<a href="{esc(r["careers"])}" target="_blank" rel="noopener">{career_label(r)}</a>')
    for t, u in r["posts"]:
        links.append(f'<a class="post" href="{esc(u)}" target="_blank" rel="noopener">{esc(t.split("—")[0].split("(")[0].strip())}</a>')

    slots = r["slots"] if not r["slots"].startswith("http") else "⚠ data error: contains an Alstom careers URL"
    panel = f"""<div class="panel">
      <dl class="kv"><dt>Address</dt><dd>{esc(r['address'])}</dd></dl>
      <dl class="kv"><dt>Contact</dt><dd>{esc(r['contact'])}<br><span style="color:var(--muted)">{esc(r['position'])}</span></dd></dl>
      <dl class="kv"><dt>Email</dt><dd><a href="mailto:{esc(r['email'].split('|')[0].split('/')[0].strip())}">{esc(r['email'])}</a></dd></dl>
      <dl class="kv"><dt>MOA</dt><dd>{esc(r['effectivity'])}</dd></dl>
      <dl class="kv"><dt>Slots</dt><dd>{esc(slots or 'not stated')}</dd></dl>
      <dl class="kv"><dt>Intake</dt><dd>{esc(r['intake'] or 'not stated')}</dd></dl>
      <dl class="kv"><dt>Basis</dt><dd>{esc(r['ev'])}</dd></dl>
    </div>"""

    it = r["intern"]
    if it["n"]:
        bl = "".join(f"<li>{esc(b)}</li>" for b in it["bullets"])
        quote = f'<blockquote>{esc(it["quote"])}</blockquote>' if it["quote"] else ""
        src = (f'<a href="{esc(it["url"])}" target="_blank" rel="noopener">source</a>' if it["url"] else "")
        stars = f'<span class="r-stars">{esc(it["stars"])} / 5</span>' if it["stars"] else ""
        reality = f"""<div class="reality">
          <div class="r-head"><span class="r-tag">intern reality</span>{stars}<span class="r-src">{esc(it['src'])}</span>{src}</div>
          <ul class="r-list">{bl}</ul>{quote}
        </div>"""
    else:
        bl = "".join(f"<li>{esc(b)}</li>" for b in it["bullets"])
        reality = f"""<div class="reality none">
          <div class="r-head"><span class="r-tag muted">intern reality</span><span class="r-src">no first-hand account found — treat duties as inferred</span></div>
          <ul class="r-list">{bl}</ul>
        </div>"""

    name = r["company"].title() if r["company"].isupper() else r["company"]
    txt = " ".join([r["company"], r["roles"], r["offering"], r["address"], r["ev"],
                    " ".join(it["bullets"])]).lower()
    return f"""  <li class="row" data-km="{r['km']}" data-fit="{r['fit']}" data-posted="{1 if r['posts'] else 0}" data-reviews="{it['n']}" data-text="{esc(txt)}">
    <div class="rank">{i:02d}</div>
    <div class="body">
      <div class="head">
        <h2>{esc(name)}</h2>
        {badge(r['fit'])}
        {('<span class="badge b-live">posting found</span>' if r['posts'] else '')}
        <span class="dist">{bar(r['km'])} {r['km']:g} km · ~{r['min']} min</span>
      </div>
      <p class="addr">{esc(r['address'])}</p>
      <ul class="roles">{roles}</ul>
      <p class="what"><b>What they do</b>{esc(r['offering'])}</p>
      {reality}
      <div class="links">{''.join(links)}</div>
      <details class="more"><summary>contact &amp; MOA details</summary>{panel}</details>
    </div>
  </li>"""


CSS = """
  :root{
    --ink:#141a1f; --ink-2:#3d4a52; --muted:#6b7a82;
    --paper:#f7f4ee; --surface:#fffdf9; --line:#ddd6c9; --line-soft:#e9e3d8;
    --accent:#a8331f; --accent-soft:#f4e3dd;
    --ok:#1f5c3d; --ok-soft:#e2efe6;
    --warn:#8a5a00; --warn-soft:#f7ecd7;
    --radius:3px; --max:1080px;
    --sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
    --serif:"Iowan Old Style","Palatino Linotype",Palatino,Georgia,"Times New Roman",serif;
    --mono:ui-monospace,"SF Mono","Cascadia Mono",Menlo,Consolas,monospace;
  }
  *{box-sizing:border-box}
  html{-webkit-text-size-adjust:100%}
  body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--sans);font-size:16px;line-height:1.55;-webkit-font-smoothing:antialiased}
  a{color:var(--accent);text-decoration:none;text-underline-offset:2px}
  a:hover{text-decoration:underline}
  a:focus-visible,button:focus-visible,input:focus-visible,summary:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
  .wrap{max-width:var(--max);margin:0 auto;padding:0 20px}
  header.mast{border-bottom:2px solid var(--ink)}
  .mast-inner{display:flex;flex-wrap:wrap;gap:16px;align-items:flex-end;justify-content:space-between;padding:28px 20px 18px;max-width:var(--max);margin:0 auto}
  .eyebrow{font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}
  h1{font-family:var(--serif);font-weight:600;font-size:clamp(30px,5vw,46px);line-height:1.05;margin:6px 0 8px;letter-spacing:-.01em}
  .dek{max-width:56ch;color:var(--ink-2);font-size:15px;margin:0}
  .stamp{font-family:var(--mono);font-size:11px;color:var(--muted);text-align:right;line-height:1.7;white-space:nowrap}
  .controls{position:sticky;top:0;z-index:20;background:rgba(247,244,238,.94);backdrop-filter:blur(8px);border-bottom:1px solid var(--line);padding:12px 0}
  .controls-inner{display:flex;flex-wrap:wrap;gap:10px 14px;align-items:center;max-width:var(--max);margin:0 auto;padding:0 20px}
  .filters{display:flex;flex-wrap:wrap;gap:6px}
  .chip{font:inherit;font-size:13px;padding:5px 11px;background:transparent;border:1px solid var(--line);color:var(--ink-2);border-radius:999px;cursor:pointer;transition:background .15s,border-color .15s,color .15s}
  .chip:hover{border-color:var(--ink-2)}
  .chip[aria-pressed="true"]{background:var(--ink);border-color:var(--ink);color:var(--paper)}
  .search{margin-left:auto;display:flex;align-items:center;gap:8px}
  .search input{font:inherit;font-size:14px;padding:7px 10px;width:210px;border:1px solid var(--line);border-radius:var(--radius);background:var(--surface);color:var(--ink)}
  .search input::placeholder{color:var(--muted)}
  .count{font-family:var(--mono);font-size:11px;color:var(--muted);letter-spacing:.06em;text-transform:uppercase}
  main{padding:26px 0 8px}
  .lead{display:grid;gap:10px;margin:0 0 20px;padding-bottom:16px;border-bottom:1px solid var(--line)}
  .lead p{margin:0;font-size:14.5px;color:var(--ink-2);max-width:78ch}
  .lead strong{color:var(--ink)}
  .findings{list-style:none;margin:0;padding:0;display:grid;gap:6px}
  .findings li{font-size:14px;color:var(--ink-2);padding-left:16px;position:relative}
  .findings li::before{content:"";position:absolute;left:2px;top:9px;width:5px;height:5px;background:var(--ink);border-radius:50%;opacity:.4}
  ol.list{list-style:none;margin:0;padding:0;border-top:1px solid var(--line)}
  li.row{display:grid;grid-template-columns:44px 1fr;gap:0 18px;padding:18px 0 20px;border-bottom:1px solid var(--line)}
  .rank{font-family:var(--mono);font-size:13px;color:var(--muted);padding-top:3px;text-align:right}
  .body{min-width:0}
  .head{display:flex;flex-wrap:wrap;align-items:baseline;gap:8px 12px}
  h2{font-family:var(--serif);font-size:20px;font-weight:600;margin:0;line-height:1.25;letter-spacing:-.005em}
  .badge{font-family:var(--mono);font-size:10.5px;letter-spacing:.08em;text-transform:uppercase;padding:2px 7px;border-radius:2px;white-space:nowrap}
  .b-high{background:var(--ok-soft);color:var(--ok)}
  .b-mid{background:var(--warn-soft);color:var(--warn)}
  .b-low{background:#ecebe6;color:var(--muted)}
  .b-live{background:var(--accent-soft);color:var(--accent)}
  .dist{margin-left:auto;display:flex;align-items:center;gap:9px;font-family:var(--mono);font-size:12px;color:var(--ink-2);white-space:nowrap}
  .bar{width:78px;height:4px;background:var(--line-soft);border-radius:2px;overflow:hidden}
  .bar i{display:block;height:100%;background:var(--accent);border-radius:2px}
  .bar i.far{background:var(--muted)}
  .addr{font-size:13px;color:var(--muted);margin:5px 0 10px}
  .roles{margin:0;padding:0;list-style:none;display:grid;gap:4px}
  .roles li{position:relative;padding-left:15px;font-size:14.5px}
  .roles li::before{content:"";position:absolute;left:2px;top:9px;width:5px;height:5px;background:var(--accent);border-radius:50%;opacity:.65}
  .what{font-size:13.5px;color:var(--ink-2);margin:10px 0 0;max-width:74ch}
  .what b{color:var(--muted);font-weight:600;font-family:var(--mono);font-size:10.5px;letter-spacing:.08em;text-transform:uppercase;margin-right:6px}
  .reality{margin:14px 0 0;padding:11px 13px 12px;background:var(--surface);border:1px solid var(--line-soft);border-left:2px solid var(--ok);border-radius:var(--radius)}
  .reality.none{border-left-color:var(--line);background:transparent}
  .r-head{display:flex;flex-wrap:wrap;align-items:baseline;gap:10px;margin-bottom:7px}
  .r-tag{font-family:var(--mono);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--ok)}
  .r-tag.muted{color:var(--muted)}
  .r-stars{font-family:var(--mono);font-size:11px;color:var(--ink);background:var(--ok-soft);padding:1px 6px;border-radius:2px}
  .r-src{font-size:11.5px;color:var(--muted)}
  .r-head a{font-size:11.5px}
  .r-list{margin:0;padding:0;list-style:none;display:grid;gap:3px}
  .r-list li{position:relative;padding-left:14px;font-size:13.5px;color:var(--ink-2)}
  .r-list li::before{content:"—";position:absolute;left:0;color:var(--muted);font-size:12px}
  blockquote{margin:9px 0 0;padding:0 0 0 12px;border-left:2px solid var(--line);font-size:13px;color:var(--ink-2);font-style:italic}
  .links{display:flex;flex-wrap:wrap;gap:6px 14px;margin-top:11px;font-size:13px}
  .links a::after{content:"\\2197";font-size:10px;opacity:.55;margin-left:3px}
  .links .post{color:var(--ok);font-weight:600}
  .links .post::after{content:"\\2713";opacity:.7}
  details.more{margin-top:10px;font-size:13px;color:var(--ink-2)}
  details.more summary{cursor:pointer;color:var(--muted);font-family:var(--mono);font-size:11px;letter-spacing:.07em;text-transform:uppercase;list-style:none;display:inline-flex;gap:6px;align-items:center}
  details.more summary::-webkit-details-marker{display:none}
  details.more summary::before{content:"+";font-size:13px;color:var(--accent)}
  details.more[open] summary::before{content:"\\2212"}
  .panel{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:4px 22px;margin-top:8px;padding:10px 12px;background:var(--surface);border:1px solid var(--line-soft);border-radius:var(--radius)}
  .kv{display:grid;grid-template-columns:74px 1fr;gap:2px 8px;font-size:12.5px;padding:2px 0;margin:0}
  .kv dt{color:var(--muted);font-family:var(--mono);font-size:10.5px;letter-spacing:.06em;text-transform:uppercase;padding-top:2px}
  .kv dd{margin:0;min-width:0;overflow-wrap:anywhere}
  .empty{padding:40px 0;color:var(--muted);font-family:var(--mono);font-size:13px}
  footer{border-top:2px solid var(--ink);margin-top:30px;padding:26px 0 46px}
  footer h3{font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);margin:0 0 10px}
  footer p,footer li{font-size:13px;color:var(--ink-2);max-width:80ch}
  footer ul{padding-left:18px;margin:0 0 18px}
  footer li{margin-bottom:5px}
  .cols{display:grid;gap:26px;grid-template-columns:1fr 1fr}
  @media (max-width:720px){
    .cols{grid-template-columns:1fr}
    .mast-inner{padding-top:20px}
    .stamp{text-align:left}
    li.row{grid-template-columns:30px 1fr;gap:0 10px}
    .dist{margin-left:0;order:9}
    .search{margin-left:0;width:100%}
    .search input{width:100%}
  }
  @media (prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important}}
"""

HEAD = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ECE OJT Targets — ranked from Taft, Malate</title>
<meta name="description" content="17 companies that list ECE in the face-to-face OJT masterlist, ranked by driving distance from Taft, Malate — with the internship roles each one could give an ECE student and what interns actually report.">
<style>{CSS}</style>
</head>
<body>
<header class="mast">
  <div class="mast-inner">
    <div>
      <div class="eyebrow">Mapúa ECE · OJT placement brief</div>
      <h1>17 ECE-listed OJT targets,<br>ranked from Taft, Malate</h1>
      <p class="dek">Every company here names <b>ECE</b> in its programs-offered column. Ordered by driving distance from DLSU–Taft, with the roles each employer could hand an electronics engineering student — and what past interns say actually happens.</p>
    </div>
    <div class="stamp">
      433 rows screened<br>
      17 list ECE<br>
      9 with intern reviews<br>
      checked 7 Nov 2026
    </div>
  </div>
</header>
"""

CONTROLS = """
<div class="controls">
  <div class="controls-inner">
    <div class="filters" role="group" aria-label="Filter companies">
      <button class="chip" data-filter="all" aria-pressed="true">All 17</button>
      <button class="chip" data-filter="near" aria-pressed="false">≤ 6 km</button>
      <button class="chip" data-filter="mid" aria-pressed="false">6–10 km</button>
      <button class="chip" data-filter="far" aria-pressed="false">10–20 km</button>
      <button class="chip" data-filter="beyond" aria-pressed="false">20 km +</button>
      <button class="chip" data-filter="high" aria-pressed="false">Strong fit</button>
      <button class="chip" data-filter="reviews" aria-pressed="false">Has intern reviews</button>
      <button class="chip" data-filter="posted" aria-pressed="false">Posting found</button>
    </div>
    <div class="search">
      <button class="chip" id="sort" data-mode="distance">Sorted by distance</button>
      <label for="q" class="count">search</label>
      <input id="q" type="search" placeholder="RF, FPGA, ELV, overtime…" autocomplete="off">
    </div>
  </div>
</div>
"""

LEAD = """
<main class="wrap">
  <div class="lead">
    <p><strong>The short answer:</strong> the six Makati CBD sites are a 6-minute drive from Taft, and three of them are genuinely electronics work — <strong>Meinhardt</strong> (ELV design), <strong>USHER</strong> (seismic instrumentation) and <strong>Edgepoint</strong> (tower RF). The silicon sits far away: Lattice in Alabang, TI in Baguio.</p>
    <ul class="findings">
      <li><strong>The Makati internships are light.</strong> APMC interns report “not much to do most of the time”; Meinhardt’s only review calls it a “light working environment”.</li>
      <li><strong>Banking pays.</strong> Security Bank interns confirm a ₱10k+ allowance — and one cohort was paid more than two months after finishing.</li>
      <li><strong>Semiconductor gives real projects.</strong> TI and Lattice reviews both stress meaningful work plus a mentor; TI’s catch is a supervisor too busy to guide you.</li>
      <li><strong>The small firms are the wildcard.</strong> USHER’s single intern review is a 2.0 warning about zero training. No reviews exist at all for Jason Marine, 90 Degrees, PISAS, Secuna or Edgepoint.</li>
    </ul>
    <span class="count" id="live" role="status" aria-live="polite">17 of 17 companies shown</span>
  </div>
  <ol class="list">
"""

TAIL = """
  </ol>
  <p class="empty" id="empty" hidden>Nothing matches that filter. Clear the search or pick “All 17”.</p>
</main>
<footer>
  <div class="wrap cols">
    <div>
      <h3>How to read this</h3>
      <ul>
        <li><b>Distance</b> is road distance from DLSU–Taft (14.5649, 120.9931), generated by OSRM. Traffic-free: add 40–100% at rush hour.</li>
        <li><b>Roles</b> are inferred from each company’s published services — not from a vacancy. Only a green ✓ posting is a requisition I actually opened.</li>
        <li><b>Intern reality</b> is quoted from Indeed and JobStreet intern reviews and press coverage. Where it says “no first-hand account”, nothing exists publicly — don’t read the role list as a promise.</li>
        <li>Ranks 1–2 and 3–5 sit inside the same Makati CBD blocks; treat sub-kilometre gaps as ties.</li>
      </ul>
    </div>
    <div>
      <h3>Before you email anyone</h3>
      <ul>
        <li>SD Solutions’ MOA expires <b>23 Nov 2026</b>.</li>
        <li>AllHome’s slots field contains an Alstom careers URL — a data-entry error.</li>
        <li>APMC’s listed email domain is mistyped (ayalaprperty.com.ph); Security Bank’s email doesn’t match the named contact.</li>
        <li>Texas Instruments lists <b>EECE</b>, not ECE — confirm the code maps to BS Electronics Engineering, and note the site is Baguio (265 km).</li>
      </ul>
    </div>
  </div>
</footer>
<script>
(function(){
  const rows=[...document.querySelectorAll('li.row')];
  const chips=[...document.querySelectorAll('.chip[data-filter]')];
  const q=document.getElementById('q');
  const empty=document.getElementById('empty');
  const live=document.getElementById('live');
  let filter='all';
  const band = km => km<=6?'near': km<=10?'mid': km<=20?'far':'beyond';

  function apply(){
    const term=q.value.trim().toLowerCase();
    let shown=0;
    rows.forEach(function(li){
      const km=parseFloat(li.dataset.km);
      const okFilter = filter==='all'
        || (filter==='high' ? (li.dataset.fit==='HIGH'||li.dataset.fit==='MED-HIGH')
        :  filter==='posted' ? li.dataset.posted==='1'
        :  filter==='reviews' ? parseInt(li.dataset.reviews,10)>0
        :  band(km)===filter);
      const okTerm = !term || li.dataset.text.includes(term);
      const show = okFilter && okTerm;
      li.hidden=!show;
      if(show) shown++;
    });
    empty.hidden = shown>0;
    live.textContent = shown+' of '+rows.length+' companies shown';
  }
  chips.forEach(function(c){
    c.addEventListener('click',function(){
      chips.forEach(function(o){o.setAttribute('aria-pressed', String(o===c));});
      filter=c.dataset.filter; apply();
    });
  });
  q.addEventListener('input',apply);
  document.getElementById('sort').addEventListener('click',function(){
    const list=document.querySelector('ol.list');
    const mode=this.dataset.mode==='distance'?'fit':'distance';
    this.dataset.mode=mode;
    this.textContent = mode==='distance' ? 'Sorted by distance' : 'Sorted by ECE fit';
    const items=[...list.children];
    const rank={HIGH:0,'MED-HIGH':1,MEDIUM:2,'LOW-MED':3,LOW:4};
    items.sort(function(a,b){
      if(mode==='distance') return (+a.dataset.km)-(+b.dataset.km);
      return rank[a.dataset.fit]-rank[b.dataset.fit] || (+a.dataset.km)-(+b.dataset.km);
    });
    items.forEach(function(el){list.appendChild(el);});
    items.forEach(function(el,i){ el.querySelector('.rank').textContent=String(i+1).padStart(2,'0'); });
  });
  apply();
})();
</script>
</body>
</html>
"""

body = "\n".join(row(i, r) for i, r in enumerate(ROWS, 1))
(HERE / "index.html").write_text(HEAD + CONTROLS + LEAD + body + TAIL, encoding="utf-8")
print("wrote index.html:", len(HEAD + CONTROLS + LEAD + body + TAIL), "bytes")
