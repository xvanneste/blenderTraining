# Fiche de révision — CH00.01 Installation et ligne de commande

## À retenir en 30 secondes
- Blender = libre (GPL), vos œuvres vous appartiennent ; les assets ont leur propre licence.
- Stable (3–4 mois) · LTS (2 ans de corrections) · Daily (tests seulement).
- On **gèle** la version d'un projet jusqu'à la livraison.
- Plusieurs versions cohabitent : un dossier de réglages par version
  (`%APPDATA%\Blender Foundation\Blender\<version>\`).
- Dossier `portable` à côté de `blender.exe` (zip) = configuration embarquée.
- GPU : activer dans *Preferences → System → Cycles Render Devices* **et** choisir
  *Render → Device → GPU Compute* dans la scène.

## Raccourcis et menus
| Action | Raccourci / menu |
|---|---|
| Ouvrir | `Ctrl+O` |
| Enregistrer | `Ctrl+S` |
| Enregistrer sous | `Shift+Ctrl+S` |
| Enregistrer en incrémentant (v001 → v002) | `Ctrl+Alt+S` (*File → Save Incremental*) |
| Rendre l'image | `F12` |
| Préférences | *Edit → Preferences* |
| Version | *Help → About Blender* · barre d'état `RMB` → *Blender Version* |
| Réglages d'usine (session) | *File → Defaults → Load Factory Settings* |
| Console système (Windows) | *Window → Toggle System Console* |

## Ligne de commande
```powershell
$B = "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe"
& $B --version                                         # version + build
& $B --factory-startup                                 # sans vos réglages
& $B -b scene.blend -o "//renders/img_####" -f 1       # une image, sans interface
& $B -b scene.blend -o "//renders/img_####" -a         # toute l'animation
& $B -b scene.blend -f 1 -- --cycles-device OPTIX      # choisir le périphérique Cycles
& $B -b --python script.py --python-exit-code 1        # script + code d'erreur
& $B -r                                                # associer les .blend
```
Ordre : **fichier → options de sortie (`-o`, `-E`) → rendu (`-f`/`-a`) → `--` → options Cycles**.

## Les 5 suspects du rendu noir
1. Clip Start/End caméra · 2. Visibilité au rendu (objets **et** collections) ·
3. Lumières et World · 4. Resolution % · 5. Caméra active / image / sortie.

## Révision espacée
- [ ] J+7 : tests chronométrés T1–T4 (EXERCISES.md)
- [ ] J+30 : refaire l'exercice 3 en < 5 min
- [ ] J+90 : régénérer rapport système + benchmark et comparer
