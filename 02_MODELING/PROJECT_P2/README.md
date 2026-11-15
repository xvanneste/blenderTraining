# Projet de phase P2 — « L'atelier »

**Phase :** 2 — Modélisation professionnelle · **Durée estimée :** 12 à 20 h · **Évalue :** C02.01 → C02.13

## Brief
Modélisez un **décor intérieur détaillé** (atelier d'artisan, cuisine, chambre d'enfant, bureau
d'inventeur…) et une **bibliothèque de 10 props** publiés comme assets, puis **liez** ces props dans
le décor. Tout est en dimensions réelles, topologie propre, UV dépliées : ce décor resservira aux
phases 4 (matériaux), 9 (lumière) et 15 (court-métrage).

## Deux fichiers
1. `PROJECTS/p2_atelier/p2_library.blend` (+ `blender_assets.cats.txt`) : **10 props** marqués
   comme assets, catalogues, métadonnées complètes (CH02.13). Validez-le avec le correcteur de
   CH02.13 : `--exercise library`.
2. `PROJECTS/p2_atelier/p2_atelier_<prenom>_v0NN.blend` : le décor, qui **lie** les props.

## Contraintes techniques du décor (vérifiées par `validate_p2.py`)
1. Collections `SET`, `PROPS`, `LIGHTS`, `CAMERAS` ; aucun objet en vrac ; noms conformes.
2. Une pièce (`SET`) : sol, au moins deux murs, une ouverture (porte ou fenêtre, booléen ou
   modélisée), dimensions réalistes (hauteur sous plafond 2,4 à 3,5 m).
3. **Au moins 10 props** dans `PROPS`, dont **au moins 5 liés** depuis `p2_library.blend` (Link).
4. Techniques de la phase visibles : au moins un objet avec **Bevel** (ou Weighted Normal), un objet
   avec **Subdivision Surface**, un objet avec un **Boolean**.
5. Échelles appliquées ; **UV présentes** sur au moins 80 % des maillages locaux ; aucun maillage
   local avec arêtes non-manifold (sauf plans volontaires : sol, murs simples).
6. Une caméra active `CAM_…` (24–85 mm) ; au moins 2 lumières.
7. Rendu `renders/p2_atelier.png` (1920 × 1080) à côté du `.blend`.

## Vérification
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "PROJECTS\p2_atelier\p2_atelier_<prenom>_v001.blend" `
  --python "02_MODELING\PROJECT_P2\validate_p2.py" --python-exit-code 1
```

## Grille d'évaluation (sur 100)
| Critère | Points | Comment l'évaluer |
|---|---|---|
| Contraintes techniques (correcteur du décor + correcteur de la bibliothèque) | 30 | Scores ramenés sur 30 |
| Topologie (quads, pôles, boucles, aucune erreur) | 15 | Inspection fil de fer, Statistics |
| Hard surface (arêtes qui accrochent la lumière) | 10 | Gros plans |
| Formes organiques / subdivision maîtrisées | 10 | Aucune bosse, boucles de maintien |
| UV (damier régulier, densité cohérente) | 10 | Matériau damier temporaire |
| Optimisation (pas de géométrie inutile, LOD pour le fond si besoin) | 10 | Statistics, triangles |
| Composition du plan (CH18.05) et lisibilité | 10 | Vignette en 3 valeurs |
| Organisation (assets liés, collections, nommage, versions) | 5 | Outliner |
**Phase 2 validée si ≥ 70/100** et tous les quiz de la phase ≥ 80 %.

## Livrables
- Les deux `.blend` et leurs versions, le fichier de catalogues, le rendu.
- Une planche « fil de fer + rendu » de 4 props dans `PORTFOLIO/p2/`.
- 10 lignes : choix de topologie, difficultés, temps passé par étape.

## Conseils de méthode
1. Références (photos de lieux réels) et plan au sol coté avant de modéliser.
2. Blocking de la pièce et des grands meubles (1 h), cadrage de la caméra.
3. Props : un par séance, chacun validé par votre checklist (CH02.01) puis publié.
4. Liez les props dans le décor au fur et à mesure ; corrigez toujours dans la bibliothèque.
