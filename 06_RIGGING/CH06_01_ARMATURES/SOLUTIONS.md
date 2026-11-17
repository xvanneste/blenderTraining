# CH06.01 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **a** — Tête, queue et roll | Head (tête), tail (queue) et roll (rotation autour de l'axe du bone). |
| Q2 | **b** — La tête du bone est collée à la queue de son parent | use_connect : la tête suit la queue du parent ; typique d'une chaîne (cuisse, tibia, pied). |
| Q3 | **b** — Elle part du côté de la colonne, pas de sa queue : sa tête ne coïncide pas avec la queue du parent | Une connexion force la tête sur la queue du parent : shoulder et thigh partent d'un autre point. |
| Q4 | — | Blender (miroir en Pose Mode, Symmetrize, X-Axis Mirror, Auto-Weights symétriques) reconnaît ces suffixes pour associer un bone à son jumeau ; un nom comme « Bone.001 » ne dit rien du côté. |
| Q5 | — | Un bone racine au sol, parent de tout : on déplace tout le personnage en le bougeant ; il ne déforme pas la peau (use_deform = False). |
| Q6 | **a** — Construire un côté puis Symmetrize (Armature > Symmetrize) | Symmetrize crée/aligne les bones du côté opposé selon les suffixes .L/.R. |
| Q7 | **a** — Qu'aucun bone n'est transformé en Pose Mode (position, rotation, échelle à l'identité) | La pose de repos doit être neutre : les animations partent de là. |
| Q8 | — | L'épaule gauche est décalée de 5 cm : l'écart avec l'image miroir de l'épaule droite (≈ 5,8 cm) dépasse 2 mm ; le miroir de pose et l'auto-weights seront faux. |
| Q9 | — | Le personnage doit être posé sur le sol : la queue de toe à z = 0 ± 2 cm ; sinon il flotte ou s'enfonce dès le rig. |
| Q10 | — | Dans les propriétés du bone (Bone Properties > Deform) ; en script, `bone.use_deform`. |
<!-- QUIZ_ANSWERS_END -->

## Exercice 2
`COMPLETED_EXAMPLES/ch06_01_armature_solution.blend` (+ `_reference.png`).

**Fabrication.** Générée par script (`build_ch06_01_files.py`) : 25 bones créés par `edit_bones.new` avec tête, queue, parent et connexion ; côté droit par miroir X → −X ; `use_deform` désactivé pour root. Score du correcteur 48/48 ; starter 0/4 (objet RIG_Hero absent : arrêt anticipé).
Croquis comparé au mannequin (de face et de profil) : les bones suivent l'axe du corps, les bras suivent la pose en A, les jambes descendent jusqu'aux pieds.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Test qui le refuse |
|---|---|---|
| `…_missing_right` | bras droit absent (shoulder à hand .R) | Bones présents ; côtés .L/.R (même défaut) |
| `…_bad_names` | noms par défaut « Bone », « Bone.001 », « Bone.003 » | Bones présents ; bones en trop ; côtés ; hiérarchie (conséquences du renommage) |
| `…_asymmetric` | épaule gauche décalée de 5 cm | Symétrie X : écart de 5,8 cm (seul) |
| `…_unparented` | hand.L sans parent | Hiérarchie ; connexions (même défaut) |
| `…_disconnected` | spine.002 non connecté | Connexions (seul) |
| `…_pose_dirty` | upper_arm.L et head transformés en Pose Mode | Pose de repos propre (seul) |
| `…_deform_root` | root avec Deform actif | Déformation (seul) |
Aussi refusé : le starter.
Deux défauts du correcteur ont été corrigés grâce aux contre-épreuves : la lecture des noms de bones pour les connexions (`spine.001`) et la construction du contre-exemple « asymétrique » (un bone connecté ne peut pas être décalé : sa connexion le remet en place).

## Limites
- Structure et positions ; aucune évaluation de la qualité de déformation (CH06.03).
- La liste de bones est fixée : 25 bones, sans doigts ni visage.
