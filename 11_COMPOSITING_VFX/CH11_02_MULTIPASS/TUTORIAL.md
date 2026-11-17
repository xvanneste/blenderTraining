# CH11.02 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch11_02_multipass_starter.blend`. Sauvegardez sous `ch11_02_multipass_starter_<prenom>_v001.blend`.

## Tutoriel 1 — Voir (5 min)
Compositing : Render Layers a les prises Combined_key et Combined_fill.

## Tutoriel 2 — Doser (15 min)
Un nœud Exposure par groupe : +1 sur key, −1 sur fill.

## Tutoriel 3 — Additionner (10 min)
Reliez les deux images issues des nœuds *Exposure* à *A* et *B* d’un nœud *Mix* de type couleur. Sélectionnez **Add** et un facteur de 1. Reliez le résultat à *Group Output*. Gardez le même réglage de vue en comparant le dosage avant et après.

## Tutoriel 4 — Mesurer (10 min)
Lancez le correcteur : rapport, FILL, structure.

## Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch11_02_multipass_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch11_02.py" -- --exercise multipass --debug
```

Remarque d'honnêteté : les prises Combined_key et Combined_fill, le nœud Mix du compositeur (ShaderNodeMix en mode RGBA/ADD) et l'absence de CompositorNodeMixRGB ont été vérifiés par exécution en 5.3 ; les menus pour créer ces nœuds (Add > ...) n'ont pas été regardés dans l'interface ; la mesure est en luminance linéaire (conversion sRGB → linéaire) sur deux flancs d'une sphère ; Diffuse/Glossy séparés (passes de lumière) et le relighting d'ombres ne sont pas évalués ; les lampes sont ponctuelles et sans lumière indirecte importante (monde noir).

## Variante de contrôle

Isolez une seule contribution avant de recréer une combinaison. Comparez le résultat à Combined et inspectez une zone claire et une zone en creux. **Preuve** L’écart est expliqué par la passe et le traitement choisis, avec les limites du calcul indiquées.
