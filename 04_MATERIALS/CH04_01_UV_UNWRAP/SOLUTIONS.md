# CH04.01 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **b** — Il indique où couper la surface 3D pour la déplier à plat | Comme les coutures d'un vêtement : on coupe pour pouvoir aplatir sans déchirer ni étirer. |
| Q2 | — | Sur les arêtes vives (angle > 50° ici) et à des endroits peu visibles ; une surface courbe développable (couvercle) peut rester d'un seul tenant. |
| Q3 | **a** — Des carrés réguliers de même taille partout | Des bandes ou des carrés étirés = distorsion (starter du chapitre : étirement moyen 1,59). |
| Q4 | — | Unwrap Angle Based, Unwrap Conformal, Unwrap Minimum Stretch (menu UV > Unwrap), plus Smart UV Project, Follow Active Quads, Cube Projection. |
| Q5 | — | Par triangle, le rapport des valeurs singulières du jacobien 3D→UV (1 = aucune distorsion) ; moyenne pondérée par l'aire ≤ 1,15 et 95ᵉ centile ≤ 1,6. |
| Q6 | **b** — À donner la même densité de texels à tous les îlots | Sans lui, une face de 1 m peut avoir autant de pixels qu'une de 10 cm : texture floue ici, nette là. |
| Q7 | — | Deux faces qui partagent les mêmes pixels partagent la même peinture ; incompatible avec le baking et la peinture. (Exception volontaire : miroir de parties symétriques.) |
| Q8 | **a** — [0, 1] × [0, 1] | Hors du carré, la texture se répète (ou tombe dans une autre tuile UDIM : CH04.02). |
| Q9 | — | 68 % ; un espace UV perdu est une résolution de texture perdue (le correcteur exige ≥ 50 %). |
| Q10 | — | Margin (avec Margin Method : Scaled, Add ou Fraction) ; une marge trop faible fait « baver » un îlot sur l'autre au mip-mapping et au baking. |
<!-- QUIZ_ANSWERS_END -->

## Exercice 2
`COMPLETED_EXAMPLES/ch04_01_chest_solution.blend` (+ `_reference.png` damier ; `_uv_layout.png` disposition UV).

**Fabrication.** Générée par script (`build_ch04_01_files.py`) avec les opérateurs réels : seams sur les arêtes d'angle > 50° (124 arêtes), `uv.unwrap` (Angle Based), `uv.average_islands_scale`, `uv.pack_islands`
(marge 2 %, rotation). Aucun contournement : ces opérateurs fonctionnent en arrière-plan en 5.3.

Mesures du correcteur sur la solution : 22 îlots ; étirement moyen 1,000 (95ᵉ centile 1,000) ; densité (écart-type du log) 0,000 ; chevauchement 0 % ; occupation 68 % ; UV de 0,01 à 0,99 ; 124 seams. Score 21/21.
Starter : étirement 1,59 (2,76), densité 0,26, chevauchement (union/somme 23 %), occupation 12 %, 0 seam : 6/21.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Test qui le refuse |
|---|---|---|
| `…_overlapping` | tous les îlots ramenés à l'origine | chevauchement (15,5 %) et occupation (10 %) |
| `…_unequal_density` | un îlot sur deux agrandi ×2,6, puis repacké | densité (0,47) — et elle seule |
| `…_out_of_bounds` | UV ×1,7 | limites [0, 1] (−0,29 à 1,39) — et elles seules |
| `…_tiny_pack` | UV ×0,3 | occupation (6 %) — et elle seule |
Aussi refusé : le starter.

**Ce que le développement a appris** :
1. une première version de « densité inégale » agrandissait des îlots autour de leur centre : ils se recouvraient aussi (chevauchement 50 %) ; il faut agrandir puis **repacker** pour isoler le défaut ;
2. `bpy.data.images.new` n'accepte pas `generated_type` : créer l'image puis `img.generated_type = 'UV_GRID'` ;
3. le seuil d'uniformité de densité a été resserré de 0,25 à 0,20 car le starter ne le dépassait que de 0,01.

## Limites
- La densité uniforme est exigée : un choix volontaire de densité (visage plus détaillé) sera refusé par ce correcteur (exercice 3).
- Pas de contrôle de la marge entre îlots ni de leur orientation.
- La mesure de chevauchement est rastérisée à 1024² : des recouvrements inférieurs à ≈ 2 % ne sont pas détectés.
