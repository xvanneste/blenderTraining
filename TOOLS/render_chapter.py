"""
render_chapter.py — Génère README.md et QUIZ.md d'un chapitre, et insère les
réponses du quiz dans SOLUTIONS.md, à partir de :
  <chapitre>/chapter.json            métadonnées du chapitre
  QUIZZES/chNN_MM.json                questions + réponses

Usage : python TOOLS/render_chapter.py <dossier_chapitre> [...]
        python TOOLS/render_chapter.py --all
"""
import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
START, END = "<!-- QUIZ_ANSWERS_START -->", "<!-- QUIZ_ANSWERS_END -->"


def render(cdir):
    meta = json.load(open(os.path.join(cdir, "chapter.json"), encoding="utf-8"))
    code = meta["code"]
    qid = "ch" + code[2:].replace(".", "_").lower()
    qpath = os.path.join(ROOT, "QUIZZES", qid + ".json")
    quiz = json.load(open(qpath, encoding="utf-8"))

    L = [f"# {code} — {meta['title']}", "",
         f"**Phase :** {meta['phase_title']}  ",
         f"**Niveau :** {meta['level']}  ",
         f"**Durée estimée :** {meta['duration']}  ",
         f"**Version :** Blender 5.3.0", "", "## Introduction", "", meta["intro"], "",
         "## Prérequis", ""]
    L += [f"- {p}" for p in meta["prereqs"]]
    L += ["", "## Objectifs pédagogiques", "", "À la fin du chapitre, vous saurez :"]
    L += [f"{i}. {o}" for i, o in enumerate(meta["objectives"], 1)]
    L += ["", "## Compétences évaluées", "", "| Code | Compétence | Validée par |", "|---|---|---|"]
    L += [f"| {c[0]} | {c[1]} | {c[2]} |" for c in meta["competences"]]
    L += ["", "## Plan du chapitre", "", "| Leçon | Titre | Durée |", "|---|---|---|"]
    L += [f"| {l[0]} | {l[1]} | {l[2]} |" for l in meta["lessons"]]
    L += ["", "## Parcours conseillé", "",
          "1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers "
          "[THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).",
          "2. " + meta.get("exercise_path",
                          "Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile."),
          "3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).",
          "4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).",
          "5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).", ""]
    if meta.get("files"):
        L += ["## Fichiers du chapitre", "", "| Fichier | Rôle |", "|---|---|"]
        L += [f"| `{f[0]}` | {f[1]} |" for f in meta["files"]]
        L += [""]
    if meta.get("validator_usage"):
        L += ["## Correcteur automatique", "", "```powershell", meta["validator_usage"], "```", ""]
    L += ["## Livrables attendus", ""]
    L += [f"{i}. {d}" for i, d in enumerate(meta["deliverables"], 1)]
    L += ["", "## Critères pour passer au chapitre suivant", ""]
    L += [f"- {c}" for c in meta.get("pass_criteria",
          [f"Quiz ≥ {quiz['pass_score']}/{len(quiz['questions'])}.",
           "Exercice difficile réussi sans tutoriel.", "Mini-projet ≥ 70/100."])]
    if meta.get("next"):
        L += ["", f"➡️ Chapitre suivant : {meta['next']}"]
    open(os.path.join(cdir, "README.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")

    Q = [f"# {code} — Quiz ({len(quiz['questions'])} questions, seuil {quiz['pass_score']}/{len(quiz['questions'])})",
         "", "Répondez sans regarder le cours, puis corrigez avec [SOLUTIONS.md](SOLUTIONS.md).",
         f"Version interactive : application de l'académie (`QUIZZES/{qid}.json`).", ""]
    for q in quiz["questions"]:
        Q.append(f"**{q['id']}.** ({q.get('lesson', '')}) {q['q']}")
        if q["type"] == "mcq":
            Q.append("")
            Q += [f"   {chr(97 + i)}) {c}" for i, c in enumerate(q["choices"])]
        Q.append("")
    open(os.path.join(cdir, "QUIZ.md"), "w", encoding="utf-8").write("\n".join(Q) + "\n")

    A = [START, "## Réponses du quiz", "", "| Q | Réponse | Explication |", "|---|---|---|"]
    for q in quiz["questions"]:
        if q["type"] == "mcq":
            ans = f"**{chr(97 + q['answer'])}** — {q['choices'][q['answer']]}"
            exp = q.get("explain", "")
        else:
            ans, exp = "—", q.get("answer_text", "")
        A.append(f"| {q['id']} | {ans} | {exp.replace('|', '/')} |")
    A.append(END)
    block = "\n".join(A)
    spath = os.path.join(cdir, "SOLUTIONS.md")
    s = open(spath, encoding="utf-8").read() if os.path.exists(spath) else f"# {code} — Solutions\n"
    if START in s:
        s = s[:s.index(START)] + block + s[s.index(END) + len(END):]
    else:
        lines = s.split("\n", 1)
        s = lines[0] + "\n\n" + block + "\n" + (lines[1] if len(lines) > 1 else "")
    open(spath, "w", encoding="utf-8").write(s)
    print(f"[render] {code}: README, QUIZ ({len(quiz['questions'])} q), réponses insérées")


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    targets = sys.argv[1:]
    if targets == ["--all"]:
        targets = sorted(os.path.dirname(p) for p in glob.glob(os.path.join(ROOT, "*", "CH*", "chapter.json")))
    for t in targets:
        render(os.path.abspath(t))


if __name__ == "__main__":
    main()
