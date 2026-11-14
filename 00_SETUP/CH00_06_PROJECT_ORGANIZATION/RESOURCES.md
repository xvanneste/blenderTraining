# CH00.06 — Ressources

| Ressource | URL |
|---|---|
| Notes de version 5.3 (projets) | https://developer.blender.org/docs/release_notes/5.3/ |
| Manuel — External Data (chemins, pack, fichiers manquants) | https://docs.blender.org/manual/en/latest/files/blend/packed_data.html |
| Manuel — Batch Rename | https://docs.blender.org/manual/en/latest/files/blend/rename.html |
| Manuel — Asset Libraries | https://docs.blender.org/manual/en/latest/editors/preferences/file_paths.html |
| Blender Studio — organisation de production (pipeline des Open Movies) | https://studio.blender.org/ |

Vérifications 5.3.0 : opérateurs `project.new/open/close/config_save/variable_add/asset_library_add`,
type `BlenderProject` (name, root_path, variables, asset_libraries, ocio_config, splash_image_path),
format disque `.blender_project/project.toml` observé en créant un projet de test ; préférences
`use_project_remember` (Remember Last Project) et `use_project_auto_save` (Auto-save Project).
Le menu *File → Project* (New / Open / Close / projets récents) et le menu *Project → Settings*
sont relevés dans `bl_ui/space_topbar.py`.
