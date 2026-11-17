# Projet de phase P3 — « Le personnage complet »

**Phase :** 3 — Sculpting (avec les UV et le bake de la phase 4) · **Durée estimée :** 20 à 35 h · **Évalue :** C03.01 → C03.10, C04.01, C04.07, C04.10

## Brief
Sculptez un **personnage complet** (stylisé ou réaliste, corps entier, pose en A), refaites-en la **topologie** pour l'animation,
dépliez-le, **bakez** le détail du sculpt dans une normal map et habillez-le d'un matériau de peau. Le résultat doit être
**prêt pour le rig** (phase 6) : échelle réelle, transformations appliquées, pieds au sol, origine entre les pieds.
Ce projet ne pouvait être évalué qu'après la phase 4 (UV, normal map) : il ferme donc les phases 3 et 4 ensemble.

## Livrables
1. `PROJECTS/p3_character/p3_character_<prenom>_v0NN.blend` contenant deux maillages :
   - `HIGH_<Nom>` : le sculpt (haute définition), caché au rendu ;
   - `CHR_<Nom>_Body` (données `ME_CHR_<Nom>_Body`) : la retopologie, avec UV, matériau `MAT_CHR_<Nom>` et normal map `T_<Nom>_N` empaquetée.
2. `PROJECTS/p3_character/renders/p3_turnaround.png` : planche de rotation (face, trois-quarts, profil, dos), ≥ 1600 px de large.
3. `PORTFOLIO/p3/` : une planche « sculpt / topologie fil de fer / rendu » et 10 lignes (références, difficultés, temps par étape).

## Contraintes techniques (vérifiées par `validate_p3.py`)
1. **Sculpt** : ≥ 20 000 faces, caché au rendu. **Retopo** : 2 000–10 000 faces, ≥ 90 % de quads, ≥ 5 fois moins de faces que le sculpt, maillage fermé.
2. **Adhérence** : la retopo colle au sculpt (distance moyenne des sommets ≤ 1,5 cm, 95ᵉ centile ≤ 4 cm).
3. **Rig-ready** : échelle 1 et rotation 0 appliquées ; taille 1,55–1,95 m ; pieds au sol ; origine en (0, 0, 0) ; nommage conforme (CH03.10).
4. **UV** : un calque, étirement moyen ≤ 1,35, aucun chevauchement (≥ 98 %), occupation ≥ 35 %, tout dans [0,1]².
5. **Bake** : `T_<Nom>_N` en Non-Color, empaquetée, branchée Image → Normal Map (Tangent) → Normal ; du relief sur ≥ 5 % des pixels des îlots ; normales valides.
6. **Peau** : Subsurface Weight ≥ 0,5, rayon R > V > B, Base Color de teinte chair (R > V > B).
7. **Planche** non noire et contrastée.

## Vérification
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "PROJECTS\p3_character\p3_character_<prenom>_v001.blend" `
  --python-exit-code 1 --python "03_SCULPTING\PROJECT_P3\validate_p3.py" -- --debug
```
Le correcteur est testé par `python 03_SCULPTING/PROJECT_P3/test_p3.py` (référence acceptée ; neuf variantes fausses refusées).

## Référence
`REFERENCE/p3_character_reference.blend` (+ `renders/p3_turnaround.png`), produite par `build_p3_reference.py` à partir du mannequin de CH03.10 :
Quadriflow (5 000 faces cibles, 4 681 obtenues, 100 % quads) → Smart UV Project + Average Islands Scale + Pack Islands → bake réel Cycles (Selected to Active, extrusion 3 cm) → peau de CH04.10. Validée 68/68.
**Limites honnêtes** : le « sculpt » de la référence est le mannequin lisse de CH03.10, pas un personnage détaillé : son bake ne porte que peu de relief (18 % des pixels) et
la retopologie automatique (Quadriflow) n'a pas la qualité d'une retopologie à la main (boucles autour des yeux, de la bouche et des articulations, CH03.09). Votre projet doit mieux faire :
tête avec visage, mains, plis, boucles de déformation. Le correcteur contrôle des mesures, pas la qualité artistique : jugez avec la grille ci-dessous.

## Grille d'évaluation (sur 100)
| Critère | Points | Comment l'évaluer |
|---|---|---|
| Contraintes techniques (score du correcteur) | 25 | Score ramené sur 25 |
| Anatomie, proportions, silhouette du sculpt | 20 | Vues face / profil / dos, ortho |
| Qualité du détail (plis, peau, formes secondaires) | 10 | Gros plans |
| Topologie de déformation (boucles aux articulations, yeux, bouche) | 15 | Fil de fer, test de pose |
| UV (coutures cachées, densité cohérente) | 10 | Damier |
| Bake et matériau (relief propre, pas de coutures visibles) | 10 | Rendu rapproché |
| Planche de rotation et présentation | 5 | Lisibilité |
| Organisation et documentation | 5 | Outliner, 10 lignes |
**Phase 3 validée si ≥ 70/100** et tous les quiz de la phase ≥ 80 %.

## Conseils de méthode
1. Références et blocking en silhouette avant tout détail ; pose en A pour le rig.
2. Sculptez symétrique, brisez la symétrie en dernier ; Voxel Remesh / Multires selon CH03.03.
3. Retopo : boucles d'abord (yeux, bouche, épaules, coudes, genoux), puis remplissage ; Shrinkwrap pour coller au sculpt.
4. Coutures UV dans les zones cachées ; vérifier avec un damier avant de baker.
5. Baker avec une extrusion suffisante et une marge ; regarder le rendu rapproché.
