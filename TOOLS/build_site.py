"""
build_site.py — Application de consultation hors ligne de l'académie.

Génère SITE/ (à ouvrir directement : SITE/index.html, aucun serveur ni dépendance) :
  index.html, style.css, app.js (fixes) et data.js (contenu régénéré à chaque exécution).
Fonctions : navigation par phase et chapitre (statut réel), lecture des 9 documents de chaque
chapitre, quiz interactifs (QCM corrigés, questions ouvertes à auto-évaluer), progression et
favoris mémorisés dans le navigateur (localStorage), recherche plein texte, fiches de révision,
documents généraux (START_HERE, CURRICULUM, ROADMAP, guides).

Convertisseur Markdown minimal intégré (titres, listes, tableaux, code, liens, images, gras,
italique, citations) : aucune bibliothèque externe n'est installée.

Usage : python TOOLS/build_site.py
"""
import glob
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "TOOLS"))
import academy_status as S  # noqa: E402

OUT = os.path.join(ROOT, "SITE")
TABS = [("README.md", "Présentation"), ("LESSON.md", "Leçons"), ("THEORY.md", "Théorie"),
        ("TUTORIAL.md", "Tutoriels"), ("EXERCISES.md", "Exercices"), ("SOLUTIONS.md", "Solutions"),
        ("TROUBLESHOOTING.md", "Dépannage"), ("RESOURCES.md", "Ressources")]
GENERAL = [("START_HERE.md", "Commencer ici"), ("README.md", "Présentation de l'académie"),
           ("CURRICULUM.md", "Programme complet"), ("ROADMAP.md", "Feuilles de route"),
           ("PROGRESS.md", "Suivi de progression (modèle)"),
           ("DOCUMENTATION/CONVENTIONS.md", "Conventions"),
           ("DOCUMENTATION/PIPELINE_BRIDGES.md", "Passerelles du pipeline"),
           ("DOCUMENTATION/COMPLEMENTARY_SOFTWARE.md", "Logiciels complémentaires"),
           ("DOCUMENTATION/VERSION_COMPATIBILITY.md", "Compatibilité des versions"),
           ("FINAL_AUDIT.md", "Audit final")]


# ---------------------------------------------------------------------------
# Markdown → HTML (sous-ensemble suffisant pour les documents de l'académie)
# ---------------------------------------------------------------------------

def _inline(text, base):
    parts = re.split(r"(`[^`]+`)", text)
    out = []
    for p in parts:
        if p.startswith("`") and p.endswith("`") and len(p) > 1:
            out.append("<code>" + html.escape(p[1:-1]) + "</code>")
            continue
        s = html.escape(p, quote=False)

        def img(m):
            return f'<img alt="{m.group(1)}" src="{_url(m.group(2), base)}">'

        def link(m):
            u = m.group(2)
            ext = u.startswith("http")
            return f'<a href="{_url(u, base)}"{" target=_blank rel=noopener" if ext else ""}>{m.group(1)}</a>'
        s = re.sub(r"!\[([^\]]*)\]\(([^)\s]+)\)", img, s)
        s = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, s)
        s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
        s = re.sub(r"(?<![\w*])\*([^*\n]+)\*(?![\w*])", r"<em>\1</em>", s)
        out.append(s)
    return "".join(out)


def _url(u, base):
    if re.match(r"^(https?:|mailto:|#)", u):
        return u
    # liens relatifs : depuis SITE/ vers le fichier réel de l'académie
    target = os.path.normpath(os.path.join(base, u)).replace("\\", "/")
    rel = os.path.relpath(os.path.join(ROOT, target), OUT).replace("\\", "/")
    return html.escape(rel)


def md_to_html(text, base=""):
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    lines = text.split("\n")
    out, i = [], 0
    while i < len(lines):
        line = lines[i]
        st = line.strip()
        if st.startswith("```"):
            lang = st[3:].strip()
            buf = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                buf.append(lines[i])
                i += 1
            out.append(f'<pre class="code" data-lang="{html.escape(lang)}"><code>{html.escape(chr(10).join(buf))}</code></pre>')
            i += 1
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", st)
        if m:
            lvl = len(m.group(1))
            out.append(f"<h{lvl}>{_inline(m.group(2), base)}</h{lvl}>")
            i += 1
            continue
        if re.match(r"^(-{3,}|\*{3,})$", st):
            out.append("<hr>")
            i += 1
            continue
        if st.startswith("|") and i + 1 < len(lines) and re.match(r"^\|?\s*:?-{2,}", lines[i + 1].strip()):
            head = [c.strip() for c in st.strip("|").split("|")]
            i += 2
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            h = "".join(f"<th>{_inline(c, base)}</th>" for c in head)
            b = "".join("<tr>" + "".join(f"<td>{_inline(c, base)}</td>" for c in r) + "</tr>" for r in rows)
            out.append(f'<div class="tw"><table><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>')
            continue
        if st.startswith(">"):
            buf = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                buf.append(lines[i].strip()[1:].strip())
                i += 1
            out.append(f"<blockquote>{md_to_html(chr(10).join(buf), base)}</blockquote>")
            continue
        if re.match(r"^\s*([-*+]|\d+[.)])\s+", line):
            items, ordered = [], bool(re.match(r"^\s*\d+[.)]", line))
            while i < len(lines) and lines[i].strip() and (re.match(r"^\s*([-*+]|\d+[.)])\s+", lines[i])
                                                           or (lines[i].startswith("   ") and items)):
                l2 = lines[i]
                mm = re.match(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$", l2)
                if mm and len(mm.group(1)) < 2:
                    items.append([mm.group(3)])
                else:
                    items[-1].append(l2.strip())
                i += 1
            tag = "ol" if ordered else "ul"
            lis = []
            for it in items:
                first, rest = it[0], it[1:]
                sub = ""
                if rest and re.match(r"^([-*+]|\d+[.)])\s+", rest[0]):
                    sub = md_to_html("\n".join(rest), base)
                    rest = []
                lis.append("<li>" + _inline(" ".join([first] + rest), base) + sub + "</li>")
            out.append(f"<{tag}>" + "".join(lis) + f"</{tag}>")
            continue
        if not st:
            i += 1
            continue
        buf = []
        while i < len(lines) and lines[i].strip() and not re.match(r"^(#{1,6}\s|```|\||>|\s*([-*+]|\d+[.)])\s+)", lines[i].strip()):
            buf.append(lines[i].strip())
            i += 1
        if not buf:          # ligne non reconnue : on l'avance pour éviter une boucle infinie
            buf.append(lines[i].strip())
            i += 1
        out.append("<p>" + _inline(" ".join(buf), base) + "</p>")
    return "\n".join(out)


def plain(text):
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    return re.sub(r"[#*`|>\[\]()_-]+", " ", text)


# ---------------------------------------------------------------------------
# Collecte du contenu
# ---------------------------------------------------------------------------

def collect():
    chapters_meta = S.curriculum_chapters()
    tests = S.last_results()
    phases = {}
    for ph, num, title in chapters_meta:
        phases.setdefault(ph, []).append((ph, num, title))
    data = {"phases": [], "chapters": {}, "general": [], "sheets": [], "stats": {}}
    phase_titles = {}
    for m in re.finditer(r"^## PHASE (\d+) — ([^⏱\n]+)", open(os.path.join(ROOT, "CURRICULUM.md"), encoding="utf-8").read(), re.M):
        phase_titles[int(m.group(1))] = m.group(2).strip().capitalize()
    n_done = 0
    for p in sorted(phases):
        entries = []
        for ph, num, title in phases[p]:
            code = f"CH{ph:02d}.{num:02d}"
            status, d, _missing = S.chapter_status(ph, num, tests)
            item = {"code": code, "title": title, "status": status, "dir": None}
            if d and os.path.isdir(d):
                rel = os.path.relpath(d, ROOT).replace("\\", "/")
                item["dir"] = rel
                docs = {}
                for fname, label in TABS:
                    f = os.path.join(d, fname)
                    if os.path.exists(f):
                        txt = open(f, encoding="utf-8").read()
                        docs[fname] = {"label": label, "html": md_to_html(txt, rel), "text": plain(txt)[:20000]}
                quiz = os.path.join(ROOT, "QUIZZES", "ch" + code[2:].replace(".", "_") + ".json")
                q = json.load(open(quiz, encoding="utf-8")) if os.path.exists(quiz) else None
                imgs = sorted(os.path.relpath(x, OUT).replace("\\", "/")
                              for x in glob.glob(os.path.join(d, "COMPLETED_EXAMPLES", "*.png")))
                data["chapters"][code] = {"docs": docs, "quiz": q, "images": imgs}
            if "✅" in status:
                n_done += 1
            entries.append(item)
        data["phases"].append({"num": p, "title": phase_titles.get(p, f"Phase {p}"), "chapters": entries})
    for f, label in GENERAL:
        path = os.path.join(ROOT, f)
        if os.path.exists(path):
            txt = open(path, encoding="utf-8").read()
            data["general"].append({"id": f, "label": label, "html": md_to_html(txt, os.path.dirname(f)),
                                    "text": plain(txt)[:40000]})
    for f in sorted(glob.glob(os.path.join(ROOT, "CHEAT_SHEETS", "*.md"))):
        txt = open(f, encoding="utf-8").read()
        title = (re.search(r"^#\s+(.*)$", txt, re.M) or [None, os.path.basename(f)])[1]
        data["sheets"].append({"id": os.path.basename(f), "label": title.replace("Fiche de révision — ", ""),
                               "html": md_to_html(txt, "CHEAT_SHEETS"), "text": plain(txt)})
    data["stats"] = {"total": len(chapters_meta), "done": n_done}
    return data


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    os.makedirs(OUT, exist_ok=True)
    data = collect()
    with open(os.path.join(OUT, "data.js"), "w", encoding="utf-8") as fh:
        fh.write("window.BCMA = ")
        json.dump(data, fh, ensure_ascii=False)
        fh.write(";\n")
    for name in ("index.html", "style.css", "app.js"):
        src = os.path.join(ROOT, "TOOLS", "site_template", name)
        with open(src, encoding="utf-8") as a, open(os.path.join(OUT, name), "w", encoding="utf-8") as b:
            b.write(a.read())
    n_docs = sum(len(c["docs"]) for c in data["chapters"].values())
    print(f"[site] {data['stats']['done']}/{data['stats']['total']} chapitres vérifiés, "
          f"{len(data['chapters'])} dossiers, {n_docs} documents, {len(data['sheets'])} fiches -> SITE/index.html")


if __name__ == "__main__":
    main()
