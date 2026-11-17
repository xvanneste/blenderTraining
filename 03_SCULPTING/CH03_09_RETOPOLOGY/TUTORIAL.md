# CH03.09 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch03_09_retopo_starter.blend` : le visage sculpté de CH03.06 (`SCULPT_Bust`, ≈ 75 000 faces) avec ses yeux. Sauvegardez sous
`ch03_09_retopo_<prenom>_v001.blend`.

## Tutoriel 1 — Préparer (10 min)
En mode Objet, ajoutez une grille (*Add → Mesh → Grid*) devant le visage. Nommez-la `RETOPO_Face`. Réglez
25 × 30 subdivisions avec `F9` avant de poursuivre. Orientez le plan dans XZ, réglez sa largeur et sa hauteur autour
de 0,19 et 0,22 m et centrez-le en (0 ; −0,2 ; 0,36). Appliquez **Rotation & Scale** en mode Objet pour que le Y
local du plan corresponde au Y de la scène. Contrôlez le placement en profil et passez en vue de face (`Numpad 1`).
En mode Édition, activez l’overlay **Retopology** pour lire la grille devant le sculpt.

## Tutoriel 2 — Les anneaux des yeux et de la bouche (40 min)
Edit Mode, vue de face. Sélectionnez les faces centrales de chaque œil (≈ 3 × 3 cellules autour de (±0,032 ; 0,385)) puis *Inset Faces* (I) deux
fois (≈ 3,5 mm puis 3 mm) : deux anneaux concentriques. Pour la bouche : une rangée de ≈ 7 cellules autour de (0 ; 0,3085), même travail.
Supprimez les faces **du centre** (pas celles de l'anneau !) pour ouvrir les yeux et la bouche : *Delete > Faces*.

## Tutoriel 3 — Garder le visage (20 min)
Supprimez les faces qui sortent du visage (loin des tempes, du menton) : elles s'étireraient entre le plan de départ et le côté de la tête.
Seul le devant du visage reste.

## Tutoriel 4 — Coller au sculpt (20 min)
En mode Objet, ajoutez *Shrinkwrap*. Choisissez **Project**, activez l’axe **Y** et la direction **Positive**,
choisissez `SCULPT_Bust` comme cible et réglez *Offset* sur 0,002 m. En profil, vérifiez que la projection rejoint
la surface du visage. Repérez les sommets restés sur le plan, corrigez leur point de départ puis revérifiez de face,
de trois quarts et de profil. Appliquez le modificateur depuis son menu après inspection. La [leçon Poly Build](../../02_MODELING/CH02_09_RETOPOLOGY/TUTORIAL.md)
présente l’alternative manuelle.

[Manuel Blender 5.3 du modificateur Shrinkwrap](https://docs.blender.org/manual/en/5.3/modeling/modifiers/deform/shrinkwrap.html)

## Tutoriel 5 — Nettoyer (30 min)
Tout en quads : *Select > Select All by Trait > Faces by Sides* (≠ 4) ; supprimez ou refaites les triangles. Peu de pôles : vérifiez les sommets de
valence 3 et 5 autour des yeux ; *Mesh > Normals > Recalculate Outside*.

## Tutoriel 6 — Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch03_09_retopo_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch03_09.py" -- --exercise retopo --render
```
Ajoutez `--debug` pour les grandeurs brutes. Référence : `COMPLETED_EXAMPLES/ch03_09_retopo_reference.png` (retopo en fil de fer sur le sculpt).

Remarque d'honnêteté : les étapes 2 à 4 ont été exécutées **par script** (Inset Region, suppression, Shrinkwrap). Les outils interactifs (Poly Build, Snap) n'ont pas
pu être exécutés en arrière-plan ; le correcteur, lui, a été éprouvé (SOLUTIONS.md).

## Variante de contrôle

Utilisez une petite zone de test avant la retopologie complète. Comparez une région plane et une région qui devra se déformer. Ajustez la densité sans faire converger des pôles nombreux sur la pliure. **Preuve** Deux vues filaires et une note de circulation des boucles.
