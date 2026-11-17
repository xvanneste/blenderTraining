# Projet de phase P8 — « Une séquence d'action »

**Phase :** 8 — Physique et simulations · **Durée estimée :** 30 à 45 h · **Évalue :** C08.01 → C08.10

## Brief
Réalisez une **séquence de 10 secondes** où plusieurs simulations jouent ensemble : un **mur de briques** s'effondre sous un boulet (destruction), un **drapeau** épinglé claque dans le **vent**, et de la **poussière** soulevée par l'impact dérive dans le même vent. Vous montrez la séquence par une **planche de contact** de quatre images. La séquence servira de plan d'essai d'effets (phases 9, 10 et 11).

## Livrables
1. `PROJECTS/p8_action/p8_action_<prenom>_v0NN.blend` : la scène (Ground, Brick_i_k, Wreck_Ball, Flag, Dust, FORCE_Wind).
2. `PROJECTS/p8_action/renders/p8_contact_sheet.png` : quatre images de la séquence côte à côte, ≥ 1 600 px de large.
3. `PORTFOLIO/p8/` : la planche, vos réglages (une ligne par simulation), 10 lignes sur les instabilités rencontrées et leurs remèdes.

## Contraintes techniques (vérifiées par `validate_p8.py`)
1. **Durée** : de 216 à 300 images à 24 i/s, début à l'image 1.
2. **Destruction** : monde de corps rigides (au moins 20 sous-étapes) ; `Ground` Passive ; au moins 20 briques `Brick_*` Active ; `Wreck_Ball` Active de 20 kg ou plus ; au moins 30 contraintes Fixed entre deux briques, au moins 90 % cassables (seuil de 0,3 à 3).
3. **Tissu** : `Flag` avec un modificateur Cloth dont le groupe d'épinglage (Pin Group) existe et compte au moins 10 sommets.
4. **Particules** : `Dust` avec un système d'au moins 100 particules.
5. **Vent** : `FORCE_Wind` (Wind, force ≥ 20), axe Z local vers +X.
6. **Simulation** (images lues une à une) : de 8 à 30 liaisons cassées sur 38 ; aucune brique sous le sol ; le haut du drapeau immobile (≤ 5 mm) ; le bas poussé d'au moins 0,15 m vers +X ; à l'image 120, au moins 100 particules vivantes dont le x moyen est de 1,5 à 15 m.
7. **Planche** non noire et contrastée.

## Vérification
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "PROJECTS\p8_action\p8_action_<prenom>_v001.blend" `
  --python-exit-code 1 --python "08_SIMULATIONS\PROJECT_P8\validate_p8.py" -- --debug
```
Le correcteur est testé par `python 08_SIMULATIONS/PROJECT_P8/test_p8.py` (référence acceptée ; dix variantes fausses refusées, chacune par le contrôle visé).

## Référence
`REFERENCE/p8_scene_reference.blend` (+ `renders/p8_contact_sheet.png`) : produit par `build_p8_reference.py` en **assemblant** les réglages des chapitres : destruction CH08.07 (24 briques, 38 contraintes Fixed de seuil 1, boulet de 40 kg animé de 1 à 60 puis lâché, 30 sous-étapes), tissu CH08.03 (grille 16 × 16, bord haut épinglé), particules CH08.04 (150 particules, images 30–70), vent CH08.09 (force 100 vers +X). Poids de champ : tissu 1, poussière 0,01, monde de corps rigides 0 (le vent ne pousse pas le mur). Mesures de la référence : 14 liaisons cassées sur 38, bas du drapeau poussé de 0,31 m, poussière à l'image 120 : 150 particules à x moyen 4,0 m. Validée 67/67.
**Limites honnêtes** : planche rendue en Workbench (couleurs d'objet, poussière en petits cubes) : c'est un contrôle de la simulation, pas un rendu artistique ; le vent n'a pas de falloff ; les caches ne sont pas cuits (le correcteur rejoue les 240 images en quelques secondes) ; aucune interaction entre les simulations (les débris ne touchent pas le drapeau) ; le correcteur ne juge ni la mise en scène ni le rythme.
Ne copiez pas la référence : changez le mur, la hauteur du drapeau ou la direction du vent.

## Grille d'évaluation (sur 100)
| Critère | Points | Comment l'évaluer |
|---|---|---|
| Contraintes techniques (score du correcteur) | 30 | Score ramené sur 30 |
| Lisibilité de l'action (cause, effet, rythme) | 25 | Lecture de la séquence |
| Stabilité des simulations (pas d'explosion, pas de tremblement) | 15 | Lecture image par image |
| Maîtrise des forces (vent, poids de champ) | 10 | Réglages et mesures |
| Cache et reproductibilité (relecture identique, CH08.10) | 10 | Sauts d'images |
| Documentation (réglages, 10 lignes, limites dites) | 10 | PORTFOLIO |
**Phase 8 validée si ≥ 70/100** et tous les quiz de la phase ≥ 80 %.

## Conseils de méthode
1. Construisez simulation par simulation, chacune validée seule (CH08.01 à CH08.09) avant de les réunir.
2. Isolez les forces : un champ n'agit que sur les systèmes dont les Field Weights l'acceptent.
3. Un mur qui explose : ralentissez le boulet, montez les sous-étapes avant toute autre chose.
4. Lisez toujours depuis l'image 1 ; cuisez seulement quand les réglages sont arrêtés (enregistrez avant).
5. Gardez une copie de la scène avant chaque cuisson.
