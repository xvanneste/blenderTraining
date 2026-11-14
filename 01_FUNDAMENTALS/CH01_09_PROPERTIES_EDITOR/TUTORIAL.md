# CH01.09 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch01_09_hunt_starter.blend`. Les consignes sont dans le Text Editor
(`README_EXERCICE`). Chaque tutoriel correspond à une consigne.

## Tutoriel 1 — Render et Output (consignes 1–2)
1. Onglet **Render** (dos d'appareil photo) : *Render Engine* → **EEVEE**.
2. Panneau *Sampling* → sous-panneau *Render* → **Samples** = `32`.
3. Onglet **Output** (imprimante) : *Format* → *Resolution X* `1280`, *Y* `720`, `%` = `100` ;
   *Frame Rate* → **25** ; *Frame Range* → *Start* `1`, *End* `120`.

## Tutoriel 2 — Scene et World (consignes 3–4)
1. Onglet **Scene** (cône et sphère) : *Camera* → **CAM_Shot** ; *Units* → *Length* → **Centimeters**.
2. Onglet **World** (globe rouge) : *Surface* → *Color* → cliquez la pastille, réglez un
   bleu nuit (en mode *RGB* : 0,02 / 0,03 / 0,08), *Strength* = 1.

## Tutoriel 3 — Object (consignes 5–6)
1. Cliquez `GEO_Guide`. Onglet **Object** (carré orange) : *Viewport Display* → *Display As*
   → **Wire** ; *Visibility* → décochez **Renders**.
2. Cliquez `GEO_Hero` : *Viewport Display* → cochez **Name**.

## Tutoriel 4 — Data (consignes 7–8)
1. Cliquez `CAM_Shot`. Onglet **Data** (caméra verte) : *Lens* → *Focal Length* = `35`.
2. Cliquez `LGT_Key`. Onglet **Data** (ampoule verte) : *Power* = `250` ; *Color* → orangé clair.

## Tutoriel 5 — Material et propriétés personnalisées (consignes 9–11)
1. `GEO_Hero` → onglet **Material** (sphère rouge) → *Surface* → *Base Color* → rouge.
2. Cliquez dans le vide pour garder la scène ; onglet **Scene** → *Custom Properties* →
   **New** → ⚙ : *Type* = **String**, *Property Name* = `shot`, *Default Value*/*Value* =
   `sq010_sh0010` → *OK*.
3. `GEO_Guide` → onglet **Material** : dans la ligne du datablock `MAT_Library_Gold`,
   cliquez le **bouclier** (Fake User). Puis, dans la liste des emplacements, cliquez **−**
   pour retirer l'emplacement.
   ✅ Outliner (*Blender File* → *Materials*) : `MAT_Library_Gold` affiche **F** / un bouclier.

## Tutoriel 6 — Vérifier
Enregistrez `ch01_09_hunt_<prenom>_v001.blend` puis :
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch01_09_hunt_<prenom>_v001.blend" `
  --python "SCRIPTS\validate_ch01_09.py" --python-exit-code 1 -- --exercise hunt
```
✅ 13/13.
