# Projet de phase P6 — « Un personnage contrôlable »

**Phase :** 6 — Rigging professionnel · **Durée estimée :** 25 à 35 h · **Évalue :** C06.01 → C06.11

## Brief
Rendez **contrôlable** le personnage de la phase 3 (ou un personnage de votre choix, humanoïde, 1,76 m environ) : un **rig Rigify généré**, un **corps lié proprement**, un rig **ergonomique** (l'animateur ne voit que les contrôles),
et un **test de pose** animé qui prouve que le personnage obéit : une pose de repos, une pose avec un pied levé et la tête tournée. Montrez le résultat sur une **planche de trois images**.
Ce personnage sera animé en phase 7 et placé dans les plans du court-métrage (phases 9 et 15).

## Livrables
1. `PROJECTS/p6_rig/p6_rig_<prenom>_v0NN.blend` : `CHR_Hero_Body` (corps), `RIG_Hero` (rig Rigify généré), éventuellement `META_Hero` (méta-rig) ; une Action de test sur `RIG_Hero`.
2. `PROJECTS/p6_rig/renders/p6_posetest.png` : trois images de l'animation de test côte à côte, ≥ 1 600 px de large.
3. `PORTFOLIO/p6/` : capture des collections de bones, trois poses commentées, 10 lignes (choix, difficultés, ce qu'il reste à améliorer).

## Contraintes techniques (vérifiées par `validate_p6.py`)
1. **Rig** : généré par Rigify (≥ 400 bones, noms `root`, `torso`, `head`, `foot_ik.L`, `hand_ik.L`, `DEF-spine`, `DEF-thigh.L`, bones `ORG-` et `MCH-`) ; ≥ 10 collections de bones ; échelle 1 ; taille 1,76 ± 0,12 m ; pieds au sol ; centré sous le corps.
2. **Peau** : corps parenté au rig avec un modificateur Armature ; poids sur les bones `DEF-` ; ≥ 98 % de sommets pesés ; somme des poids = 1 ; ≤ 4 influences.
3. **Ergonomie** : les collections `ORG`, `MCH` et `DEF` sont **masquées** ; au moins 10 collections de contrôle restent visibles.
4. **Animation de test** : une Action sur `RIG_Hero` avec au moins 2 courbes, des images clés à au moins 2 images différentes (la première = repos), valeurs différentes entre la première et la dernière.
5. **Comportement** (mesuré sur le maillage évalué) : racine +0,5 m → le corps suit (moyenne 0,5 ± 0,03 m) ; à la dernière pose : le **pied gauche monte** de 0,10 à 0,35 m, le **pied droit reste** (≤ 1 cm), la **tête bouge** (≥ 8 mm en moyenne) ; à la première image : le pied gauche reste au sol (≤ 2 cm).
6. **Planche** non noire et contrastée.

## Vérification
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "PROJECTS\p6_rig\p6_rig_<prenom>_v001.blend" `
  --python-exit-code 1 --python "06_RIGGING\PROJECT_P6\validate_p6.py" -- --debug
```
Le correcteur est testé par `python 06_RIGGING/PROJECT_P6/test_p6.py` (référence acceptée ; neuf variantes fausses refusées).

## Référence
`REFERENCE/p6_character_reference.blend` (+ `renders/p6_posetest.png`) : produit par `build_p6_reference.py` à partir de la solution de CH06.05 (personnage du projet P3, rig Rigify de 706 bones, corps lié par Automatic Weights) :
Action « P6_PoseTest » (image 1 : repos ; image 24 : `foot_ik.L` levé de 0,25 m et `head` tourné de 30°), planche des images 1, 12 et 24 (EEVEE, caméra CAM_Front). Validée 63/63.
**Limites honnêtes** : (1) le méta-rig humain a les bras en T alors que le mannequin les a en A : les bras ne sont pas alignés (le correcteur teste la racine, les jambes et la tête) ;
(2) le visage Rigify est généré mais ni testé ni lié finement (pas de shape keys) ; (3) pas de contrôleurs sur mesure : les formes sont celles de Rigify ; (4) la tête du mannequin est un ovoïde : le tour de tête se mesure mais se voit à peine sur la planche.
Ne copiez pas la référence : liez votre propre personnage.

## Grille d'évaluation (sur 100)
| Critère | Points | Comment l'évaluer |
|---|---|---|
| Contraintes techniques (score du correcteur) | 30 | Score ramené sur 30 |
| Qualité du skinning (articulations propres sur trois poses extrêmes) | 20 | Planche et poses extrêmes (genoux, épaules, cou) |
| Contrôle (le rig se laisse poser vite, sans surprise) | 15 | Faire une pose en 5 minutes |
| Ergonomie (collections, noms, couleurs, verrous) | 10 | Capture du rig vu par l'animateur |
| Test de pose (poses variées, clés propres) | 10 | Action et planche |
| Robustesse (aucune pose ne casse le maillage ; origine, échelle, symétrie propres) | 10 | Poses extrêmes |
| Documentation (10 lignes, limites dites) | 5 | PORTFOLIO |
**Phase 6 validée si ≥ 70/100** et tous les quiz de la phase ≥ 80 %.

## Conseils de méthode
1. Ajustez le méta-rig AVANT de générer ; ne retouchez jamais le rig généré à la main sans le noter.
2. Liez le corps, puis testez trois poses extrêmes (jambe levée, bras en l'air, cou tourné) avant d'aller plus loin.
3. Corrigez les poids par zone, jamais globalement ; normalisez et limitez à 4 influences.
4. Masquez ORG, MCH et DEF dès la fin ; une scène que l'animateur lit en dix secondes est une bonne scène.
5. Gardez l'image 1 en pose de repos : c'est la base de comparaison de toutes les poses.
