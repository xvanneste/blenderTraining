# CH02.02 — Tutoriels pas à pas : le tabouret

Ouvrez `STARTER_FILES/ch02_02_stool_starter.blend`. `GEO_Stool` est l'assise : 40 × 40 × 6 cm, à
42 cm du sol. Sélectionnez-la, entrez en mode Édition avec `Tab` et activez **Statistics**.
Utilisez la vue de face (`Numpad 1`) pour contrôler la hauteur.

## Tutoriel 1 — Découper l'assise (Loop Cut)
1. `Ctrl+R`, survolez une arête **horizontale** de face avant : la coupe prévue est verticale.
   Molette vers le haut : **2** coupes. Clic gauche, puis **clic droit** (coupes au tiers).
2. Les deux boucles sont sélectionnées : `S` `X` `2.25` `Entrée` → elles passent à ±15 cm.
3. Même chose dans l'autre direction (survolez une arête de la face latérale) avec `S` `Y` `2.25`.
4. Vue de dessous (`Ctrl+Numpad 7`) : la face du dessous est découpée en 3 × 3, carrés d'angle de 5 cm.

## Tutoriel 2 — Les pieds (Extrude en tronçons)
1. En mode face (`3`), placez-vous sous l’assise. Désactivez X-Ray et désélectionnez avec
   `Alt+A`. Sélectionnez le premier carré d’angle, puis ajoutez les trois autres avec `Shift`.
2. Avec l’orientation *Global*, pressez `E` puis `Échap` pour garder les nouvelles faces
   sélectionnées à leur position de départ. Déplacez-les avec `G`, `Z`, `-0.2`, `Entrée`.
   Refaites l’extrusion puis le déplacement pour `-0.05` et `-0.17`. Le tronçon de 5 cm
   fournit les faces de raccord des traverses. Contrôlez de face que le bas atteint le sol.

## Tutoriel 3 — Les traverses (Bridge)
1. Désélectionnez tout. Orbitez pour sélectionner la face intérieure du tronçon médian
   d’un pied. Orbitez vers le pied voisin et ajoutez avec `Shift` la face médiane qui lui
   fait face. Contrôlez que seules ces deux faces sont sélectionnées.
2. Lancez *Bridge Edge Loops* depuis la recherche `F3`. Blender remplace les deux faces
   par le raccord continu entre leurs contours.
3. Pont vrillé ? Panneau de l'opération → **Twist** : changez la valeur jusqu'à un pont droit.
4. Répétez sur les 4 côtés (au moins 2).

## Tutoriel 4 — Le chanfrein (Bevel)
1. Mode arête (`2`), `Alt+clic` sur une arête du pourtour supérieur de l'assise : toute la boucle.
2. `Ctrl+B`, glissez la souris, molette → **2 segments**, largeur ≈ 1 cm (panneau : *Width* 0.01).

## Tutoriel 5 — Le dessus creusé (Inset)
1. Mode face, sélectionnez les faces du dessus de l'assise.
2. `I`, environ 2 cm (*Thickness* 0.02). Puis `E` `-0.005` `Entrée` : un creux de 5 mm.

## Tutoriel 6 — Vérifier
`Tab` (Object Mode), rendu `F12`. Enregistrez `ch02_02_stool_<prenom>_v001.blend` puis :
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch02_02_stool_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch02_02.py" -- --exercise stool --render
```

## Variante de contrôle

Sur l’assise, testez une coupe avant et après une face à plus de quatre côtés sur une copie. Décrivez où le chemin s’arrête. Pour une traverse, sélectionnez les deux boucles ouvertes avant Bridge et comparez l’alignement des quatre coins. **Preuve** Deux jonctions continues avec le même nombre de sommets sur les bords prévus.

[Manuel Blender 5.3 de Bridge Edge Loops](https://docs.blender.org/manual/en/5.3/modeling/meshes/editing/edge/bridge_edge_loops.html)
