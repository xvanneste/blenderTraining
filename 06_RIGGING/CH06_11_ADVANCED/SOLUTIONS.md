# CH06.11 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **b** — Il le découpe en segments qui peuvent se courber (Bendy Bones) | Avec Segments > 1, le bone se courbe en arche lisse ; avec 1 il est rigide. |
| Q2 | **b** — Rien : le bone est rigide | Mesuré : le milieu du tube est décalé de 0,0 cm avec 1 segment. |
| Q3 | **b** — La courbe est plus lisse : 5,6° contre 17° de virage entre anneaux | Avec 2 segments, la courbe est faite de deux morceaux presque droits. |
| Q4 | — | Un bone avec Segments ≥ 6, use_deform actif, un modificateur Armature sur le tube, des poids sur le bone. |
| Q5 | — | Bone properties > Bendy Bones (non relu dans l'interface 5.3 ; vérifié par l'API : propriété bbone_curveinx). |
| Q6 | **b** — Link garde une référence à la bibliothèque ; Append fait une copie locale | Le contre-exemple « appended » n'a aucune bibliothèque : le rig est une copie, les mises à jour de la bibliothèque ne l'atteignent plus. |
| Q7 | **b** — Pour modifier localement un rig lié sans toucher à l'original | Un lien nu n'est pas éditable ; l'override est la copie éditable qui garde le lien avec la bibliothèque. |
| Q8 | — | Le projet reste déplaçable : le plan retrouve la bibliothèque tant que les deux dossiers gardent leur position relative ; un chemin absolu casse sur une autre machine. |
| Q9 | — | Mesuré en 5.3 : une rotation de bone saisie sans Action n'est pas conservée à la réouverture du plan (0° mesuré) ; une Action est conservée (30° mesurés). |
| Q10 | — | Un override créé seulement pour porter la hiérarchie, non éditable par l'utilisateur ; on utilise do_fully_editable = True (Make > Selected & Content) pour pouvoir poser le rig. |
<!-- QUIZ_ANSWERS_END -->

## Exercices 2 et 3
`COMPLETED_EXAMPLES/ch06_11_bendy_solution.blend` (+ `_reference.png`) ; `COMPLETED_EXAMPLES/ch06_11_shot_solution.blend` (la bibliothèque est `STARTER_FILES/ch06_11_rig_library.blend`).

**Fabrication.** Générés par script (`build_ch06_11_files.py`) : volet A : bone à 8 segments ; volet B : `libraries.load(link=True, relative=True)`, `override_hierarchy_create(do_fully_editable=True)`, location, keyframe. Scores : volet A 23/23 (starter 13/23) ; volet B 34/34 (starter : arrêt anticipé, 0/12).
Croquis regardé : tube droit (1 et 8 segments), tube non courbé à 1 segment, arche lisse à 8 segments.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_bendy_segments_1` | 1 segment : bone rigide | segments ; arche (seuls) |
| `…_bendy_few_segments` | 2 segments : courbe anguleuse | segments ; lissage 17° (arche et extrémités valides) |
| `…_bendy_no_modifier` | modificateur Armature supprimé | déformation ; arche |
| `…_bendy_no_deform` | bone sans déformation | déformation ; arche |
| `…_shot_linked_only` | lien nu, sans override | override ; éditable ; Action ; pose ; bout ; placement (conséquences du lien nu) |
| `…_shot_appended` | copie locale (Append) | bibliothèque (0) ; chemin ; override et conséquences |
| `…_shot_absolute_path` | chemin de bibliothèque absolu | chemin relatif (seul) |
| `…_shot_not_posed` | override sans pose | Action ; angle ; bout (seuls) |
Aussi refusés : les deux starters.

## Limites
- Les bendy bones testés : un seul bone, courbe sur l'axe X ; pas de chaîne.
- La mise à jour de la bibliothèque (changer l'original) n'est pas testée.
- En 5.3 en arrière-plan, une pose d'un rig overridé n'est conservée que par une Action ; le comportement dans l'interface n'a pas été vérifié.
