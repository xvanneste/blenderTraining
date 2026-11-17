"""
academy_status.py — Inventaire de production de l'académie.

Lit CURRICULUM.md (liste officielle des chapitres), inspecte les dossiers de
chapitres et écrit TASKS.md : liste exhaustive des tâches, dépendances et statut
réel de chaque chapitre, calculé à partir des fichiers présents (pas déclaratif).

Statuts :
  ✅ Terminé et vérifié        9 documents + quiz JSON + (tests.json passants OU chapitre sans .blend déclaré "doc-only")
  🟦 Terminé mais non vérifié  9 documents + quiz JSON, tests absents ou en échec
  🟨 Partiellement terminé     dossier présent mais documents manquants
  ⬜ Non commencé              pas de dossier

Usage : python TOOLS/academy_status.py
"""
from collections import Counter
import glob
import hashlib
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = ["README.md", "LESSON.md", "THEORY.md", "TUTORIAL.md", "EXERCISES.md", "QUIZ.md",
        "SOLUTIONS.md", "TROUBLESHOOTING.md", "RESOURCES.md"]
PHASE_DIRS = {0: "00_SETUP", 1: "01_FUNDAMENTALS", 2: "02_MODELING", 3: "03_SCULPTING",
              4: "04_MATERIALS", 5: "05_GEOMETRY_NODES", 6: "06_RIGGING", 7: "07_ANIMATION",
              8: "08_SIMULATIONS", 9: "09_CINEMATOGRAPHY", 10: "10_RENDERING",
              11: "11_COMPOSITING_VFX", 12: "12_EDITING_SOUND", 13: "13_PYTHON_AUTOMATION",
              14: "14_AI_PRODUCTION", 15: "15_SHORT_FILMS", 16: "16_FEATURE_FILMS",
              17: "17_EXPERT_SPECIALIZATIONS", 18: "18_GREASE_PENCIL"}
# Dépendances principales entre phases (prérequis pédagogiques)
PHASE_DEPS = {0: [], 1: [0], 2: [1], 3: [2], 4: [2], 5: [2, 4], 6: [3], 7: [6], 8: [2],
              9: [1, 4], 10: [4, 9], 11: [10], 12: [1], 13: [1], 14: [13], 18: [1],
              15: [7, 9, 10, 11, 12, 18], 16: [15], 17: [16]}


def curriculum_chapters():
    text = open(os.path.join(ROOT, "CURRICULUM.md"), encoding="utf-8").read()
    chapters = []
    for m in re.finditer(r"^\|\s*\**CH(\d\d)\.(\d\d)\s+([^|*]+?)\**(?:\s*⏱[^|]*)?\s*\|", text, re.M):
        ph, num, title = int(m.group(1)), int(m.group(2)), m.group(3).strip()
        if (ph, num) not in [(c[0], c[1]) for c in chapters]:
            chapters.append((ph, num, title))
    return chapters


def last_results():
    p = os.path.join(ROOT, "TOOLS", "last_test_results.json")
    if not os.path.exists(p):
        return {}
    data = json.load(open(p, encoding="utf-8"))
    res = {}
    for r in data["results"]:
        res.setdefault(r["chapter"], []).append(r)
    return res


def case_label(case):
    verdict = "VALIDÉ" if case["expect"] else "REFUSÉ"
    return f"{case['file']} [{case['exercise']}] attendu {verdict}"


def extra_label(extra):
    return f"script {extra['script']}"


def evidence_gaps(spec_bytes, recorded):
    spec = json.loads(spec_bytes)
    expected = Counter(case_label(case) for case in spec.get("cases", ()))
    expected.update(extra_label(extra) for extra in spec.get("extra", ()))
    if not expected:
        return ["aucun scénario déclaré"]
    got = Counter(row["test"] for row in recorded)
    gaps = []
    if expected - got:
        gaps.append(f"{sum((expected - got).values())} résultat(s) déclaré(s) manquant(s)")
    if any(not row["ok"] for row in recorded):
        gaps.append("au moins un contrôle enregistré en échec")
    fingerprint = hashlib.sha256(spec_bytes).hexdigest()
    if any(row.get("spec_sha256", fingerprint) != fingerprint for row in recorded):
        gaps.append("spécification modifiée depuis les résultats")
    return gaps


def chapter_status(ph, num, tests):
    pattern = os.path.join(ROOT, PHASE_DIRS[ph], f"CH{ph:02d}_{num:02d}_*")
    found = [d for d in glob.glob(pattern) if os.path.isdir(d)]
    if not found:
        return "⬜ Non commencé", None, []
    d = found[0]
    missing = [f for f in DOCS if not os.path.exists(os.path.join(d, f))]
    quiz = os.path.exists(os.path.join(ROOT, "QUIZZES", f"ch{ph:02d}_{num:02d}.json"))
    if not quiz:
        missing.append(f"QUIZZES/ch{ph:02d}_{num:02d}.json")
    if missing:
        return "🟨 Partiellement terminé", d, missing
    spec = os.path.join(d, "SCRIPTS", "tests.json")
    name = os.path.basename(d)
    if os.path.exists(spec):
        r = tests.get(name)
        with open(spec, "rb") as source:
            gaps = evidence_gaps(source.read(), r or [])
        if r and not gaps:
            return "✅ Terminé et vérifié", d, []
        return "🟦 Terminé mais non vérifié", d, gaps
    if os.path.exists(os.path.join(d, "DOC_ONLY")):
        return "✅ Terminé et vérifié", d, []
    return "🟦 Terminé mais non vérifié", d, ["pas de tests.json"]


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    chapters = curriculum_chapters()
    tests = last_results()
    lines = ["# TASKS — Liste exhaustive de production (générée)", "",
             "> Fichier généré par `python TOOLS/academy_status.py` à partir de CURRICULUM.md",
             "> et de l'état réel des dossiers. Ne pas éditer à la main.", "",
             "## Dépendances entre phases", "", "| Phase | Dépend de |", "|---|---|"]
    lines += [f"| {p} | {', '.join(map(str, d)) or '—'} |" for p, d in sorted(PHASE_DEPS.items())]
    counts = {}
    by_phase = {}
    for ph, num, title in chapters:
        st, d, missing = chapter_status(ph, num, tests)
        counts[st] = counts.get(st, 0) + 1
        by_phase.setdefault(ph, []).append((num, title, st, d, missing))
    lines += ["", "## Synthèse", "", "| Statut | Chapitres |", "|---|---|"]
    lines += [f"| {k} | {v} |" for k, v in sorted(counts.items())]
    lines += [f"| **Total** | **{len(chapters)}** |"]
    for ph in sorted(by_phase):
        lines += ["", f"## Phase {ph} — `{PHASE_DIRS[ph]}/`", "",
                  "| Chapitre | Titre | Statut | Manques |", "|---|---|---|---|"]
        for num, title, st, d, missing in by_phase[ph]:
            link = f"[CH{ph:02d}.{num:02d}]({os.path.relpath(d, ROOT).replace(os.sep, '/')}/README.md)" if d else f"CH{ph:02d}.{num:02d}"
            lines.append(f"| {link} | {title} | {st} | {', '.join(missing) if missing else ''} |")
    open(os.path.join(ROOT, "TASKS.md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
    # Mise à jour de la section « État de production » de chaque README de phase
    for ph, rows in by_phase.items():
        rp = os.path.join(ROOT, PHASE_DIRS[ph], "README.md")
        if not os.path.exists(rp):
            continue
        txt = open(rp, encoding="utf-8").read()
        table = ["## État de production", "", "| Chapitre | Statut |", "|---|---|"]
        for num, title, st, d, missing in rows:
            if d:
                rel = os.path.relpath(d, os.path.dirname(rp)).replace(os.sep, "/")
                table.append(f"| [CH{ph:02d}.{num:02d} {title}]({rel}/README.md) | {st} |")
            else:
                table.append(f"| CH{ph:02d}.{num:02d} {title} | {st} |")
        block = "\n".join(table) + "\n"
        if "## État de production" in txt:
            start = txt.index("## État de production")
            nxt = txt.find("\n## ", start + 5)
            txt = txt[:start] + block + ("\n" + txt[nxt + 1:] if nxt != -1 else "")
        else:
            txt = txt.rstrip() + "\n\n" + block
        open(rp, "w", encoding="utf-8").write(txt)
    print(f"{len(chapters)} chapitres :", ", ".join(f"{k} {v}" for k, v in counts.items()))


if __name__ == "__main__":
    main()
