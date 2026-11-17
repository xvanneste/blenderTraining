# CH00.03 — Exercices

## Exercice 1 — Facile : diagnostic chiffré ⏱ 10 min
Sur le starter, relevez : objets, faces viewport, faces estimées au rendu, maillages
distincts, RAM, VRAM. Écrivez une phrase : « la principale source de coût est… ».
**Réussi si :** chiffres cohérents avec `bcma_scene_cost.py` et diagnostic correct
(subdivision rendu 5 + données dupliquées).

## Exercice 2 — Moyen : l'effet de chaque levier ⏱ 20 min
Sur une copie du starter, appliquez les leviers **un par un** et notez après chacun
l’estimation de faces. Si vous rendez les variantes, utilisez le même périphérique, 50 % et 32 échantillons :
1. Données partagées seulement. 2. + Subdivision 1/2. 3. + Simplify.
Présentez un tableau et expliquez pourquoi le levier 1 ne change pas l'estimation de
faces. Après réouverture de chaque version, mesurez sa taille de fichier et distinguez cette mesure de la mémoire au rendu.

## Exercice 3 — Difficile : optimiser sans procédure ⏱ 15 min
Rendez `ch00_03_heavy_scene_starter.blend` conforme au budget : **< 2 000 000 faces
estimées au rendu**, **≤ 5 maillages distincts** pour les galets, **200 galets
conservés**, galets toujours **lisses**. Enregistrez `ch00_03_heavy_scene_<prenom>_v001.blend`.
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch00_03_heavy_scene_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch00_03.py" -- --exercise optimize --render
```
Barème (12 pts) : 200 galets 2 · maillages partagés 3 · budget de faces 3 · lisses 2 ·
qualité conservée 1 · rendu 1.

## Défis
- **Défi 1 :** trouvez la plus petite valeur de *Render Levels* qui reste visuellement
  identique au rendu de référence à 100 % (comparez deux rendus côte à côte dans l'Image
  Editor, *Slot* 1 et 2 : touche `J` pour alterner).
- **Défi 2 :** en ligne de commande, rendez le starter avec `-- --cycles-print-stats` et
  relevez la mémoire maximale utilisée. Comparez avec la solution.
- **Défi 3 :** dupliquez les galets jusqu'à 2 000 (en duplication liée). Que deviennent la
  taille du fichier, la RAM et le temps de rendu ? Et avec 2 000 copies **non** liées ?

## Mini-projet — Rapport d'optimisation ⏱ 30 min
Une page dans `PORTFOLIO/setup/optimisation_report.md` : avant/après (chiffres, captures),
leviers utilisés, temps gagné par image, projection sur un court-métrage de 2 minutes à
24 i/s (2 880 images).

| Critère | Points |
|---|---|
| Mesures avant/après exactes | 30 |
| Leviers expliqués et justifiés | 30 |
| Projection sur un court-métrage cohérente | 20 |
| Qualité visuelle préservée (rendus comparés) | 20 |

## Tests chronométrés
| Test | Cible |
|---|---|
| Relier les données de 200 objets (`Ctrl+L`) | 30 s |
| Copy to Selected d'un paramètre de modificateur | 20 s |
| Activer et régler Simplify | 20 s |
