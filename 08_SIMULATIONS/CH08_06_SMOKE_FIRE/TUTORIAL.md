# CH08.06 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch08_06_smoke_starter.blend`. Sauvegardez sous `ch08_06_smoke_starter_<prenom>_v001.blend`.

## Tutoriel 1 — Le domaine (15 min)
FLAME_Domain : Physics > Fluid ; Type Domain ; Domain Type Gas ; Resolution Divisions 32 ; Cache : Type Modular, Frame Start 1, End 30.

## Tutoriel 2 — Le foyer (10 min)
FLAME_Source : Physics > Fluid ; Type Flow ; Flow Type Fire + Smoke ; Flow Behavior Inflow.

## Tutoriel 3 — Le matériau (20 min)
Domaine : nouveau matériau ; supprimez le Principled BSDF ; ajoutez Principled Volume relié à Material Output > Volume ; deux nœuds Attribute : « density » vers Density, « flame » vers Emission Strength.

## Tutoriel 4 — Cuire et lire (10 min)
Enregistrez la scène avec un dossier de cache propre à votre variante. Lancez *Bake Data*, puis comparez deux images du volume après le démarrage. Vérifiez visuellement la fumée et les zones émissives. Le correcteur vérifie le calcul du cache selon les critères de l’exercice.

## Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch08_06_smoke_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch08_06.py" -- --exercise smoke --debug
```

Remarque d'honnêteté : la solution est générée par script (modificateur `FLUID`, `domain_settings`, `flow_settings`, nœuds `ShaderNodeVolumePrincipled` et `ShaderNodeAttribute`) ; le correcteur cuit avec `bpy.ops.fluid.bake_data` et mesure la taille des fichiers `.vdb` (la grille n'est pas lue : pas de lecteur OpenVDB) ; le rendu du volume n'a pas été regardé (ce n'est pas testé) ; les noms de panneaux et la connexion exacte des attributs n'ont pas été relus dans l'interface 5.3. Courbe des tailles (numpy) regardée : croissance régulière avec foyer, constante sans.

## Variante de contrôle

Avant la cuisson finale, testez un dépôt faible puis plus dense et inspectez le mouvement près du foyer. Conservez le même cadre et une transformation d’affichage constante. **Preuve** Le rapport sépare changement de simulation et changement apparent dû au matériau ou à l’éclairage.
