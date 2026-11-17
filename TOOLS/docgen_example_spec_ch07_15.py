import sys
sys.path.insert(0, r"G:/_formation/blender/BLENDER_CINEMA_MASTER_ACADEMY/TOOLS")
from docgen import make

S = dict(
    phase_dir="07_ANIMATION", dir="CH07_15_DIALOGUE", pfx="ch07_15_dialogue", code="CH07.15", title="Scène dialoguée", slug="dialogue",
    phase_title="7 — Animation 3D", level="expert", duration="10 h", exercises_validator=None,
    intro="Une scène dialoguée se construit par étapes : le BLOCKING (les poses clés qui racontent la scène, en interpolation Constant pour juger les poses sans les mouvements), le SPLINING (on passe en courbes lisses et on ajoute des breakdowns), puis le POLISH (overlap, détails). Ce chapitre applique la méthode au regard d'un personnage dans une conversation à trois (A à gauche, B à droite, la caméra) : sept poses, trois breakdowns, des maintiens qui restent plats et des marqueurs qui jalonnent la scène. Le correcteur lit les deux actions (BLOCK et FINAL) et l'animation évaluée.",
    prereqs=["CH07.02–07.04 (clés, courbes), CH07.07 (posing), CH07.10 (acting)."],
    objectives=["Construire un blocking en poses clés (Constant).", "Passer en splining sans perdre les poses.", "Ajouter des breakdowns et garder les maintiens plats.", "Baliser une scène par des marqueurs."],
    competences=[["C07.15.a", "Scène dialoguée", "Exercice 2 (correcteur) + courbes de la solution"]],
    lessons=[
        dict(id="L1", title="Le blocking", dur="5 h", body="### A. Comprendre\nPoses clés, Constant, marqueurs. → THEORY.md §1–3.\n### D. Pratiquer\n- **Facile :** exercice 1.\n### G. Évaluer\nQuiz Q1–Q5."),
        dict(id="L2", title="Splining et polish", dur="5 h", body="### A. Comprendre\nBezier, breakdowns, maintiens. → THEORY.md §4–8.\n### B. Observer\n`ch07_15_dialogue_reference.png`.\n### C. Reproduire\nTutoriels 1 à 5.\n### D. Pratiquer\n- **Moyen :** exercice 2 ; **Difficile :** exercice 3.\n### E. Déboguer\nTROUBLESHOOTING.md.\n### F. Optimiser\nGarder BLOCK : on peut toujours y revenir.\n### G. Évaluer\nQuiz Q6–Q10 ; correcteur `--exercise dialogue`."),
    ],
    blocks=[dict(exercise="dialogue", starter="ch07_15_dialogue_starter", solution="ch07_15_dialogue_solution", cprefix="ch07_15_dialogue",
                 starter_desc="Tête GEO_Head avec l'action BLOCK active (7 poses en Constant), sans FINAL ni marqueurs", solution_desc="BLOCK intacte, FINAL active (Bezier, 3 breakdowns), marqueurs beat_1 à beat_7",
                 ref_desc="Blocking en escalier (gris) et splining (orange) : poses en blanc, breakdowns en vert",
                 counters=[("still_stepped", "FINAL encore en Constant", "breakdowns ; Bezier ; mouvement lisse"), ("no_breakdowns", "aucun breakdown", "breakdowns (seul)"), ("drift", "pose modifiée (+55° au lieu de +40°)", "poses conservées ; mouvement lisse ; maintiens"),
                           ("hold_lost", "un breakdown dans un maintien", "maintiens plats ; mouvement lisse (seuls)"), ("no_markers", "aucun marqueur", "marqueurs (seul)"), ("block_active", "BLOCK reste l'action active", "FINAL active ; mouvement lisse")])],
    counter_desc="Fichiers FAUX volontaires (reste en Constant, sans breakdowns, pose modifiée, maintien cassé, sans marqueurs, mauvaise action active)",
    deliverables=["Scène en blocking puis splining validée.", "Auto-évaluation ≥ 7/10."], pass_criteria=["Quiz ≥ 8/10.", "Exercice 2 validé."],
    next="[Projet P7 — Scène animée](../PROJECT_P7/README.md)",
    quiz=[
        ("Q1", "L1", "mcq", "Qu'est-ce que le blocking ?", ["Les poses clés principales, souvent en Constant", "Le rendu final", "Un type de caméra", "Un shape key"], 0, "Sept poses aux images 1, 13, 25, 37, 49, 61, 73."),
        ("Q2", "L1", "mcq", "Pourquoi l'interpolation Constant en blocking ?", ["On juge les poses sans les mouvements entre elles", "Elle est plus rapide à rendre", "Elle supprime les clés", "Elle évite les marqueurs"], 0, "Le regard saute de pose en pose : on lit l'histoire."),
        ("Q3", "L1", "mcq", "À quoi servent les marqueurs ?", ["Baliser les moments clés de la scène", "Changer la couleur", "Animer la caméra", "Supprimer des clés"], 0, "beat_1 à beat_7 aux images des poses (touche M)."),
        ("Q4", "L1", "open", "Pourquoi garder BLOCK intacte ?", "Pour comparer, corriger les poses sans perdre le splining, et revenir au blocking si le polish dérive."),
        ("Q5", "L1", "open", "Pourquoi les poses sont-elles 0, +40, +40, −30, −30, 0, 0 ?", "Neutre, regarde A, écoute A, regarde B, écoute B, regarde la caméra, maintien final : chaque maintien est une écoute."),
        ("Q6", "L2", "mcq", "Qu'est-ce qu'un breakdown ?", ["Une clé entre deux poses qui précise le trajet", "Une panne", "Un marqueur", "Un modificateur"], 0, "Images 7 (+22°), 31 (+5°), 55 (−12°) : ils décident du trajet entre les poses."),
        ("Q7", "L2", "mcq", "Que doit-il arriver aux maintiens au splining ?", ["Rester plats", "Osciller", "Disparaître", "Être raccourcis"], 0, "Deux clés égales en Auto Clamped donnent une valeur plate : 0,0° d'écart mesuré."),
        ("Q8", "L2", "open", "Que montre « hold_lost » ?", "Un breakdown (25°) dans le maintien : la tête dérive de 15° pendant l'écoute ; le personnage ne tient plus son regard."),
        ("Q9", "L2", "open", "Pourquoi les poses ne doivent-elles pas changer au splining ?", "Le blocking a été validé : le splining règle le mouvement, pas l'histoire ; contre-exemple « drift » : +55° au lieu de +40°."),
        ("Q10", "L2", "open", "Qu'ajoute le polish ?", "L'overlap et le follow-through, les détails (clignements, respirations), le timing fin : CH07.06, CH07.10, CH07.11."),
    ],
    theory="""
## 1. Les étapes d'une scène
1. **Blocking** : poses clés principales, souvent en interpolation Constant ; on valide l'histoire et le timing des poses.
2. **Splining** : passage en courbes (Bezier), ajout de breakdowns entre les poses, réglage des maintiens.
3. **Polish** : overlap, follow-through, détails (clignements, souffle), nettoyage des courbes.

## 2. La scène de l'exercice
GEO_Head (sphère de 25 cm avec un nez pour lire l'orientation), lacet autour de Z, 73 images à 24 i/s. Poses : 1 neutre (0°), 13 regarde A (+40°), 25 écoute A (+40°), 37 regarde B (−30°), 49 écoute B (−30°), 61 regarde la caméra (0°), 73 maintien final (0°).

## 3. Marqueurs
beat_1 à beat_7 aux images des poses : repères pour la navigation et le montage (touche M dans la timeline).

## 4. Splining
Action FINAL (active) : mêmes poses en Bezier (poignées Auto Clamped) et trois breakdowns : image 7 (+22°), 31 (+5°), 55 (−12°). Un breakdown choisit le trajet (courbe plus rapide au début, plus lente à la fin...) sans changer les poses.

## 5. Les maintiens
Entre deux clés de même valeur (13–25, 37–49, 61–73), la courbe Auto Clamped reste plate : écarts mesurés de 0,0° aux images 19, 43, 67. Un breakdown placé dans un maintien le casse.

## 6. Mesures
Solution : 36/36 ; BLOCK : 7 clés, toutes Constant ; FINAL : 10 clés (7 poses + 3 breakdowns), toutes Bezier ; variation maximale du lacet 8,7°/image ; maintiens à 0,0° d'écart. Contre-exemples : FINAL en Constant (saut de 70°) ; aucun breakdown ; pose à 55° (écart de 13,1° au maintien) ; breakdown de 25° dans un maintien (15,0°) ; aucun marqueur ; BLOCK active (saut de 70°).

## 7. Pièges
- Splinner en détruisant le blocking (travailler dans la même action).
- Breakdown dans un maintien.
- Modifier les poses pendant le splining.
- Oublier d'activer FINAL.
- Marqueurs mal nommés.

## 8. Limites
Un objet, un canal (le lacet) ; pas de dialogue audio ni de lip sync dans cette scène (CH07.11) ; le polish est présenté, non mesuré ; le correcteur lit des clés et des valeurs, pas la justesse du jeu.
""",
    tutorial="""
Ouvrez `STARTER_FILES/ch07_15_dialogue_starter.blend` (BLOCK active). Sauvegardez sous `ch07_15_dialogue_starter_<prenom>_v001.blend`.

## Tutoriel 1 — Lire le blocking (10 min)
Lisez l'animation (Espace) : le regard saute de pose en pose. Dope Sheet : 7 clés en Constant.

## Tutoriel 2 — Dupliquer (10 min)
Éditeur d'action : dupliquez « BLOCK » ; renommez la copie « FINAL » ; assurez-vous que FINAL est l'action de GEO_Head (BLOCK en utilisateur fictif).

## Tutoriel 3 — Splining (15 min)
Dope Sheet (action FINAL) : toutes les clés : T > Bezier ; Graph Editor : V > Auto Clamped.

## Tutoriel 4 — Breakdowns (15 min)
Image 7 : lacet +22°, clé ; image 31 : +5°, clé ; image 55 : −12°, clé. Pas de clé dans les maintiens.

## Tutoriel 5 — Marqueurs (10 min)
Timeline : M aux images 1, 13, 25, 37, 49, 61, 73 ; F2 pour nommer beat_1 à beat_7.
""",
    honesty="Remarque d'honnêteté : les fichiers sont générés par script (clés, interpolation, poignées, marqueurs) ; les touches T, V, M et F2 sont celles de la keymap par défaut (vérifiées dans `blender_default.py`) ; le bouton de duplication de l'éditeur d'action et la gestion de l'utilisateur fictif n'ont pas été relus dans l'interface 5.3. Le croquis (numpy) a été regardé : escalier gris du blocking, courbe orange du splining, maintiens plats. Ce chapitre ne mesure pas le polish.",
    exercises="""
## Exercice 1 — Facile : blocking ⏱ 30 min
Sur papier, notez sept poses d'un personnage qui reçoit une mauvaise nouvelle (images et regard).

## Exercice 2 — Moyen : le splining ⏱ 4 h
Partez du starter. Validation : `--exercise dialogue`.

## Exercice 3 — Difficile : la scène complète ⏱ 10 h
Reprenez la méthode sur un plan de dialogue de 10 secondes avec deux personnages (CH07.10 et CH07.11) : blocking, splining, polish ; documentez les trois étapes.

### Grille d'auto-évaluation (sur 10)
| Critère | 0 | 1 | 2 |
|---|---|---|---|
| BLOCK intacte (Constant) | non | partiel | oui |
| FINAL active, poses conservées | non | partiel | oui |
| Breakdowns ajoutés, Bezier | non | partiel | oui |
| Maintiens plats | non | partiel | oui |
| Marqueurs beat_1 à beat_7 | non | partiel | oui |
**≥ 7/10** : acquis.

## Défis
- **Défi 1 :** ajoutez un overlap (le corps suit la tête de 2 images) en polish.
- **Défi 2 :** ajoutez un clignement au beat_3.

## Mini-projet
Une scène de 5 secondes en trois étapes (blocking, splining, polish), trois fichiers de la même scène.
""",
    fabrication="Générées par script (`build_ch07_15_files.py`) : tête et nez, actions BLOCK (Constant) et FINAL (Bezier, Auto Clamped, breakdowns), marqueurs. Score 36/36 ; starter : arrêt anticipé (pas de FINAL). Courbe regardée.",
    limits=["Un objet et un canal (le lacet) ; pas de dialogue audio, pas de polish mesuré.", "Les contre-exemples « still_stepped » et « block_active » échouent aussi sur le mouvement lisse (le saut de 70° vient de l'interpolation Constant) ; « drift » aussi sur le maintien et le mouvement.", "Le correcteur lit des clés et des valeurs, pas la justesse du jeu."],
    trouble=[("Le regard saute", "FINAL en Constant ou BLOCK active", "Bezier et FINAL active"), ("La tête dérive pendant l'écoute", "Breakdown dans un maintien", "Supprimer la clé du maintien"), ("Les poses ont changé", "Modifications pendant le splining", "Revenir aux valeurs de BLOCK"), ("BLOCK est modifiée", "Travail dans la mauvaise action", "Restaurer BLOCK, travailler dans FINAL"),
             ("Les maintiens ondulent", "Poignées libres", "Auto Clamped"), ("Marqueurs sans nom", "Renommage oublié", "F2"), ("Une action disparaît", "Pas d'utilisateur", "Utilisateur fictif"), ("Mouvement trop brusque", "Trop peu de breakdowns", "Ajouter des breakdowns")],
    resources=["Références : aucun ouvrage n'est cité ici faute de titre vérifié.", "Manuel Blender 5.3 : *Animation & Rigging > Graph Editor*, *Markers*, *Actions*.",
               "Vérifié par l'API 5.3 : `Keyframe.interpolation`, `handle_left_type` (AUTO_CLAMPED), `Scene.timeline_markers`, `AnimData.action`, `Action.use_fake_user`.", "Keymap par défaut : T (interpolation), V (type de poignée), M (marqueur), F2 (nom du marqueur).", "Liens : CH07.04, CH07.07, CH07.10, CH07.11, projet P7."],
    cheat="Blocking (poses, Constant) → splining (Bezier, breakdowns, maintiens plats) → polish (overlap, détails). BLOCK intacte, FINAL active, marqueurs beat_n. Poses : 0, +40, +40, −30, −30, 0, 0.\nCorrecteur : `--exercise dialogue [--debug]`.",
)
make(S)
