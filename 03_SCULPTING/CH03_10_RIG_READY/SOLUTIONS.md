# CH03.10 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **b** — Un rig suppose des transformations neutres (échelle 1, rotation 0) : sinon les os et les déformations sont faussés | Mesuré : le starter avait une échelle de 0,01 et une rotation de 4° non appliquées. |
| Q2 | — | Au sol, entre les pieds, en (0, 0, 0) : le personnage se place, se tourne et s'échelonne naturellement, et l'os racine du rig s'y accroche. |
| Q3 | — | Objet CHR_<Nom>_Body (ex. CHR_Hero_Body), données ME_CHR_<Nom>_Body, collection CHR_<Nom> ; aucun suffixe .001, pas d'espace. |
| Q4 | **b** — ≈ 1,76 m (1,55–1,95 pour le correcteur) | Un maillage en centimètres avec une échelle 0,01 donne la bonne taille à l'écran mais des données fausses. |
| Q5 | — | Vers −Y (convention de ce chapitre, comme dans tout le cursus), Z vers le haut ; les orteils dépassent vers −Y. |
| Q6 | **b** — Les épaules et les aisselles se déforment mieux ; on peut peindre les poids et poser les os | Mesuré : A à 38°, T à 90° ; bras le long du corps (4°) refusés. |
| Q7 | — | A : bras à ≈ 30–55° de la verticale, plus proche d'une pose naturelle, moins de déformation d'épaule. T : bras à 90°, plus simple à symétriser et à peindre. Les deux sont acceptées. |
| Q8 | — | Un rig symétrique (Mirror des os, poids en miroir) exige un maillage symétrique ; un bras décalé de 10 cm descend la symétrie à 79 % (mesuré). |
| Q9 | **a** — Object > Set Origin > Origin to 3D Cursor | Placez d'abord le curseur 3D à l'origine du monde (Shift+C) ou sur le centre des pieds. |
| Q10 | — | Sommets isolés (Select All by Trait > Loose Geometry) et doublons (Mesh > Clean Up > Merge by Distance) ; aussi volume fermé et normales vers l'extérieur. |
<!-- QUIZ_ANSWERS_END -->

## Exercice 2
`COMPLETED_EXAMPLES/ch03_10_char_solution.blend` (+ `_reference.png` : face, profil).

**Honnêteté sur la fabrication.** Le mannequin est **généré par script** (`build_ch03_10_files.py`) : 18 ellipsoïdes (bassin, poitrine, cou, tête ; de chaque côté : épaule, bras, avant-bras, main, cuisse, jambe, pied) → Join → Voxel Remesh 1 cm → lissage → coupe plane à z = 0 (pieds plats). C'est un **mannequin simplifié** (sans visage ni doigts), pas un
modèle anatomique ; il illustre la livraison, pas la sculpture.

Mesures du correcteur sur la solution : 1 volume fermé ; taille 1,759 m ; z min 0,04 cm ; centre des pieds x = 0 ; orteils vers −Y ; symétrie 100 % ;
bras à 38,1° (pose A) ; pieds écartés de 36 cm ; 0 sommet isolé. Score 31/31. La variante en pose T (`COUNTER_EXAMPLES/ch03_10_char_tpose_ok.blend`) est **valide** (bras à 90°).

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Test(s) qui le refusent |
|---|---|---|
| `…_wrong_scale` | échelle 0,01 non appliquée | transformations |
| `…_bad_name` | `Cube.001` | nom, données, collection (et rien d'autre) |
| `…_origin_off` | origine au centre du corps (z = 0,9) | transformations (position) |
| `…_arms_down` | bras à 4° de la verticale | pose |
| `…_asymmetric` | bras gauche décalé de 10 cm | symétrie (79 %) |
| `…_floating` | personnage à 30 cm du sol | pieds au sol, écart des pieds |
Aussi refusé : le starter (nom, transformations, symétrie à cause des 4° de rotation).

**Ce que le correcteur a révélé pendant la construction** (consigné aussi dans CLAUDE.md) :
1. la première version du mannequin avait **3 morceaux** : les bras flottaient, détachés du torse (le haut de l'ellipsoïde de poitrine est étroit à la hauteur de l'épaule) ;
   des ellipsoïdes d'épaule ont été ajoutés (le rendu les montrait déjà détachés, mais trop petits pour s'en rendre compte) ;
2. une erreur de tranche sur une séquence bmesh dans le correcteur lui-même (`bm.verts[::k]` n'est pas supporté) : on boucle sur les indices ;
3. ma première consigne disait « pieds écartés de 22 cm » alors que la solution mesure 36 cm (centre à centre) : corrigé dans le fichier et les documents.

## Limites
- Le correcteur ne juge que des conventions mesurables ; il ne juge pas la qualité de la topologie ni de l'anatomie.
- La face vers −Y est déduite des pieds (les orteils dépassent vers −Y) : un modèle sans pieds identifiables ne peut pas être contrôlé.
- Le nom attendu est `CHR_<Nom>_Body` : adaptez la convention à votre pipeline (CH-phase 15).
