"""Contrôle les documents pédagogiques, quiz et routes du site Blender généré."""
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

import academy_status as catalogue

ROOT = Path(catalogue.ROOT)
LINK = re.compile(r"!?(?:\[[^\]\n]*\])\(\s*(<[^>\n]+>|[^\s)]+)\s*(?:\"[^\"\n]*\")?\)")
BAD_EXIT_ORDER = re.compile(r"--python[ \t]+(?:\"[^\"\r\n]+\"|[^\s]+)[ \t]+--python-exit-code")
FENCE = re.compile(r"^ {0,3}(?:" + chr(96) * 3 + r"|~~~)")


class Page(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.ids = set()
        self.duplicates = set()
        self.routes = []
        self.feed(html)

    def handle_starttag(self, tag, pairs):
        attrs = dict(pairs)
        identifier = attrs.get("id")
        if identifier:
            if identifier in self.ids:
                self.duplicates.add(identifier)
            self.ids.add(identifier)
        href = attrs.get("href") or ""
        if tag == "a" and href.startswith(("#ch/", "#doc/")):
            self.routes.append(unquote(href))


def validate_docs():
    errors = []
    docs = 0
    chapters = catalogue.curriculum_chapters()
    sources = []
    for phase, number, _title in chapters:
        code = f"CH{phase:02}.{number:02}"
        folders = list((ROOT / catalogue.PHASE_DIRS[phase]).glob(f"CH{phase:02}_{number:02}_*"))
        if len(folders) != 1:
            errors.append(f"{code}: {len(folders)} dossiers")
            continue
        sources.extend(folders[0] / name for name in catalogue.DOCS)
        quiz_path = ROOT / "QUIZZES" / f"ch{phase:02}_{number:02}.json"
        quiz = json.loads(quiz_path.read_text(encoding="utf-8-sig"))
        questions = quiz["questions"]
        ids = [q["id"] for q in questions]
        if quiz["chapter"] != code or len(ids) != len(set(ids)) or not 0 < quiz["pass_score"] <= len(ids):
            errors.append(f"{quiz_path}: structure du quiz")
        for question in questions:
            kind = question["type"]
            if kind == "mcq":
                valid = 0 <= question["answer"] < len(question["choices"])
            else:
                valid = kind == "open" and bool(question.get("answer_text"))
            if not valid:
                errors.append(f"{quiz_path}: réponse de {question['id']}")
    sources.extend(ROOT.glob("*.md"))
    sources.extend((ROOT / "DOCUMENTATION").rglob("*.md"))
    sources.extend((ROOT / "CHEAT_SHEETS").glob("*.md"))
    sources.extend(ROOT.glob("[01][0-9]_*/PROJECT_P*/README.md"))
    for path in sources:
        doc = path.read_text(encoding="utf-8-sig")
        fenced = False
        docs += 1
        for line_number, line in enumerate(doc.splitlines(), 1):
            if FENCE.match(line):
                fenced = not fenced
                continue
            if BAD_EXIT_ORDER.search(line):
                errors.append(f"{path.relative_to(ROOT)}:{line_number}: code de sortie activé trop tard")
            if fenced:
                continue
            for match in LINK.finditer(line):
                url = urlsplit(match[1].strip("<>"))
                if not url.scheme and url.path:
                    target = path.parent / unquote(url.path)
                    if not target.exists():
                        errors.append(f"{path.relative_to(ROOT)}:{line_number}: {url.path}")
    return docs, len(chapters), errors


def validate_routes():
    text = (ROOT / "SITE/data.js").read_text(encoding="utf-8").strip()
    prefix = "window.BCMA = "
    if not text.startswith(prefix) or not text.endswith(";"):
        raise ValueError("SITE/data.js ne contient pas les données générées attendues.")
    data = json.loads(text[len(prefix):-1])
    docs = {}
    known_chapters = {f"#ch/{chapter['code']}" for phase in data["phases"] for chapter in phase["chapters"]}
    for code, chapter in data["chapters"].items():
        for tab, doc in chapter["docs"].items():
            docs[f"#ch/{code}/{tab}"] = Page(doc["html"])
        if chapter["quiz"]:
            docs[f"#ch/{code}/QUIZ"] = Page("")
    for doc in data["general"]:
        docs[f"#doc/{doc['id']}"] = Page(doc["html"])
    for fiche in data["sheets"]:
        docs[f"fiche:{fiche['id']}"] = Page(fiche["html"])
    checked = 0
    errors = []
    for address, page in docs.items():
        for identifier in sorted(page.duplicates):
            errors.append(f"{address}: ancre dupliquée {identifier}")
        for link in page.routes:
            checked += 1
            if link in docs or link in known_chapters:
                continue
            base, _, anchor = link.rpartition("/")
            if base not in docs or anchor not in docs[base].ids:
                errors.append(f"{address}: lien interne introuvable {link}")
    return checked, errors


def main():
    docs, quizzes, errors = validate_docs()
    routes, route_errors = validate_routes()
    errors.extend(route_errors)
    print(f"{docs} documents, {quizzes} quiz et {routes} renvois du site contrôlés.")
    for error in errors:
        print(error)
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
