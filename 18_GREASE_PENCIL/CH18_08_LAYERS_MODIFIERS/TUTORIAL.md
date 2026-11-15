# CH18.08 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch18_08_layers_starter.blend`, `Num 0`. Le dessin est fourni : un mur avec
une fenêtre (BG), des nuages mal placés (CLOUDS), des rayons de soleil partout (FX_LIGHT), la forme
des vitres (MASK_WINDOW), une ombre (SHADE) et un personnage (LINE). Ne redessinez rien.

## Tutoriel 1 — Modificateurs limités à un calque
1. Sélectionnez `GP_Practice` (Object Mode). Properties → **Modifiers** (icône clé).
2. **Add Modifier → Deform → Thickness** : *Thickness Factor* 2,5. Dépliez **Influence** →
   **Layer** : `LINE`. Seul le personnage s'épaissit.
3. **Add Modifier → Deform → Noise** : *Factor* 0,3 ; Influence → Layer : `LINE`.
4. **Add Modifier → Color → Tint** : couleur orange, *Factor* 0,2 ; Influence → Layer : `BG`.
5. **Add Modifier → Generate → Build** : *Length* 48 ; Influence → Layer : `LINE`.
   Lancez la lecture (`Espace`) : le personnage se dessine de l'image 1 à 48.
6. Testez l'icône écran/appareil photo de chaque modificateur pour comparer avant/après.

## Tutoriel 2 — Un masque de lumière
1. Properties → **Object Data** → Layers : cliquez **FX_LIGHT** (calque actif).
2. Sous-panneau **Masks** : cochez la case de l'en-tête, puis **+** → `MASK_WINDOW`.
   Les rayons n'apparaissent plus que dans la forme des vitres.
3. Calque **MASK_WINDOW** : **Opacity = 0**. N'utilisez pas l'œil : un masque caché n'agit plus.

## Tutoriel 3 — Ombre en Multiply
1. Calque **SHADE** : **Blend Mode → Multiply**, **Opacity** 0,6.
2. L'ombre fonce le sol au lieu de le recouvrir d'un gris opaque.

## Tutoriel 4 — Transformer un calque
1. Calque **CLOUDS** actif → sous-panneau **Transform** → **Translation X = 2**.
2. Les nuages entrent dans la fenêtre. L'objet et les traits n'ont pas bougé (vérifiez en Edit
   Mode : les points ont gardé leurs coordonnées).

## Tutoriel 5 — Un effet (facultatif)
Properties → onglet **Effects** → *Add Effect* → **Shadow** : *Offset* 8 / −8 px ; ombre portée
type papier découpé.

## Tutoriel 6 — Vérifier
Enregistrez `ch18_08_layers_<prenom>_v001.blend`, puis :
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch18_08_layers_<prenom>_v001.blend" `
  --python "SCRIPTS\validate_ch18_08.py" --python-exit-code 1 -- --exercise layers --render
```
Références : `COMPLETED_EXAMPLES/ch18_08_layers_reference.png` (image 60) et
`ch18_08_layers_build_frame20.png` (image 20 : le Build est en cours).
