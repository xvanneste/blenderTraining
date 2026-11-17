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
import tempfile
from pathlib import Path
from urllib.parse import quote, unquote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "TOOLS"))
import academy_status as S  # noqa: E402

OUT = os.path.join(ROOT, "SITE")
TABS = [("README.md", "Présentation"), ("LESSON.md", "Leçons"), ("THEORY.md", "Théorie"),
        ("TUTORIAL.md", "Tutoriels"), ("EXERCISES.md", "Exercices"), ("SOLUTIONS.md", "Solutions"),
        ("TROUBLESHOOTING.md", "Dépannage"), ("RESOURCES.md", "Ressources")]
GENERAL = [("START_HERE.md", "Commencer ici"), ("README.md", "Présentation de l'académie"),
           ("DOCUMENTATION/PARCOURS_PREMIER_PLAN.md", "Premier plan animé"),
           ("01_FUNDAMENTALS/PROJECT_P1/README.md", "Projet P1 · Nature morte"),
           ("CURRICULUM.md", "Programme complet"), ("ROADMAP.md", "Feuilles de route"),
           ("PROGRESS.md", "Suivi de progression (modèle)"),
           ("DOCUMENTATION/CONVENTIONS.md", "Conventions"),
           ("DOCUMENTATION/GLOSSAIRE_BLENDER.md", "Glossaire Blender"),
           ("DOCUMENTATION/PIPELINE_BRIDGES.md", "Passerelles du pipeline"),
           ("DOCUMENTATION/COMPLEMENTARY_SOFTWARE.md", "Logiciels complémentaires"),
           ("DOCUMENTATION/VERSION_COMPATIBILITY.md", "Compatibilité des versions"),
           ("FINAL_AUDIT.md", "Contrôles de production")]
CHAPTER_DOCS = {filename for filename, _ in TABS}
GENERAL_DOCS = {filename for filename, _ in GENERAL}

MODELING_PRACTICE = {
    "CH01.05": ("outils", "maison"),
    "CH02.01": ("outils", "hum-topologie"),
    "CH02.02": ("caisse", "table", "chaise"),
    "CH02.03": ("epee", "maison"),
    "CH02.04": ("outils",),
    "CH02.05": ("epee", "coffre"),
    "CH02.06": ("stylise", "hum-mirror"),
    "CH02.07": ("coffre",),
    "CH02.08": ("stylise", "hum-corps"),
    "CH02.09": ("hum-topologie",),
    "CH02.10": ("hum-topologie",),
    "CH02.11": ("projet-humain",),
    "CH02.12": ("hum-rig",),
    "CH02.13": ("projet-humain",),
    "CH03.01": ("hum-poses", "hum-photos"),
    "CH03.04": ("stylise",),
    "CH03.06": ("hum-visage",),
    "CH03.07": ("hum-corps",),
    "CH03.09": ("hum-topologie",),
    "CH03.10": ("hum-rig", "projet-humain"),
}


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
    if base == "02_MODELING/PARCOURS_PRATIQUE" and re.fullmatch(r"[a-z0-9-]+\.md", u):
        return "#atelier/" + u[:-3]
    path, _, fragment = u.partition("#")
    target = os.path.normpath(os.path.join(base, unquote(path))).replace("\\", "/")
    anchor = "/" + quote(unquote(fragment), safe="") if fragment else ""
    chapter = re.fullmatch(r"(\d{2}_[^/]+)/(CH(\d{2})_(\d{2})_[^/]+)/([^/]+)", target)
    if chapter and chapter.group(1) == S.PHASE_DIRS.get(int(chapter.group(3))):
        doc = chapter.group(5)
        filename = Path(ROOT) / target
        if doc in CHAPTER_DOCS and filename.is_file():
            return f"#ch/CH{chapter.group(3)}.{chapter.group(4)}/{doc}{anchor}"
        if doc == "QUIZ.md" and not fragment and filename.is_file():
            return f"#ch/CH{chapter.group(3)}.{chapter.group(4)}/QUIZ"
    if target in GENERAL_DOCS:
        return "#doc/" + target + anchor
    if target == "SITE/index.html" and fragment:
        return "#" + html.escape(fragment)
    # Les ressources à ouvrir ou à télécharger restent des fichiers relatifs.
    rel = os.path.relpath(os.path.join(ROOT, target), OUT).replace("\\", "/")
    return html.escape(rel + ("#" + fragment if fragment else ""))


def md_to_html(text, base="", anchors=None):
    if anchors is None:
        anchors = set()
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
            title = _inline(m.group(2), base)
            visible = html.unescape(re.sub(r"<[^>]*>", "", title)).lower()
            slug = re.sub(r"[^\w\- ]", "", visible).replace(" ", "-")
            identifier = slug or "section"
            index = 1
            while identifier in anchors:
                identifier = f"{slug or 'section'}-{index}"
                index += 1
            anchors.add(identifier)
            out.append(f'<h{lvl} id="{identifier}" tabindex="-1">{title}</h{lvl}>')
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
            out.append(f"<blockquote>{md_to_html(chr(10).join(buf), base, anchors)}</blockquote>")
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


def modeling_course():
    base = Path(ROOT) / "02_MODELING" / "PARCOURS_PRATIQUE"
    with (base / "programme.json").open(encoding="utf-8") as src:
        course = json.load(src)
    units = set()
    for group in course:
        for unit in group["units"]:
            code = unit["id"]
            if code in units or not re.fullmatch(r"[a-z0-9-]+", code):
                raise ValueError(f"Identifiant d'atelier invalide : {code}")
            units.add(code)
            path = base / (code + ".md")
            text = path.read_text(encoding="utf-8")
            intro, guided = text.split("\n## Tutoriel dans Blender\n", 1)
            parts = re.split(r"^### ([a-z0-9-]+) — (.+)$", guided, flags=re.M)
            steps = []
            if parts[0].strip() or len(parts) < 4:
                raise ValueError(f"Étapes introuvables : {path}")
            for i in range(1, len(parts), 3):
                step, title, body = parts[i:i + 3]
                steps.append({"id": step, "title": title, "html": md_to_html(body, "02_MODELING/PARCOURS_PRATIQUE")})
            if len({step["id"] for step in steps}) != len(steps):
                raise ValueError(f"Étape dupliquée : {path}")
            for link in re.findall(r"\]\(([^\s()]+)\)", text):
                if not link.startswith(("https:", "http:", "#")) and not (base / link.split("#")[0]).exists():
                    raise ValueError(f"Lien local introuvable dans {path.name} : {link}")
            intro = re.sub(r"^# [^\n]+\n", "", intro, count=1)
            unit.update({"intro": md_to_html(intro, "02_MODELING/PARCOURS_PRATIQUE"), "steps": steps, "text": plain(text)})
            if unit.get("video"):
                if not (base / unit["video"]).is_file():
                    raise ValueError(f"Vidéo introuvable : {unit['video']}")
                unit["video"] = _url(unit["video"], "02_MODELING/PARCOURS_PRATIQUE")
            for question in unit.get("quiz", []):
                if question["type"] != "mcq" or not 0 <= question["answer"] < len(question["choices"]):
                    raise ValueError(f"Quiz invalide : {path}")
    return course


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
                if status.startswith("✅"):
                    item["evidence"] = ("Contrôles techniques enregistrés" if os.path.isfile(
                        os.path.join(d, "SCRIPTS", "tests.json")) else "Supports publiés · évaluation par revue")
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
    data["modeling"] = modeling_course()
    unit_ids = {unit["id"] for group in data["modeling"] for unit in group["units"]}
    for chapter, units in MODELING_PRACTICE.items():
        if chapter not in data["chapters"] or not unit_ids.issuperset(units):
            raise ValueError(f"Renvoi d'atelier invalide : {chapter}")
        data["chapters"][chapter]["practice"] = units
    return data


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    os.makedirs(OUT, exist_ok=True)
    data = collect()
    output = tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=OUT, delete=False)
    temp_data = Path(output.name)
    try:
        with output as fh:
            fh.write("window.BCMA = ")
            json.dump(data, fh, ensure_ascii=False)
            fh.write(";\n")
        temp_data.replace(Path(OUT) / "data.js")
    finally:
        temp_data.unlink(missing_ok=True)
    for name in ("index.html", "style.css", "app.js"):
        src = os.path.join(ROOT, "TOOLS", "site_template", name)
        with open(src, encoding="utf-8") as a, open(os.path.join(OUT, name), "w", encoding="utf-8") as b:
            b.write(a.read())
    n_docs = sum(len(c["docs"]) for c in data["chapters"].values())
    print(f"[site] {data['stats']['done']}/{data['stats']['total']} chapitres au statut publié, "
          f"{len(data['chapters'])} dossiers, {n_docs} documents, {len(data['sheets'])} fiches -> SITE/index.html")


if __name__ == "__main__":
    main()
