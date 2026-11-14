# CH01.11 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch01_11_house_colors_starter.blend`. Passez la vue en **Material
Preview** (`Z` → *Material Preview*).

## Tutoriel 1 — Modifier un matériau existant
1. Cliquez `GEO_House` → *Properties → Material* (sphère rouge-rose).
2. L'emplacement unique contient `MAT_Wall`. Panneau *Surface* → **Base Color** → cliquez
   la pastille → réglez un blanc cassé (V ≈ 0,85, légère teinte jaune).
   ✅ Toute la maison s'éclaircit.

## Tutoriel 2 — Un second matériau pour le toit
1. Dans la liste des emplacements, **+** → un emplacement vide apparaît.
2. **New** → un matériau `Material` est créé : double-cliquez son nom → `MAT_Roof`.
3. *Base Color* rouge tuile (≈ 0,6 ; 0,12 ; 0,06), *Roughness* 0,75.
4. `Tab` (Edit Mode), mode faces (`3`), cliquez un pan du toit, `Shift`+clic sur l'autre.
5. Emplacement `MAT_Roof` sélectionné dans la liste → **Assign**. `Tab`.
   ✅ Le toit est rouge.

## Tutoriel 3 — La porte
1. Encore **+**, **New**, `MAT_Door`, brun (≈ 0,35 ; 0,2 ; 0,1).
2. Edit Mode : cliquez la face de porte (rectangle sur la façade avant) → **Assign**.

## Tutoriel 4 — Métal et lumière
1. `GEO_Gutter` → **New** → `MAT_Metal` : *Metallic* **1**, *Roughness* 0,3, Base Color gris clair.
   ✅ En Material Preview, la gouttière reflète l'environnement.
2. `GEO_Lantern` → **New** → `MAT_Lamp_Glow` : panneau *Emission* → *Color* jaune,
   *Strength* **8**.
3. `Z` → *Rendered* (EEVEE) : la lanterne brille.

## Tutoriel 5 — Vérifier
Enregistrez (Object Mode) `ch01_11_house_colors_<prenom>_v001.blend` puis :
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch01_11_house_colors_<prenom>_v001.blend" `
  --python "SCRIPTS\validate_ch01_11.py" --python-exit-code 1 -- --exercise colors --render
```
Référence : `COMPLETED_EXAMPLES/ch01_11_house_colors_reference.png`.
