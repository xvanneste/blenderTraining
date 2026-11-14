# Fiche de révision — CH00.05 Extensions

- Extension = `.zip` + `blender_manifest.toml` ; dépôts : extensions.blender.org, User Default, System.
- Accès en ligne : Preferences → System → Network → Allow Online Access · `--online-mode` / `--offline-mode`.
- Installer : Get Extensions / Add-ons → ˅ → Install from Disk, ou glisser-déposer le `.zip`.
- Avant d'installer : source · licence · permissions · compatibilité · lecture du paquet.
- Add-ons livrés utiles : Node Wrangler (ph. 4), Rigify (ph. 6), Pose Library (ph. 7), BVH (ph. 7), FBX/glTF.
- Outils : `blender -c extension validate <dossier>` · `blender -c extension build --source-dir X --output-dir Y`.
- Panne au démarrage : `blender --factory-startup` → désactiver une à une.
- Sidebar de la vue 3D : `N` (onglets des add-ons).
