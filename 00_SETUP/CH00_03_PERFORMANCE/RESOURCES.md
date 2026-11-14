# CH00.03 — Ressources

| Ressource | URL |
|---|---|
| Manuel — System preferences (Cycles devices, Display Graphics, Memory) | https://docs.blender.org/manual/en/latest/editors/preferences/system.html |
| Manuel — Viewport preferences | https://docs.blender.org/manual/en/latest/editors/preferences/viewport.html |
| Manuel — Simplify | https://docs.blender.org/manual/en/latest/render/cycles/render_settings/simplify.html |
| Manuel — Subdivision Surface | https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/subdivision_surface.html |
| Manuel — Link/Transfer Data | https://docs.blender.org/manual/en/latest/scene_layout/object/editing/link_transfer/index.html |
| Manuel — Optimisation du rendu Cycles | https://docs.blender.org/manual/en/latest/render/cycles/optimizations/index.html |
| Blender Open Data (benchmarks) | https://opendata.blender.org/ |

Vérifications 5.3.0 : libellés *Display Graphics → Backend*, *Viewport → Textures → Limit
Size*, *Viewport → Subdivision → GPU Subdivision*, *System → Memory & Limits → Undo Memory
Limit*, *System → Video Sequencer → Memory Cache Limit*, propriétés `render.use_simplify`,
`simplify_subdivision(_render)` contrôlés dans les sources et l'API.
Mesures : réalisées le 14/11/2026 sur le poste de référence.
