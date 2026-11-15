# CH02.02 — Tutoriels pas à pas : le tabouret

Ouvrez `STARTER_FILES/ch02_02_stool_starter.blend`. `GEO_Stool` est l'assise : 40 × 40 × 6 cm, à
42 cm du sol. Sélectionnez-la, `Tab`. Activez **Statistics**. Vue de face `Num 1` quand c'est utile.

## Tutoriel 1 — Découper l'assise (Loop Cut)
1. `Ctrl+R`, survolez une arête **horizontale** de face avant : la coupe prévue est verticale.
   Molette vers le haut : **2** coupes. Clic gauche, puis **clic droit** (coupes au tiers).
2. Les deux boucles sont sélectionnées : `S` `X` `2.25` `Entrée` → elles passent à ±15 cm.
3. Même chose dans l'autre direction (survolez une arête de la face latérale) avec `S` `Y` `2.25`.
4. Vue de dessous (`Ctrl+Num 7`) : la face du dessous est découpée en 3 × 3, carrés d'angle de 5 cm.

## Tutoriel 2 — Les pieds (Extrude en tronçons)
1. Mode face (`3`), vue de dessous. `Shift+clic` sur les **4 carrés d'angle**.
2. `E` `Z` `-0.2` `Entrée` ; `E` `Z` `-0.05` `Entrée` ; `E` `Z` `-0.17` `Entrée`.
   Les pieds touchent le sol (vérifiez en vue de face : bas à z = 0).

## Tutoriel 3 — Les traverses (Bridge)
1. Sur deux pieds voisins, sélectionnez les **2 faces du tronçon du milieu** qui se regardent
   (vue de face, mode X-ray `Alt+Z` pour atteindre la face arrière si besoin).
2. *Edge → Bridge Edge Loops* (ou clic droit → *Bridge Faces*). Une traverse relie les pieds.
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
  --python "SCRIPTS\validate_ch02_02.py" --python-exit-code 1 -- --exercise stool --render
```
