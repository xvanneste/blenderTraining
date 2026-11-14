# Conventions de l'académie (et de production)

Ces conventions sont celles que vous appliquerez **dans vos propres projets**. Elles
sont volontairement proches de celles d'un studio.

## 1. Nommage des fichiers
```
<projet>_<sequence>_<plan>_<tache>_v<NNN>.<ext>
bcma_sq010_sh0040_anim_v003.blend
```
- minuscules, pas d'espaces ni d'accents, séparateur `_` ;
- versions sur **3 chiffres** (`v001`) pour que le tri alphabétique soit chronologique ;
- ne jamais écraser une version publiée : on incrémente (`Ctrl+Alt+S` dans Blender
  incrémente le numéro final du nom de fichier).

Fichiers d'exercice de l'académie :
```
chNN_MM_<sujet>_starter.blend      fichier de départ
chNN_MM_<sujet>_solution.blend     version corrigée
chNN_MM_<sujet>_<prenom>_v001.blend  votre travail
```

## 2. Nommage dans Blender
| Élément | Convention | Exemple |
|---|---|---|
| Objet | `TYPE_Nom` en PascalCase | `GEO_Table`, `CAM_Main`, `LGT_Key` |
| Collection | MAJUSCULES | `SET`, `PROPS`, `CHARACTERS`, `LIGHTS`, `CAMERAS` |
| Matériau | `MAT_Nom` | `MAT_WoodOak` |
| Côtés | suffixe `.L` / `.R` | `hand.L` |
| Bones de contrôle / déformation | préfixes `CTRL_`, `DEF_`, `MCH_` | `CTRL_foot.L` |

Préfixes de type : `GEO` mesh · `CRV` courbe · `CAM` caméra · `LGT` lumière ·
`EMP` empty · `RIG` armature · `GN` objet Geometry Nodes · `FX` simulation.

## 3. Unités et échelle
- Système métrique, **1 unité Blender = 1 mètre**.
- Modéliser à l'échelle réelle (une porte ≈ 2,1 m) : la physique, l'éclairage (watts,
  atténuation) et la profondeur de champ en dépendent.
- Appliquer l'échelle (`Ctrl+A → Scale`) avant rigging, simulation et export.

## 4. Chemins
- Toujours en **chemins relatifs** (`//textures/…`), jamais `C:\Users\…`.
- Textures dans `ASSETS/TEXTURES/` ou dans un dossier `textures/` à côté du `.blend`.

## 5. Scripts
- Python 3 (version embarquée par Blender — 3.13 pour Blender 5.3).
- Un script = un en-tête docstring (but, usage en ligne de commande, version Blender testée).
- Testé en mode arrière-plan : `blender -b --factory-startup --python script.py`.
- Code de retour non nul en cas d'échec (`--python-exit-code 1`).

## 6. Langue
- Cours en français. Termes d'interface Blender en **anglais** (l'interface de référence
  de l'académie est en anglais, comme dans la majorité des studios et de la documentation),
  avec traduction à la première occurrence : *Outliner (l'arborescence de la scène)*.

## 7. Raccourcis
Notation : `Ctrl+Alt+S`, `Shift+A`, `Num 1` (pavé numérique), `MMB` (bouton du milieu),
`LMB`/`RMB` (gauche/droit). Keymap de référence : **Blender par défaut**, sélection au
clic gauche.
