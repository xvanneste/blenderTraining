# Fiche de révision — CH00.06 Organisation

```
00_admin 01_preprod 02_assets 03_shots/sqNNN/shNNNN/<tâche> 04_edit 05_sound 06_deliveries 99_archive
```
- Fichiers : `projet_sq010_sh0010_anim_v001.blend` · `projet_chr_nom_v001.blend`
- Objets `GEO_ CAM_ LGT_ EMP_ CRV_ RIG_ GP_ TXT_` · collections MAJUSCULES · `MAT_` · `.L/.R`

| Action | Raccourci / menu |
|---|---|
| Renommer l'actif | `F2` |
| Renommer en masse | `Ctrl+F2` (Edit → Batch Rename) |
| Chemins relatifs | File → External Data → Make Paths Relative |
| Fichiers manquants | File → External Data → Find Missing Files / Report Missing Files |
| Projet Blender 5.3 | File → Project → New / Open / Close · Project → Settings |
| Créer l'arborescence | `bcma_create_project.py --root … --name …` |
| Contrôler un fichier | `blender -b f.blend --python SCRIPTS/bcma_naming_check.py` |
