# CH06.06 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **b** — Quatre : cuisse, jambe, pied, orteils (avec épaule devant) | thigh, shin, foot, toe (front_ pour l'avant, plus shoulder) : le « genou » arrière est en réalité le jarret. |
| Q2 | **b** — Y (tête vers −Y, queue vers +Y) | Le méta-rig est orienté comme les personnages : la face regarde −Y. |
| Q3 | **a** — Cat, Horse, Wolf, Bird, Shark | Les opérateurs d'ajout existent : armature_cat_metarig_add, horse, wolf, bird, shark, basic_quadruped. |
| Q4 | — | La créature a été construite autour du méta-rig d'origine : tout écart d'échelle ou de position désaligne les os et les volumes (écarts de 22 à 44 cm mesurés avec une échelle de 1,4). |
| Q5 | — | Échelle globale, puis ajustement des os en Edit Mode (X-Ray) : colonne, épaules, genoux/jarrets, pieds, queue ; avant de générer. |
| Q6 | **a** — front_foot_ik.L | Contrôleur IK du pied avant ; foot_ik.L est celui de la patte arrière gauche. |
| Q7 | **b** — 283 | 34 bones de méta-rig donnent 283 bones générés (DEF-, ORG-, MCH-, contrôleurs). |
| Q8 | — | Qu'elles restent immobiles (≤ 10 mm) quand la patte avant gauche est levée de 0,15 m : pas de poids parasites entre pattes. |
| Q9 | — | Le rig est à 0,5 m de la créature : les poids Automatic Weights sont calculés entre des objets qui ne coïncident pas ; la patte du maillage ne suit pas son os. |
| Q10 | — | Pattes arrière à jarret (articulation inversée), queue et cou à plusieurs os (spine.00x), épaules mobiles (shoulder.L/.R), poids entre pattes voisines. |
<!-- QUIZ_ANSWERS_END -->

## Exercice 2
`COMPLETED_EXAMPLES/ch06_06_quadruped_solution.blend` (+ `_reference.png`).

**Fabrication.** Générée par script (`build_ch06_06_files.py`) avec les opérateurs réels (méta-rig Basic Quadruped, `rigify_generate`, Automatic Weights, normalisation, Limit Total). Score du correcteur 51/51 ; starter 2/8 (rig absent : arrêt anticipé). Mesures : THEORY.md §4.
Croquis regardé : capsules autour des os ; patte avant gauche levée et pliée, trois autres pattes immobiles.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_not_generated` | méta-rig seul | Rig généré (arrêt anticipé) |
| `…_unskinned` | créature non liée | Corps lié ; groupes ; poids ; mouvements (conséquences) |
| `…_wrong_scale` | méta-rig à l'échelle 1,4 (écarts de 22 à 44 cm) | Ajustement (seul) |
| `…_no_modifier` | modificateur Armature supprimé | Modificateur ; mouvements (conséquences) |
| `…_partial_weights` | poids retirés aux pattes avant (77 % pesés) | Sommets pesés ; racine ; patte |
| `…_offset` | rig décalé de 0,5 m en X | Centrage (50 cm) ; patte levée |
Aussi refusé : le starter.

## Limites
- Créature synthétique construite sur le méta-rig d'origine ; pas d'ajustement à une anatomie libre.
- Seule la patte avant gauche est testée en IK ; pas de queue, cou, tête.
