# CH10.04 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch10_04_passes_starter.blend`. Sauvegardez sous `ch10_04_passes_starter_<prenom>_v001.blend`.

## Tutoriel 1 — Les passes (10 min)
Properties > View Layer > Passes : Data : Z, Normal, Object Index ; Light > Diffuse > Color ; Cryptomatte > Object.

## Tutoriel 2 — Index, groupes, AOV (20 min)
Object Properties > Relations > Pass Index : Hero 1, Backdrop 2. View Layer > Light Groups : ajoutez key et fill ; Object Properties > Shading > Light Group sur KEY et FILL. View Layer > Shader AOV : ajoutez tint (Color) ; dans MA_Hero ajoutez un nœud AOV Output nommé tint.

## Tutoriel 3 — Deux calques (15 min)
Renommez le calque en FG, excluez la collection Backdrop ; ajoutez un calque BG (New) qui exclut Hero, avec la passe Z.

## Tutoriel 4 — Sortie et mesure (10 min)
Dans *Output Properties → Output*, choisissez **Multi-Layer EXR** comme type de média, puis 16 bits. Rendez une image et ouvrez cet EXR dans un nœud *Image* du Compositor. Vérifiez que FG et BG sont accessibles et que la profondeur existe pour BG. Lancez ensuite le correcteur pour contrôler les noms de canaux dans le fichier produit.

## Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch10_04_passes_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch10_04.py" -- --exercise passes --debug
```

Remarque d'honnêteté : les panneaux View Layer (Passes, Cryptomatte, Light Groups, Shader AOV), Object > Relations > Pass Index et Object > Shading > Light Group ont été relus dans `bl_ui` et `addons_core/cycles/ui.py` ; en 5.3 l'option de sortie multicouche est `image_settings.media_type = 'MULTI_LAYER_IMAGE'` (file_format passe alors à OPEN_EXR_MULTILAYER) : j'ai vérifié l'API et le fichier produit, mais je n'ai pas regardé le libellé de ce réglage dans l'interface ; la lecture des canaux utilise un analyseur d'en-tête EXR écrit pour l'occasion et validé sur les fichiers produits par Blender 5.3 (multi-parties) ; le contenu des pixels n'est pas vérifié ; le rendu de la planche est une illustration (les deux calques séparés).

## Variante de contrôle

Choisissez une passe de profondeur et une passe utile pour un ajustement local. Vérifiez leur branchement en ouvrant le fichier de rendu et leur effet dans le composite. **Preuve** La correction reste limitée à la zone et à l’information annoncées.
