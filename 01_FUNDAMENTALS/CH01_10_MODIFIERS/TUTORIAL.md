# CH01.10 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch01_10_bridge_starter.blend`.

## Tutoriel 1 — Array : le tablier
1. Cliquez `GEO_Plank`. *Properties → Modifiers* → **Add Modifier → Generate → Array**.
2. *Count* = `10`. *Relative Offset* → *Factor X* = `1.05` (5 % d'espace entre planches).
   ✅ 10 planches alignées. Le maillage ne contient toujours qu'une planche (*Statistics* en
   Edit Mode : 8 sommets).
3. Essayez *Fit Type* → *Fit Length* = 3 m, observez, revenez à *Fixed Count*.

## Tutoriel 2 — Mirror : la rambarde
1. `GEO_Railing` → **Add Modifier → Generate → Mirror** → axe **X** coché (défaut).
   ✅ La rambarde s'étend de −2,5 à +2,5 m. La symétrie se fait par rapport à l'**origine**
   de l'objet (CH01.07).
2. `Tab` sur la rambarde, déplacez un sommet : son reflet bouge aussi. `Ctrl+Z`.

## Tutoriel 3 — Bevel : le pilier
1. `GEO_Pillar` → **Add Modifier → Generate → Bevel** → *Amount* `0.02`, *Segments* `3`.
2. Vue rapprochée en *Material Preview* (`Z` → 2) : un liseré de lumière apparaît sur les arêtes.

## Tutoriel 4 — Solidify puis Subdivision : le seau
1. `GEO_Bucket` → **Add Modifier → Generate → Solidify** → *Thickness* `0.02`.
2. **Add Modifier → Generate → Subdivision Surface** → *Levels Viewport* `1`, *Render* `2`.
3. `RMB` dans la vue → **Shade Smooth** (*Object → Shade Smooth*).
4. Inversez l'ordre (menu ˅ de Subdivision → *Move to First*) : comparez le bord du seau.
   Remettez Solidify en premier.
   ✅ Pile : Solidify (haut) puis Subdivision (bas).

## Tutoriel 5 — Vérifier
Enregistrez `ch01_10_bridge_<prenom>_v001.blend`, puis :
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch01_10_bridge_<prenom>_v001.blend" `
  --python "SCRIPTS\validate_ch01_10.py" --python-exit-code 1 -- --exercise bridge --render
```
Rendu de référence : `COMPLETED_EXAMPLES/ch01_10_bridge_reference.png`.
