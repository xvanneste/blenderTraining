# CH00.07 — Ressources

| Ressource | URL |
|---|---|
| Manuel — Opening & Saving (Recover, Auto Save, Save Versions) | https://docs.blender.org/manual/en/latest/files/blend/open_save.html |
| Manuel — Import/Export (formats) | https://docs.blender.org/manual/en/latest/files/import_export.html |
| USD (OpenUSD) | https://openusd.org/ |
| Alembic | https://www.alembic.io/ |
| glTF (Khronos) | https://www.khronos.org/gltf/ |
| OpenEXR | https://openexr.com/ |
| Git LFS | https://git-lfs.com/ |

Vérifications 5.3.0 : raccourci `Ctrl+Alt+S` → `wm.save_mainfile(incremental=True)`
(keymap `blender_default.py`) ; menu *File → Recover* ; génération réelle d'un `.blend1`
par `save_version = 1` et contrôle de son contenu (GEO_Hero présent).
Script `bcma_backup.py` testé (rotation, exclusions, vérification CRC).
