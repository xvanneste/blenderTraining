"""docgen.py — génère les documents d'un chapitre à partir d'un dictionnaire (spec). Usage : from docgen import make; make(SPEC)."""
import json
import os

ROOT = r"G:\_formation\blender\BLENDER_CINEMA_MASTER_ACADEMY"
BL = r'"C:\Program Files\Blender Foundation\Blender 5.3\blender.exe"'


def w(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write(text)


def make(S):
    os.chdir(ROOT)
    D = f"{S['phase_dir']}/{S['dir']}/"
    pfx = S["pfx"]
    code = S["code"]
    num = code.replace("CH", "").replace(".", "_")          # 07_02
    low = code.lower().replace(".", "_")                    # ch07_02
    exs = S["exercises_validator"]                          # {exercise: [(solution, starter, [counters...])]} ou liste de blocs
    cases = []
    for blk in S["blocks"]:
        ex, sol, start = blk["exercise"], blk["solution"], blk["starter"]
        cases.append({"file": f"COMPLETED_EXAMPLES/{sol}.blend", "exercise": ex, "expect": True})
        cases.append({"file": f"STARTER_FILES/{start}.blend", "exercise": ex, "expect": False})
        for k, _, _ in blk["counters"]:
            cases.append({"file": f"COMPLETED_EXAMPLES/COUNTER_EXAMPLES/{blk['cprefix']}_{k}.blend", "exercise": ex, "expect": False})
    w(D + "SCRIPTS/tests.json", json.dumps({"build": f"build_{low}_files.py", "validator": f"validate_{low}.py", "cases": cases}, indent=2, ensure_ascii=False) + "\n")
    usage = "\n\n".join(f"& {BL} -b --factory-startup `\n  \"STARTER_FILES\\{b['starter']}_<prenom>_v001.blend\" `\n  --python-exit-code 1 --python \"SCRIPTS\\validate_{low}.py\" -- --exercise {b['exercise']}" for b in S["blocks"])
    files = [[f"STARTER_FILES/{b['starter']}.blend", b["starter_desc"]] for b in S["blocks"]] + \
            [[f"COMPLETED_EXAMPLES/{b['solution']}.blend", b["solution_desc"]] for b in S["blocks"]] + \
            [[f"COMPLETED_EXAMPLES/{b['solution'].replace('_solution', '_reference')}.png", b["ref_desc"]] for b in S["blocks"] if b.get("ref_desc")] + \
            [["COMPLETED_EXAMPLES/COUNTER_EXAMPLES/", S["counter_desc"]], [f"SCRIPTS/validate_{low}.py", "Correcteur"]]
    chapter = {"code": code, "title": S["title"], "phase_title": S["phase_title"], "level": S["level"], "duration": S["duration"], "intro": S["intro"], "prereqs": S["prereqs"],
               "objectives": S["objectives"], "competences": S["competences"], "lessons": [[l["id"], l["title"], l["dur"]] for l in S["lessons"]], "files": files,
               "validator_usage": usage, "deliverables": S["deliverables"], "pass_criteria": S["pass_criteria"], "next": S["next"]}
    w(D + "chapter.json", json.dumps(chapter, ensure_ascii=False, indent=2) + "\n")
    quiz = {"chapter": code, "title": S["title"], "pass_score": 8, "questions": []}
    assert len(S["quiz"]) == 10, "10 questions"
    for q in S["quiz"]:
        if q[2] == "mcq":
            quiz["questions"].append({"id": q[0], "lesson": q[1], "type": "mcq", "q": q[3], "choices": q[4], "answer": q[5], "explain": q[6]})
        else:
            quiz["questions"].append({"id": q[0], "lesson": q[1], "type": "open", "q": q[3], "answer_text": q[4]})
    w(f"QUIZZES/{low}.json", json.dumps(quiz, ensure_ascii=False, indent=2) + "\n")
    w(D + "THEORY.md", f"# {code} — Cours théorique : {S['title']}\n\n" + S["theory"].strip() + "\n")
    w(D + "TUTORIAL.md", f"# {code} — Tutoriels pas à pas\n\n" + S["tutorial"].strip() + "\n\n## Vérifier\n```powershell\n" + usage + " --debug\n```\n\n" + S["honesty"].strip() + "\n")
    les = f"# {code} — Leçons\n"
    for l in S["lessons"]:
        les += f"\n## Leçon {l['id'][1:]} — {l['title']}\n**Niveau :** {S['level']} · **Durée :** {l['dur']} · **Compétence :** {S['competences'][0][0]}\n" + l["body"].strip() + "\n"
    w(D + "LESSON.md", les)
    w(D + "EXERCISES.md", f"# {code} — Exercices\n\n" + S["exercises"].strip() + "\n")
    rows = []
    for b in S["blocks"]:
        for k, dfct, tests in b["counters"]:
            rows.append(f"| `…_{k}` | {dfct} | {tests} |")
    sol_txt = "\n".join(f"`COMPLETED_EXAMPLES/{b['solution']}.blend`" + (f" (+ `_reference.png`)" if b.get("ref_desc") else "") for b in S["blocks"])
    w(D + "SOLUTIONS.md", f"# {code} — Solutions\n\n<!-- QUIZ_ANSWERS_START -->\n<!-- QUIZ_ANSWERS_END -->\n\n## Exercices\n{sol_txt}\n\n**Fabrication.** " + S["fabrication"].strip() + "\n\n## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)\n| Fichier faux | Défaut | Tests qui le refusent |\n|---|---|---|\n" + "\n".join(rows) + "\nAussi refusé : le starter.\n\n## Limites\n" + "\n".join(f"- {x}" for x in S["limits"]) + "\n")
    w(D + "TROUBLESHOOTING.md", f"# {code} — Dépannage\n\n| Symptôme | Cause | Solution |\n|---|---|---|\n" + "\n".join(f"| {a} | {b} | {c} |" for a, b, c in S["trouble"]) + "\n")
    w(D + "RESOURCES.md", f"# {code} — Ressources\n\n" + "\n".join(f"- {x}" for x in S["resources"]) + "\n\nRessources produites (licence BCMA) : starters, solutions, contre-exemples, correcteur éprouvé.\n")
    w(f"CHEAT_SHEETS/{code.replace('.', '_')}_{S['slug']}.md", f"# Fiche de révision — {code} {S['title']}\n\n" + S["cheat"].strip() + "\n")
    print("docs ok", code)
