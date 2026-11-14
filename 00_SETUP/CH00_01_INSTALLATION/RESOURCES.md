# CH00.01 — Ressources

## Documentation officielle (consultée le 14/11/2026)
| Ressource | URL | Utilisée pour |
|---|---|---|
| Téléchargement | https://www.blender.org/download/ | Tutoriel 1 |
| Configuration requise | https://www.blender.org/download/requirements/ | Choix du matériel |
| Versions LTS | https://www.blender.org/download/lts/ | L1 |
| Notes de version 5.3 | https://developer.blender.org/docs/release_notes/5.3/ | L1, compatibilité |
| Manuel — Installation Windows | https://docs.blender.org/manual/en/latest/getting_started/installing/windows.html | L2 |
| Manuel — Disposition des dossiers (portable, chemins) | https://docs.blender.org/manual/en/latest/advanced/blender_directory_layout.html | L2, L3 |
| Manuel — Réglages initiaux (écran d'accueil) | https://docs.blender.org/manual/en/latest/getting_started/configuration/defaults.html | Tutoriel 2 |
| Manuel — Arguments de ligne de commande | https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html | L4 |
| Manuel — Rendu GPU Cycles | https://docs.blender.org/manual/en/latest/render/cycles/gpu_rendering.html | L4 |
| Manuel — Récupération (Recover) | https://docs.blender.org/manual/en/latest/files/blend/open_save.html | TROUBLESHOOTING |
| API Python | https://docs.blender.org/api/current/ | Scripts |
| Licence de Blender | https://www.blender.org/about/license/ | L1 |

Le manuel hors ligne est consultable depuis Blender : *Help → Manual*.

## Presse spécialisée (sortie de 5.3, sources secondaires)
- CG Channel, 11/11/2026 — annonce de Blender 5.3.
- Phoronix — « Blender 5.3 Released With NVIDIA DLSS 4.5 Ray Reconstruction, Vulkan Default ».
- 80.lv — « Blender 5.3 has finally arrived ».
Ces sources ont servi à repérer les nouveautés ; chaque fonction est revérifiée dans le
logiciel avant d'être enseignée.

## Ressources produites pour ce chapitre
Toutes sont **générées par script** (aucun téléchargement), licence de l'académie
(usage personnel libre). Détail dans `ASSET_MANIFEST.json`, identifiants `CH00_01-*`.

| Fichier | Généré par | Vérifié |
|---|---|---|
| `STARTER_FILES/ch00_01_testcard_starter.blend` | `build_ch00_01_files.py` | Ouverture + correcteur (échec attendu) |
| `STARTER_FILES/ch00_01_broken_render_starter.blend` | idem | Correcteur : 0/12, rendu noir (attendu) |
| `COMPLETED_EXAMPLES/ch00_01_testcard_solution.blend` | idem | Correcteur : 11/11, rendu OK |
| `COMPLETED_EXAMPLES/ch00_01_broken_render_solution.blend` | idem | Correcteur : 12/12, rendu OK |
| `COMPLETED_EXAMPLES/ch00_01_testcard_reference_render.png` | rendu OptiX 960×540, 128 éch. | Contrôle visuel |
| `COMPLETED_EXAMPLES/benchmark_reference/` | `bcma_render_benchmark.py` | CPU 7,41 s · CUDA 0,83 s · OptiX 0,84 s |
| `COMPLETED_EXAMPLES/system_report_reference/` | `bcma_system_report.py` | Diagnostic 5×OK |

## Pour aller plus loin
- Blender Studio (films ouverts et fichiers de production) : https://studio.blender.org/
- Blender Open Data (benchmark communautaire officiel, pour comparer votre machine à
  d'autres) : https://opendata.blender.org/
