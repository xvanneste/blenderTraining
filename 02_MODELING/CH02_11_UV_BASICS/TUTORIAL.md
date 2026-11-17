# CH02.11 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch02_11_uv_starter.blend`. Workspace **UV Editing** (onglet en haut) : à
gauche l'UV Editor, à droite le 3D Viewport. Passez le viewport en Material Preview (`Z`).

## Tutoriel 1 — La caisse : Smart UV Project
1. Sélectionnez `GEO_Crate`, `Tab`, `A`.
2. **`U` → Smart UV Project** : *Angle Limit* 66°, *Island Margin* 0.02. Dans l'UV Editor, les
   6 faces apparaissent rangées ; dans le viewport, le damier est régulier.

## Tutoriel 2 — La boîte : coutures et Unwrap
1. Sélectionnez `GEO_Can`, `Tab`, mode arête (`2`).
2. `Alt+clic` sur le cercle du couvercle supérieur, `Shift+Alt+clic` sur le cercle inférieur,
   `Shift+clic` sur **une** arête verticale.
3. *Edge → Mark Seam* (ou `U` → *Mark Seam*) : les arêtes deviennent rouges.
4. Gardez le pointeur dans la vue 3D. Pressez `A`, puis `U` → **Unwrap Angle Based**.
   L’UV Editor doit montrer trois îles distinctes, un rectangle et deux disques.
5. Placez le pointeur dans l’UV Editor, sélectionnez les îles avec `A`, puis lancez
   *UV → Pack Islands*. Réglez *Margin* sur 0,02 et vérifiez l’espace entre les îles.

## Tutoriel 3 — Lire le damier
1. Orbitez pour vérifier que les carrés restent réguliers. Pour déplacer la couture,
   sélectionnez uniquement l’ancienne arête, lancez *Clear Seam*, puis marquez la
   nouvelle arête. Relancez le dépliage avec toutes les faces sélectionnées.
2. Comparez la taille des carrés entre la caisse et la boîte (densité de texels, THEORY §5).

## Tutoriel 4 — Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch02_11_uv_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch02_11.py" -- --exercise uv --render
```

## Variante de contrôle

Mettez un damier commun sur les deux variantes de caisse. Inscrivez une couture que vous placez sur une arête peu visible et comparez l’étirement sur le dessus et sur les côtés. **Preuve** Aucune variation d’échelle inexpliquée entre les faces comparées, aucune superposition involontaire et couture choisie pour une raison visible.
