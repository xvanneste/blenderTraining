# CH18.06 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | — | D'une suite de points en 3D (position, rayon, opacité), appartenant à une image clé d'un calque d'un objet GP. |
| Q2 | **b** — Blank | Blank : un calque, un matériau, aucun trait. |
| Q3 | **c** — Sculpt Mode | Sculpt Mode déforme les traits au pinceau (Smooth, Push, Twist…). |
| Q4 | — | Les workspaces « 2D Animation » et « 2D Full Canvas », un objet GP Stroke et une caméra, en 1920×1080 à 24 i/s. |
| Q5 | — | Pour travailler chaque étape séparément : esquisse verrouillée et pâle, encrage, couleur ; on peut masquer, verrouiller ou modifier l'un sans abîmer les autres. |
| Q6 | — | Panneau Layers : icône dossier (Add New Layer Group), puis glisser-déposer le calque sur la ligne du groupe. |
| Q7 | **b** — Pour chaque élément qui bouge ou se place indépendamment (personnage, décor, effets) | Un objet par élément indépendant ; les calques organisent le contenu d'un même objet. |
| Q8 | — | Origin, 3D Cursor, Surface, Stroke. |
| Q9 | — | Activer la passe Z : Properties → View Layer → Passes → Data → Z. |
| Q10 | **b** — À ordonner les traits entre eux : ordre des calques (2D Layers) ou position 3D réelle (3D Location) | Il ordonne les traits entre eux ; l'occlusion par les maillages au rendu dépend de la passe Z. |
<!-- QUIZ_ANSWERS_END -->

## Exercice 2
Le correcteur signale : « Groupe de calques CHAR contenant LINE et COLOR » ✘, « Objet Grease
Pencil GP_Background » ✘ (renommé), « rangé dans DRAWINGS » ✘. Réparation : glisser COLOR dans
CHAR ; `F2` → GP_Background ; `M` → DRAWINGS.

## Exercice 3
Référence : `COMPLETED_EXAMPLES/ch18_06_gp_scene_solution.blend` (générée par
`SCRIPTS/build_ch18_06_files.py`) et `ch18_06_gp_scene_reference.png` :
- `GP_Character` à Y = 1,5 (la maison est à Y = 4) ; calques `SKETCH` (verrouillé, opacité 0,3),
  groupe `CHAR` contenant `LINE` (mannequin) et `COLOR` (hachures rouges) ;
- `GP_Background` à Y = 9 : deux lignes de collines, nuages, ligne d'horizon ;
- passe Z activée : sur le rendu de référence, la maison et l'arbre **cachent** les collines.
Points de contrôle mesurés par le correcteur : distance moyenne des points à la caméra (devant /
derrière la maison), part des points dans le cadre de CAM_Shot (≥ 60 %).
