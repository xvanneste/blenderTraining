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
4. `A`, **`U` → Unwrap** (*Angle Based*). Trois îles : un rectangle, deux disques.
5. UV Editor : *UV → Pack Islands*, *Margin* 0.02.

## Tutoriel 3 — Lire le damier
1. Orbitez : carrés réguliers partout ? La couture verticale se voit-elle ? Placez-la à l'arrière
   (côté opposé à la caméra) si besoin : *Clear Seam*, nouvelle arête, re-Unwrap.
2. Comparez la taille des carrés entre la caisse et la boîte (densité de texels, THEORY §5).

## Tutoriel 4 — Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch02_11_uv_<prenom>_v001.blend" `
  --python "SCRIPTS\validate_ch02_11.py" --python-exit-code 1 -- --exercise uv --render
```
