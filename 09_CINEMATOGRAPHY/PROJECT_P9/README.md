# Projet de phase P9 — « Cinq plans, cinq émotions »

**Phase :** 9 — Lighting et cinématographie · **Durée estimée :** 30 à 45 h · **Évalue :** C09.01 → C09.12

## Brief
Un même personnage, cinq plans, cinq émotions : **joie, tristesse, colère, calme, peur**. Pour chaque plan vous construisez une **scène** (lumière, couleur, cadrage) qui exprime l'émotion sans changer le sujet. Vous montrez le résultat par une **planche de contact** des cinq plans côte à côte. C'est un exercice de color script éclairé : l'intention d'abord, la mesure ensuite.

## Livrables
1. `PROJECTS/p9_emotions/p9_emotions_<prenom>_v0NN.blend` : cinq scènes `SH_JOY`, `SH_SADNESS`, `SH_ANGER`, `SH_CALM`, `SH_FEAR`, chacune avec sa caméra, son monde et ses lampes ; l'objet `Hero` (cylindre de 1,8 m, couleur d'objet rouge) est partagé par les cinq scènes.
2. `PROJECTS/p9_emotions/renders/p9_contact_sheet.png` : les cinq plans côte à côte, ≥ 1 600 px de large.
3. `PORTFOLIO/p9/` : la planche, un tableau (une ligne par plan : intention, lumière, couleur, cadrage) et 10 lignes sur ce que la mesure a corrigé.

## Contraintes techniques (vérifiées par `validate_p9.py`)
1. Cinq scènes nommées comme ci-dessus ; `Hero` dans chacune, immobile en (0, 6, 0,9) ; chaque scène a sa caméra.
2. Le correcteur rend chaque scène deux fois (160 × 90) : en **Cycles CPU** (32 échantillons, sans débruitage, gestion des couleurs de la scène) pour l'ambiance, et en **Workbench plat** (monde noir temporaire) pour le cadrage.
3. **JOY** : luminance moyenne ≥ 0,45 ; chaud (R/B ≥ 1,1) ; Hero sur un tiers vertical (33 % ou 67 % ± 8).
4. **SADNESS** : luminance moyenne de 0,02 à 0,15 ; froid (B/R ≥ 1,1) ; Hero sur un tiers (± 8).
5. **ANGER** : part de rouge R/(R+G+B) ≥ 0,5 ; écart p95 − p5 de la luminance ≥ 0,4 ; Hero ≥ 60 % de la hauteur de l'image et centré (50 % ± 10).
6. **CALM** : luminance moyenne de 0,25 à 0,5 ; écart p95 − p5 ≤ 0,4 ; B ≥ R ; Hero sur un tiers (± 8).
7. **FEAR** : luminance moyenne de 0,01 à 0,12 ; Hero ≤ 35 % de la hauteur de l'image et excentré (centre hors de 40–60 %).
8. **Ensemble** : luminance moyenne des cinq plans étalée d'au moins 0,3 ; tailles du Hero étalées d'au moins 0,3.
9. **Planche** (`renders/p9_contact_sheet.png` à côté du .blend) : ≥ 1 600 px de large, non noire, contrastée.

## Vérification
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "PROJECTS\p9_emotions\p9_emotions_<prenom>_v001.blend" `
  --python-exit-code 1 --python "09_CINEMATOGRAPHY\PROJECT_P9\validate_p9.py" -- --debug
```
Le correcteur est testé par `python 09_CINEMATOGRAPHY/PROJECT_P9/test_p9.py` : la référence est acceptée (68/68) ; dix variantes fausses sont refusées, chacune par le contrôle visé (monde trop clair, plan de joie froid ou centré, colère pâle, calme trop contrasté, peur trop proche, sujet déplacé, scène manquante, planche absente ou noire).

## Référence
`REFERENCE/p9_scene_reference.blend` (+ `renders/p9_contact_sheet.png`) produite par `build_p9_reference.py` en **assemblant** les chapitres : sol et sujet diffus, monde et lampes ponctuelles réglés par plan (CH09.01–06), cadrage par Shift X (CH09.07 : tiers à ± 0,167), échelle par focale et distance (CH09.08, CH09.10), couleur (CH09.11). Mesures de la référence (Y = luminance moyenne) :

| Plan | Y | Couleur | Hero (hauteur, centre) |
|---|---|---|---|
| JOY | 0,77 | chaud (R/B 1,26) | 53 %, 33 % |
| SADNESS | 0,11 | froid (R/B 0,49) | 53 %, 67 % |
| ANGER | 0,31 | part de rouge 0,57, écart 0,57 | 77 %, 50 % |
| CALM | 0,43 | bleuté (R/B 0,72), écart 0,14 | 53 %, 33 % |
| FEAR | 0,08 | quasi noir | 27 %, 25 % |

**Limites honnêtes** : sujet unique et décor réduit à un sol (aucune mise en scène : voir CH09.12) ; rendu de 160 × 90 à 32 échantillons, avec du bruit (le seuil d'ambiance a des marges de 0,03 à 0,07 sur la référence) ; la planche de la référence est rendue en 400 × 225 par plan ; dans le plan de tristesse le sujet est presque invisible (c'est le rendu de cadrage Workbench, pas l'image d'ambiance, qui le mesure) ; les plages d'émotion sont des conventions, pas des vérités ; le correcteur ne juge ni la narration, ni le rythme du montage.
Ne copiez pas la référence : changez le sujet, le décor ou la progression des plans.

## Grille d'évaluation (sur 100)
| Critère | Points | Comment l'évaluer |
|---|---|---|
| Contraintes techniques (score du correcteur) | 30 | Score ramené sur 30 |
| Lisibilité de l'émotion (planche sans légende) | 25 | Faire deviner l'émotion de chaque plan |
| Qualité de la lumière (direction, ratio, ombres) | 15 | Lecture des rendus |
| Cohérence couleur et cadrage (color script, tiers, échelle) | 15 | Planche |
| Variété des cinq plans (lumière, échelle, couleur) | 5 | Planche |
| Documentation (tableau, 10 lignes, limites dites) | 10 | PORTFOLIO |
**Phase 9 validée si ≥ 70/100** et tous les quiz de la phase ≥ 80 %.

## Conseils de méthode
1. Commencez par la planche au crayon : cinq vignettes, une intention par vignette, avant d'ouvrir Blender.
2. Réglez un plan à la fois, rendez-le petit (160 × 90) pour itérer vite, regardez-le avant de lancer le correcteur.
3. Commencez par la luminance (monde et lampes), puis la couleur, puis le cadrage.
4. Un plan trop sombre n'est pas forcément un plan triste : gardez de la lisibilité (Y ≥ 0,02).
5. Comparez les cinq plans côte à côte : s'ils se ressemblent, la planche ne raconte rien.
