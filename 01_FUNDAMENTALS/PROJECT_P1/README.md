# Projet de phase P1 — « Nature morte »

**Phase :** 1 — Fondamentaux absolus · **Durée estimée :** 6 à 10 h · **Évalue :** C01.01 → C01.14

## Brief
Réalisez une **nature morte** originale (un coin de bureau, une table de cuisine, un établi
d'artisan, un autel de magicien…) entièrement construite avec les outils de la phase 1 :
primitives, Edit Mode, modificateurs, matériaux simples, une caméra composée, un éclairage
trois points, et livrez **deux rendus** (EEVEE et Cycles).

## Contraintes techniques (vérifiées par `validate_p1.py`)
1. Fichier `PROJECTS/p1_nature_morte/p1_nature_morte_<prenom>_v0NN.blend` (nommage BCMA).
2. Collections : `SET`, `PROPS`, `LIGHTS`, `CAMERAS` (+ `HELPERS` hors rendu si besoin) ; aucun
   objet en vrac ; conventions de noms respectées (`bcma_naming_check.py` sans problème).
3. Au moins **8 objets** dans `PROPS`, dont au moins : 2 duplications liées, 1 objet avec
   **≥ 2 modificateurs**, 1 objet avec **≥ 2 matériaux** (affectation par faces).
4. Échelles appliquées (1, 1, 1) sur tous les maillages sans parent.
5. Une caméra active `CAM_…` avec une focale entre 35 et 100 mm, profondeur de champ activée.
6. Au moins 3 lumières (key/fill/rim) ; monde à intensité ≤ 0,5.
7. Rendus `renders/p1_cycles.png` et `renders/p1_eevee.png` (1920 × 1080) à côté du `.blend`.

## Vérification
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "PROJECTS\p1_nature_morte\p1_nature_morte_<prenom>_v001.blend" `
  --python "01_FUNDAMENTALS\PROJECT_P1\validate_p1.py" --python-exit-code 1
```

## Grille d'évaluation (sur 100)
| Critère | Points | Comment l'évaluer |
|---|---|---|
| Contraintes techniques (correcteur) | 30 | Score du correcteur ramené sur 30 |
| Composition (tiers, lisibilité, profondeur) | 15 | Le regard sait où aller en 2 secondes |
| Éclairage (formes lisibles, ratio maîtrisé, pas de zones brûlées) | 15 | Vue *False Color* |
| Matériaux crédibles (métal/non-métal, rugosités variées) | 15 | Au moins 4 matières distinctes |
| Qualité de modélisation (formes propres, biseaux, pas d'interpénétration) | 15 | Inspection rapprochée |
| Autonomie et vitesse (journal de temps, aucun tutoriel suivi pas à pas) | 10 | Journal dans PROGRESS.md |
**Phase 1 validée si ≥ 70/100** et tous les quiz de la phase ≥ 80 %.

## Livrables
- Le `.blend` final et ses versions intermédiaires (`v001`, `v002`…).
- Les deux rendus, plus une planche « avant/après » (premier jet vs final) dans `PORTFOLIO/p1/`.
- Un court texte (5–10 lignes) : intention, choix de focale et d'éclairage, difficultés.

## Conseils de méthode
1. **Références d'abord** (15 min) : 3 photos de natures mortes dont vous aimez la lumière.
2. **Blocking** en cubes et cylindres (30 min) : composition et cadrage avant tout détail.
3. Formes et modificateurs, puis matériaux, puis lumière, puis rendu : toujours du général au
   particulier.
4. `Ctrl+Alt+S` à chaque étape (versions), sauvegarde 3-2-1 en fin de séance.
