"""
final_audit.py — Génère FINAL_AUDIT.md à partir de l'état RÉEL des fichiers.

Rien n'est déclaratif : statuts calculés par academy_status (documents, quiz, tests passants),
registre d'assets vérifié, présence des livrables globaux exigés par la mission.
Statuts : Terminé et vérifié / Terminé mais non vérifié / Partiellement terminé / Bloqué /
Non commencé.

Usage : python TOOLS/final_audit.py
"""
import datetime
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "TOOLS"))
import academy_status as S  # noqa: E402

GLOBAL = [
    ("README.md", "Présentation"), ("START_HERE.md", "Démarrage"), ("CURRICULUM.md", "Programme 19 phases"),
    ("ROADMAP.md", "Feuilles de route 5/10/20 h"), ("PROGRESS.md", "Suivi apprenant"),
    ("CLAUDE.md", "Instructions de reprise"), ("PROJECT_STATE.md", "État et décisions"),
    ("TASKS.md", "Inventaire des tâches (généré)"), ("ASSET_MANIFEST.json", "Registre des ressources"),
    ("DOCUMENTATION/CONVENTIONS.md", "Conventions"), ("DOCUMENTATION/VERSION_COMPATIBILITY.md", "Compatibilité"),
    ("DOCUMENTATION/PIPELINE_BRIDGES.md", "Passerelles du pipeline"),
    ("DOCUMENTATION/COMPLEMENTARY_SOFTWARE.md", "Logiciels complémentaires"),
    ("TOOLS/run_all_tests.py", "Tests automatiques"), ("TOOLS/build_site.py", "Application de consultation"),
    ("SITE/index.html", "Application générée"),
]


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    chapters = S.curriculum_chapters()
    tests = S.last_results()
    rows, count = [], {}
    by_phase = {}
    for ph, num, title in chapters:
        st, d, missing = S.chapter_status(ph, num, tests)
        label = st.split(" ", 1)[1]
        count[label] = count.get(label, 0) + 1
        by_phase.setdefault(ph, []).append((f"CH{ph:02d}.{num:02d}", title, label, missing))
    res = json.load(open(os.path.join(ROOT, "TOOLS", "last_test_results.json"), encoding="utf-8"))["results"]
    n_ok = sum(1 for r in res if r["ok"])
    man = json.load(open(os.path.join(ROOT, "ASSET_MANIFEST.json"), encoding="utf-8"))
    assets = man["assets"] if isinstance(man, dict) and "assets" in man else man
    total = len(chapters)
    done = count.get("Terminé et vérifié", 0)
    L = []
    L.append("# FINAL_AUDIT — Audit de l'académie (généré, état réel)")
    L.append("")
    L.append(f"**Généré le :** {datetime.date.today():%d/%m/%Y} par `python TOOLS/final_audit.py` · "
             f"Blender de référence : 5.3.0")
    L.append("")
    L.append("> Ce document est recalculé à partir des fichiers : il ne peut pas annoncer comme terminé un")
    L.append("> chapitre dont un document, le quiz ou les tests manquent.")
    L.append("")
    L.append("## Verdict")
    L.append("")
    verdict = "TERMINÉE" if done == total else "NON TERMINÉE"
    L.append(f"**La formation est {verdict}** : {done} chapitres sur {total} sont terminés et vérifiés "
             f"({100 * done / total:.0f} %).")
    L.append("")
    L.append("| Statut | Chapitres |")
    L.append("|---|---|")
    for k in ("Terminé et vérifié", "Terminé mais non vérifié", "Partiellement terminé", "Bloqué", "Non commencé"):
        L.append(f"| {k} | {count.get(k, 0)} |")
    L.append("")
    L.append(f"Tests automatiques (dernière exécution enregistrée) : **{n_ok} / {len(res)} réussis**. "
             f"Ressources enregistrées dans ASSET_MANIFEST.json : **{len(assets)}**.")
    L.append("")
    L.append("## Par phase")
    L.append("")
    L.append("| Phase | Vérifiés | Total | Statut de la phase |")
    L.append("|---|---|---|---|")
    for ph in sorted(by_phase):
        items = by_phase[ph]
        ok = sum(1 for i in items if i[2] == "Terminé et vérifié")
        st = ("Terminé et vérifié" if ok == len(items) else "Non commencé" if ok == 0 and
              all(i[2] == "Non commencé" for i in items) else "Partiellement terminé")
        L.append(f"| {ph} — {S.PHASE_DIRS[ph]} | {ok} | {len(items)} | {st} |")
    L.append("")
    L.append("## Livrables globaux exigés")
    L.append("")
    L.append("| Élément | Fichier | Présent |")
    L.append("|---|---|---|")
    for f, label in GLOBAL:
        L.append(f"| {label} | `{f}` | {'oui' if os.path.exists(os.path.join(ROOT, f)) else '**NON**'} |")
    L.append("")
    L.append("## Exigences de la mission non encore satisfaites")
    L.append("")
    missing_phases = [ph for ph in sorted(by_phase) if any(i[2] != "Terminé et vérifié" for i in by_phase[ph])]
    L.append(f"- Chapitres restants : {total - done} (phases incomplètes : {', '.join(str(p) for p in missing_phases)}).")
    gp = by_phase.get(18, [])
    proj = next((i for i in gp if i[0] == "CH18.22"), None)
    L.append(f"- Phase 18 : 7 projets obligatoires (CH18.22) — statut : {proj[2] if proj else 'inconnu'}.")
    L.append("- Passerelles du pipeline obligatoires en phases 15 et 16 : documentées dans "
             "`DOCUMENTATION/PIPELINE_BRIDGES.md` ; leur mise en pratique dépend des chapitres des phases 15–16.")
    L.append("- Parcours de logiciels complémentaires : guide et plans de cours produits ; chapitres détaillés en "
             "attente de l'installation des logiciels **par l'utilisateur** (aucune installation sans accord).")
    L.append("- Phase 14 (IA) : chaque outil doit être vérifié (disponibilité, licence) au moment de la rédaction.")
    L.append("")
    L.append("## Détail des chapitres non terminés (hors « Non commencé »)")
    L.append("")
    other = [(c, t, s, m) for ph in sorted(by_phase) for (c, t, s, m) in by_phase[ph]
             if s not in ("Terminé et vérifié", "Non commencé")]
    if other:
        for c, t, s, m in other:
            L.append(f"- {c} {t} — {s} : {', '.join(m)}")
    else:
        L.append("- Aucun : chaque chapitre est soit terminé et vérifié, soit non commencé.")
    L.append("")
    L.append("## Méthode de vérification")
    L.append("")
    L.append("- Chaque `.blend` est généré par script, chaque solution est acceptée et chaque fichier de départ "
             "refusé par le correcteur du chapitre (`TOOLS/run_all_tests.py`).")
    L.append("- Chaque solution est rendue en image de référence, et l'image est regardée (pas seulement le score).")
    L.append("- Les libellés d'interface sont vérifiés dans les sources `bl_ui` et la keymap de Blender 5.3.0.")
    L.append("- Les comportements surprenants sont mesurés (voir CLAUDE.md, « Pièges »), puis enseignés.")
    open(os.path.join(ROOT, "FINAL_AUDIT.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    print(f"[audit] {done}/{total} chapitres vérifiés ; tests {n_ok}/{len(res)} ; verdict : {verdict}")


if __name__ == "__main__":
    main()
