# CH08.05 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch08_05_fluid_starter.blend`. Sauvegardez sous `ch08_05_fluid_starter_<prenom>_v001.blend`.

## Tutoriel 1 — Le domaine (15 min)
FLUID_Domain : Physics > Fluid ; Type Domain ; Domain Type Liquid ; Resolution Divisions 32 ; Cache : Type Modular, Frame Start 1, End 20 ; Mesh coché.

## Tutoriel 2 — La source (10 min)
FLUID_Source : Physics > Fluid ; Type Flow ; Flow Type Liquid ; Flow Behavior Geometry.

## Tutoriel 3 — Cuire (10 min)
Enregistrez d’abord votre copie et choisissez un dossier de cache dédié. Sur le domaine liquide, calculez *Bake Data* avant *Bake Mesh*. Si vous reprenez la résolution ou la source, repartez d’un cache neuf pour recalculer les deux étapes.

## Tutoriel 4 — Lire (10 min)
Lecture depuis l'image 1 : le cube tombe et s'étale ; lancez le correcteur (il cuit tout seul).

## Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch08_05_fluid_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch08_05.py" -- --exercise fluid --debug
```

Remarque d'honnêteté : la solution est générée par script (modificateur `FLUID`, `domain_settings`, `flow_settings`) ; le correcteur cuit en arrière-plan avec `bpy.ops.fluid.bake_data` puis `bake_mesh` (moins d'une seconde) et lit les fichiers `.bobj.gz` (format : entier du nombre de sommets puis flottants xyz, déduit de la lecture et vérifié sur les bornes obtenues) ; les noms des panneaux (Fluid, Cache, Bake Data, Bake Mesh) n'ont pas été relus dans l'interface 5.3. Un contre-exemple « sans gravité » n'a pas pu être fabriqué. Le profil (numpy) a été regardé : la boîte englobante du liquide descend puis s'étale.

## Variante de contrôle

Créez un premier essai à résolution modeste sur une courte plage. Localisez la première apparition de liquide et le contact avec l’obstacle. Comparez deux définitions du domaine à géométrie identique. **Preuve** Les dates, résolution et dossier de cache permettent de reconnaître quel calcul est relu.
