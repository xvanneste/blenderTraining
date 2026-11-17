# Projet de phase P7 — « Une scène animée »

**Phase :** 7 — Animation 3D · **Durée estimée :** 40 à 60 h · **Évalue :** C07.01 → C07.15

## Brief
Réalisez une **scène de 15 à 25 secondes** avec un personnage qui JOUE : un **jeu d'acteur** (une remarque rapide, un temps de pensée, une action), un **dialogue** (deux répliques synchronisées sur la réaction du personnage), du **mouvement** (marche, saut) et **deux caméras** avec une coupe. La scène est montée à partir d'actions réutilisables (éditeur NLA) et montrée par une **planche de contact** de quatre images. Elle servira de plan d'essai pour les courts-métrages (phases 9 et 15).

## Livrables
1. `PROJECTS/p7_scene/p7_scene_<prenom>_v0NN.blend` : le mannequin (ou votre personnage) `RIG_Mannequin` / `CHR_Mannequin` animé par NLA, deux caméras, le texte `DIALOGUE`, les marqueurs.
2. `PROJECTS/p7_scene/renders/p7_contact_sheet.png` : quatre images de la scène côte à côte, ≥ 1 600 px de large.
3. `PORTFOLIO/p7/` : les trois étapes du plan principal (blocking, splining, polish), la planche et 10 lignes (choix de jeu, difficultés, limites).

## Contraintes techniques (vérifiées par `validate_p7.py`)
1. **Durée** : de 360 à 600 images à 24 i/s (15 à 25 s).
2. **Personnage** : `RIG_Mannequin` (13 bones) et `CHR_Mannequin` lié par un modificateur Armature.
3. **Montage NLA** : **aucune action active** ; au moins 5 strips sur au moins 2 pistes ; au moins 3 actions différentes ; au moins un strip répété 3 fois ou plus (une marche) ; au moins 3 fondus d'entrée (Blend In ≥ 4 images) sur des strips qui chevauchent un autre strip.
4. **Jeu d'acteur** (lacet évalué de la tête) : une **remarque** (au moins 40° en 10 images ou moins) et un **maintien** (12 images consécutives ou plus à moins de 3° de variation, à plus de 30° de lacet).
5. **Continuité** : aucune cheville ni poignet ne se déplace de plus de 0,40 m d'une image à l'autre (pas de saut aux raccords).
6. **Caméras** : au moins 2 caméras **animées**, avec une **contrainte de visée** sur un objet ; au moins 2 **marqueurs liés** à une caméra, à des images différentes, le premier à l'image de début ; la caméra de la scène change au raccord.
7. **Dialogue** : texte `DIALOGUE` (lignes « image N : réplique »), au moins 2 répliques espacées d'au moins 36 images, marqueurs `line_1`, `line_2`… aux images indiquées ; à chaque réplique la tête varie d'au moins 25° dans les 14 images qui suivent.
8. **Planche** non noire et contrastée.

## Vérification
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "PROJECTS\p7_scene\p7_scene_<prenom>_v001.blend" `
  --python-exit-code 1 --python "07_ANIMATION\PROJECT_P7\validate_p7.py" -- --debug
```
Le correcteur est testé par `python 07_ANIMATION/PROJECT_P7/test_p7.py` (référence acceptée ; neuf variantes fausses refusées).

## Référence
`REFERENCE/p7_scene_reference.blend` (+ `renders/p7_contact_sheet.png`) : produit par `build_p7_reference.py` en **assemblant** les résultats des chapitres : le mannequin et l'action de jeu d'acteur de CH07.10 (72 images), la marche de CH07.08 et le saut de CH07.09, montés par NLA (CH07.13) : ACTING (1–73), WALK ×6 (67–211), JUMP (205–245), ACTING (239–311), WALK ×4 (305–401) = 401 images (16,7 s), cinq strips sur deux pistes alternées, fondu d'entrée de 6 images ; deux caméras (CH07.12) avec Track To et marqueurs liés (coupe à l'image 201) ; deux répliques aux images 14 et 253, alignées sur la remarque du personnage. Validée 49/49.
**Limites honnêtes** : le mannequin marche SUR PLACE et reste au même endroit ; il n'y a ni lip sync (le dialogue est porté par les marqueurs et la réaction de la tête), ni décor, ni son ; le jeu est celui, schématique, du chapitre CH07.10 ; la planche est un contrôle de la scène, pas un rendu artistique ; le correcteur ne juge ni l'intention ni la qualité du jeu.
Ne copiez pas la référence : animez votre propre plan.

## Grille d'évaluation (sur 100)
| Critère | Points | Comment l'évaluer |
|---|---|---|
| Contraintes techniques (score du correcteur) | 30 | Score ramené sur 30 |
| Qualité du jeu (intention lisible, timing, maintiens) | 25 | Lecture de la scène sans le son |
| Mouvement (marche, saut, raccords propres) | 15 | Lecture en boucle des raccords |
| Caméras (mouvement motivé, coupe) | 10 | Les deux plans |
| Dialogue (alignement jeu et répliques) | 10 | Marqueurs et réaction |
| Processus (blocking, splining, polish documentés) | 5 | PORTFOLIO |
| Documentation (10 lignes, limites dites) | 5 | PORTFOLIO |
**Phase 7 validée si ≥ 70/100** et tous les quiz de la phase ≥ 80 %.

## Conseils de méthode
1. Écrivez la scène en une phrase puis en poses clés (blocking) avant de lisser quoi que ce soit.
2. Gardez vos actions séparées (jeu, marche, saut) et assemblez-les par NLA : ce qui est réutilisable se corrige une seule fois.
3. Sur chaque raccord de strips, un fondu d'entrée de 6 images ; mesurez les pops avant de rendre.
4. Une réplique se joue par la réaction du corps : tête, buste, puis le reste.
5. Gardez une copie du blocking : on y revient quand le polish dérive.
