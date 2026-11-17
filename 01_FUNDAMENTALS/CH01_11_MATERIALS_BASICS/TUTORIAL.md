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
4. `Tab` (Edit Mode), puis mode faces (`3`). Orbitez pour voir les deux pans et cliquez
   le premier. Ajoutez le second avec `Shift` et un clic. Vérifiez que seuls les deux pans
   sont sélectionnés avant de les affecter au matériau.
5. Emplacement `MAT_Roof` sélectionné dans la liste → **Assign**. `Tab`.
   ✅ Le toit est rouge.

## Tutoriel 3 — La porte
1. Encore **+**, **New**, `MAT_Door`, brun (≈ 0,35 ; 0,2 ; 0,1).
2. En mode Édition, cliquez la face rectangulaire sur la façade avant. Dans *Material
   Properties*, sélectionnez `MAT_Door` et choisissez **Assign**. Revenez en mode Objet
   avant de sélectionner la gouttière.

## Tutoriel 4 — Métal et lumière
1. `GEO_Gutter` → **New** → `MAT_Metal` : *Metallic* **1**, *Roughness* 0,3, Base Color gris clair.
   ✅ En Material Preview, la gouttière reflète l'environnement.
2. `GEO_Lantern` → **New** → `MAT_Lamp_Glow` : panneau *Emission* → *Color* jaune,
   *Strength* **8**.
3. `Z` → *Rendered* pour observer la surface émissive. Baissez un instant *Strength*
   à zéro et comparez la surface. Pour éclairer le mur avec un contrôle direct, placez
   une source *Point* près de la lanterne. Réglez-la séparément de l’émission.

## Tutoriel 5 — Vérifier
Enregistrez (Object Mode) `ch01_11_house_colors_<prenom>_v001.blend` puis :
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch01_11_house_colors_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch01_11.py" -- --exercise colors --render
```
[Image de référence des matériaux de la maison](COMPLETED_EXAMPLES/ch01_11_house_colors_reference.png)

## Contrôle de transfert

Après Assign pour le toit, sélectionnez une face de toiture puis une face de mur en mode Édition. Vérifiez l’emplacement attribué avant d’interpréter la couleur. Dans Material Preview, comparez deux valeurs de Roughness en gardant la lumière et Base Color fixes. **Réussite** Le toit et les murs conservent leurs attributions, et la différence visible concerne surtout la netteté du reflet.
